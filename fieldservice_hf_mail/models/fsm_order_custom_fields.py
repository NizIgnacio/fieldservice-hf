from odoo import models, fields

class FSMOrderSignatureField(models.Model):
    _inherit = "fsm.order"

    dni = fields.Char()
    signed_by = fields.Char()
    signature = fields.Image(max_width=1024, max_height=1024)


class WizardDNIFieldClass(models.TransientModel):
    _inherit = "fsm.order.sign.wizard"

    dni = fields.Char()

    def action_sign(self):
        res = super().action_sign()
        self.order_id.write({'dni': self.dni})
        return res
