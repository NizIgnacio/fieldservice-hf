from odoo import models, fields, api, _
from odoo.exceptions import UserError
import base64


class MailWizard(models.TransientModel):
    _name = "mail.wizard"
    _description = "Script in charge of creating the mail wizard, and sending the email with the corresponding fields"

    mail_from = fields.Char(required=True)
    mail_to = fields.Char(required=True)
    mail_subject = fields.Char(required=True)
    mail_content = fields.Html()
    mail_cc = fields.Char()
    attachment_ids = fields.Many2many("ir.attachment")

    @api.model
    def default_get(self, fields_list):
        res = super().default_get(fields_list)

        active_model = self.env.context.get("active_model")
        active_id = self.env.context.get("active_id")

        if active_model == "fsm.order" and active_id:
            order = self.env["fsm.order"].browse(active_id)

            report = self.env.ref("fieldservice_hf_mail.service_order_record_temp")
            pdf_content, _ = report._render_qweb_pdf(report.id, res_ids=[order.id])

            attachment = self.env["ir.attachment"].create({
                "name": f"Orden_de_Servicio_{order.name}.pdf",
                "type": "binary",
                "datas": base64.b64encode(pdf_content).decode("utf-8"),
                "mimetype": "application/pdf",
            })

            res["attachment_ids"] = [(4, attachment.id)]

            #if order.person_id and order.person_id.partner_id:
            #    res["mail_from"] = order.person_id.partner_id.email or ""

            res["mail_from"] = self.env.user.email

            if order.location_id:
                res["mail_to"] = order.location_id.email or ""

            res["mail_subject"] = f"Service Order ({order.location_id.name})"

        return res

    def BuildAndSend(self):
        self.ensure_one()

        active_id = self.env.context.get("active_id")
        order = self.env["fsm.order"].browse(active_id)

        report = self.env.ref("fieldservice_hf_mail.service_order_record_temp")
        pdf_content, __ = report._render_qweb_pdf(report.id, res_ids=[order.id])

        attachment = self.env["ir.attachment"].create({
            "name": f"Orden_de_Servicio_{order.name}.pdf",
            "type": "binary",
            "datas": base64.b64encode(pdf_content).decode("utf-8"),
            "mimetype": "application/pdf",
        })

        mail = self.env["mail.mail"].create({
            "email_to": self.mail_to,
            "email_from": self.mail_from,
            "email_cc": self.mail_cc,
            "subject": self.mail_subject,
            "body_html": self.mail_content,
            "attachment_ids": [(4, attachment.id)],
        })

        try:
            mail.send()
            return {
                "type": "ir.actions.client",
                "tag": "display_notification",
                "params": {
                    "title": _("Success"),
                    "message": _("The mail has been successfully sent"),
                    "type": "success",
                    "sticky": False,
                    "next": {
                        "type": "ir.actions.act_window_close",
                    },
                },
            }
        except Exception as e:
            raise UserError(_(f"Failed to send email: {str(e)}"))
