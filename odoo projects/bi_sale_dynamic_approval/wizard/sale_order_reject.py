from odoo import _, api, fields, models, tools
from odoo.exceptions import UserError, ValidationError
import datetime

class RejectedOrders(models.TransientModel):
    _name = 'order.reject.wizard'
    _description = "Rejected orders"

    reason_rejection = fields.Text(string='Reason On Rejected Order')

    rejection_order_id = fields.Many2one('sale.order')

    def reject_order_wizard(self):
        for order in self.rejection_order_id:
            user_activet = self.env.user
            order.reject_reason = self.reason_rejection
            order.reject_date = datetime.datetime.now()
            order.rejected_user_id = user_activet          
            order.write({'state': 'reject'})
        return True
