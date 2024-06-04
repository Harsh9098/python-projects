# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.
from odoo import fields, models, api, _
from odoo.exceptions import UserError, ValidationError
from odoo import fields, models, api, _

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    sale_approval_id = fields.Many2one('approval', string='Approval Level')   
    state = fields.Selection(
        selection_add=[('waiting', 'Waiting For Approval'), ('reject', 'Reject')])
    user_ids = fields.Many2many('res.users', string='Users', copy=False, compute="_compute_user_ids")
    group_ids = fields.Many2many('res.groups', string='Groups', copy=False, compute="_compute_group_ids")
    next_approval_level = fields.Integer(string='Next Approval Level', copy=False, compute='_compute_next_approval_level')
    reject_date = fields.Datetime('Reject Date', copy=False)
    rejected_user_id = fields.Many2one('res.users', string='Reject By', copy=False )
    reject_reason = fields.Text('Reject Reason', copy=False)
    sale_approved_ids = fields.One2many('sale.order.approved', 'order_id', string='Sale Approval Details')
    approved_date = fields.Date(copy=False)
    is_sale_approved = fields.Boolean(related='company_id.dynamic_approval')
    is_user_present = fields.Boolean(string="Is User Associated", compute='_compute_is_user_present')
    all_state_approved = fields.Boolean(
        'All Level Approved', default=False, compute='_compute_all_level_approved')
    is_reject = fields.Boolean(default=False)
    
    @api.depends('sale_approved_ids')
    def _compute_all_level_approved(self):
        for record in self:
            if record.sale_approved_ids and all(record.sale_approved_ids.mapped('state')):
                record.all_state_approved = True               
            else:
                record.all_state_approved = False
                
    @api.depends('sale_approval_id', 'sale_approved_ids.state')
    def _compute_next_approval_level(self):
        for order in self:
            if order.sale_approval_id:
                pending_lines = order.sale_approved_ids.filtered(lambda line: not line.state)
                if pending_lines:
                    order.next_approval_level = min(line.level for line in pending_lines)
                else:
                    order.next_approval_level = min(line.level for line in order.sale_approval_id.approval_line_ids)
            else:
                order.next_approval_level = 0

    @api.depends('sale_approval_id.approval_line_ids.user_ids', 'sale_approval_id.approval_line_ids.group_ids.users')
    def _compute_user_ids(self):
        for order in self:
            users = order.sale_approval_id.approval_line_ids.filtered(lambda line: line.level == order.next_approval_level).mapped('user_ids')
            group_users = order.sale_approval_id.approval_line_ids.filtered(lambda line: line.level == order.next_approval_level).mapped('group_ids.users')
            order.user_ids = users | group_users

    @api.depends('sale_approval_id')
    def _compute_group_ids(self):
        for order in self:
            order.group_ids = order.sale_approval_id.approval_line_ids.mapped('group_ids')

    def _prepare_approved_line(self, line):
        if line:
            return {
                'approval_level': line.level,
                'user_ids': [(6, 0, line.user_ids.ids)] if line.user_ids else False,
                'group_ids': [(6, 0, line.group_ids.ids)] if line.group_ids else False,
            }

    def action_approve(self):
        for order in self:
            if order.is_user_present and order.state == 'waiting':
                all_approved = all(line.state for line in order.sale_approved_ids)
                if all_approved:
                    for line in order.sale_approved_ids:
                        line.approved_id = self.env.user.id
                        line.approved_date = fields.Date.today()
                    order.write({'state': 'sale'})
                    order.approved_date = fields.Date.today()
                else:
                    pending_lines = order.sale_approved_ids.filtered(lambda line: not line.state)
                    if pending_lines:
                        if len(pending_lines) == 1:  # Only one pending line
                            pending_line = pending_lines[0]
                            pending_line.write({'state': True, 'approved_id': self.env.user.id, 'approved_date': fields.Date.today()})
                            order._compute_next_approval_level()  # Recompute next_approval_level after approval

                            all_levels_approved = all(line.state for line in order.sale_approved_ids)
                            if all_levels_approved:
                                order.write({'state': 'sale'})
                        else:
                            next_line = pending_lines[0]
                            next_line.write({'state': True, 'approved_id': self.env.user.id, 'approved_date': fields.Date.today()})
                    else:
                        raise UserError("All approval levels must be approved before changing the sale order status.")
            else:
                raise ValidationError(_('You do not have the rights for approval or the order is not in the waiting stage!'))
        return True

    def action_reject(self):
        if not self.is_reject:
            self.is_reject = True
        return {
            'name': _('Reject Orders'),
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'order.reject.wizard',
            'target': 'new',
            'context': {'default_rejection_order_id': self.id}
        }

    @api.depends('user_ids')
    def _compute_is_user_present(self):
        current_user = self.env.user
        for order in self:
            order.is_user_present = current_user in order.user_ids   

    def action_confirm(self):
        if self.is_sale_approved:
            for order in self:
                if not order.sale_approval_id:
                    approval_configs = self.env['approval'].search([])
                    closest_config = None
                    min_difference = float('inf')
                    for config in approval_configs:
                        if config.minimum_amount <= order.amount_total:
                            difference = order.amount_total - config.minimum_amount
                            if difference < min_difference:
                                min_difference = difference
                                closest_config = config
                    if closest_config:
                        order.sale_approval_id = closest_config.id
                        self.write({'state':'waiting'}) 
                        
                        approval_lines_ids = []
                        for line in order.sale_approval_id.approval_line_ids:
                            approval_lines_ids.append((0, 0, order._prepare_approved_line(line)))
                        if approval_lines_ids:
                            order.sale_approved_ids = approval_lines_ids  
                        approval_level = order.next_approval_level
                        if self.env.user in order.sale_approved_ids.filtered(lambda line: line.level == approval_level).user_ids:
                            order.action_approve()
                    else:
                        order.write({'state': 'sale'})  # No matching configuration found, proceed to sale state
                else:
                    all_lines_approved = all(line.state for line in order.sale_approved_ids)
                    if all_lines_approved:
                        order.write({'state': 'sale'})
        else:
            return super(SaleOrder, self).action_confirm()
