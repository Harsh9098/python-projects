from odoo import fields, models, api

class SaleApproval(models.Model):
    _name = "sale.order.approved"
    _description = "Sale order approved details"
    _rec_name = 'approval_level'

    approval_level = fields.Integer('Approval Level')
    user_ids = fields.Many2many('res.users', string='Users')
    group_ids = fields.Many2many('res.groups', string='Groups')
    state = fields.Boolean('State')
    approved_date = fields.Datetime('Approved Date')
    approved_id = fields.Many2one('res.users', string='Approved By')
    sale_approval_id = fields.Many2one('approval', string='Sale Approval')
    order_id = fields.Many2one('sale.order', string='Order')
    level = fields.Integer('Level')  # Define the 'level' field here

    @api.model
    def create(self, values):
        if values.get('approval_level'):
            values['level'] = values['approval_level']
        return super(SaleApproval, self).create(values)
