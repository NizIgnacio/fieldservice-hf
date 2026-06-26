from odoo import models, fields

class WizardDNIFieldClass(models.TransientModel):
    _inherit = "fsm.order.sign.wizard"

    dni = fields.Char()

    def action_sign(self):
        res = super().action_sign()
        self.order_id.write({'dni': self.dni})
        return res

class FSMOrder(models.Model):
    _inherit = "fsm.order"

    dni = fields.Char()
