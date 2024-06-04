# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.
from odoo import fields, models, api, _
from odoo . exceptions import ValidationError

class CustomerCredit(models.Model):
    _inherit = "res.partner"
    is_credit_limit = fields.Boolean(string="Is Credit Limit")
    credit_limit_customer = fields.Integer(string="Credit Limit customer")
    blocking_limit = fields.Integer(string="Blocking Limit")
    put_on_hold = fields.Boolean(string="Put on Hold")
    total_invoice_ids = fields.One2many('account.move', 'partner_id')
    payment_ids = fields.One2many(
        'account.payment', 'partner_id', string='Payments')
    
class AccountMove(models.Model):
    _inherit = 'account.move'
    is_paid = fields.Boolean(string='Is Paid', compute='_compute_is_paid')

    @api.depends('amount_residual')
    def _compute_is_paid(self):
        for move in self:
            move.is_paid = move.amount_residual == 0

class SaleOrder(models.Model):
    _inherit = "sale.order"
    credit_limit_sale = fields.Integer(
        string="Credit Limit", related='partner_id.credit_limit_customer')
    total_receivable = fields.Float(
        string="Total Receivable", compute="_compute_total_receivable")
    customer_due_amount = fields.Float(
        "Customer Due Amount", compute="_compute_due_amount")
    cross_credit_limit_warnning = fields.Boolean(default=False)
    sale_url_mail = fields.Char(string="url", compute="_compute_sale_url")

    @api.depends('name')
    def _compute_sale_url(self):
        base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
        for order in self:
            order.sale_url_mail = base_url + '/web#id=%s&view_type=form&model=sale.order' % order.id

    @api.onchange('customer_due_amount','credit_limit_sale')
    def _onchange_(self):
        if self.credit_limit_sale < self.customer_due_amount:
           self.cross_credit_limit_warnning = True
        else:
            self.cross_credit_limit_warnning = False
            
    @api.depends('partner_id', 'partner_id.total_invoice_ids')
    def _compute_total_receivable(self):
        for order in self:
            total_receivable = sum(order.partner_id.total_invoice_ids.filtered(
                lambda inv: inv.state == 'posted').mapped('amount_total'))
            order.total_receivable = total_receivable
            
    @api.depends('partner_id', 'partner_id.total_invoice_ids', 'partner_id.payment_ids')
    def _compute_due_amount(self):
        for order in self:
            total_due = sum(order.partner_id.total_invoice_ids.filtered(
                lambda inv_state: inv_state.state == 'posted' and not inv_state.is_paid).mapped('amount_total'))
            order.customer_due_amount = total_due

    def action_confirm(self):
        res = super(SaleOrder, self).action_confirm()
        for order in self:
            if order.partner_id.blocking_limit < order.customer_due_amount:
                raise ValidationError("Customer is in blocking stage and has to pay %s" % order.customer_due_amount)
       
            elif order.customer_due_amount > order.credit_limit_sale:
                order.partner_id.put_on_hold = True
                template_id = self.env.ref('bi_customer_limit.customer_credit_limit_mail').id
                template = self.env['mail.template'].browse(template_id)
                if template:
                    if order.id: 
                        template.send_mail(order.id, force_send=True)
                return {
                    'name': _('Confirm credit limit'),
                    'view_mode': 'form',
                    'view_type': 'form',
                    'res_model': 'credit.limit.wizard',
                    'type': 'ir.actions.act_window',
                    'target': 'new',
                    'context': {
                        'default_name': self.partner_id.name,
                        'default_current_order': self.name,
                        'default_credit_limit': self.partner_id.credit_limit_customer,
                        'default_put_on_hold': self.partner_id.put_on_hold,
                        'default_total_receivable': self.total_receivable,
                        'default_current_quotations': self.amount_total,
                        'default_due_after': self.customer_due_amount + self.amount_total,
                        'default_exceeded_amount': self.total_receivable,
                    },
                }
