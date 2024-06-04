# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.
from odoo import fields, models ,api

class SaleOrder(models.Model):
    _inherit = "sale.order"

    sale_commission_user_ids = fields.One2many('commission.settings','sale_order_id','Commission Settings')
    def action_confirm(self):
        res = super(SaleOrder, self).action_confirm()
        commission_line_obj = self.env['sale.commission.line']
        calculation_setting = self.env['ir.config_parameter'].sudo().get_param('commission_calculation_setting', 'product')
        commission_conf_setting = self.env['ir.config_parameter'].sudo().get_param('commission_conf_setting', 'sale_order_commission')

        for order in self:
            for user in order.sale_commission_user_ids:
                commission_date = fields.Date.today()
                source_document = order.name
                amount = 0.0
                if commission_conf_setting == 'sale_order_commission':
                    if calculation_setting == 'product':
                        for line in order.order_line:
                            commission_percentage = line.product_id.commission_settings_ids.filtered(lambda x: x.commission_level_id == user.commission_level_id).percentage
                            amount += line.price_subtotal * (commission_percentage / 100)
                    elif calculation_setting == 'product_category':
                            for line in order.order_line:
                                product_category = line.product_id.categ_id
                                if product_category:
                                    commission_settings = self.env['commission.settings'].search([
                                        ('product_category_id', '=', product_category.id),
                                        ('commission_level_id', '=', user.commission_level_id.id)
                                    ])
                                    if commission_settings:
                                        amount += line.price_subtotal * (commission_settings.percentage / 100)
                    elif calculation_setting == 'partner':
                                for line in order.order_line:
                                    partner = line.order_id.partner_id
                                    if partner:
                                        commission_settings = self.env['commission.settings'].search([
                                            ('partner_id', '=', partner.id),
                                            ('commission_level_id', '=', user.commission_level_id.id)
                                        ])
                                        if commission_settings:
                                            amount += line.price_subtotal * (commission_settings.percentage / 100)
                    elif calculation_setting == 'sales_team':
                        for line in order.order_line:
                            sales_team = line.order_id.team_id
                            if sales_team:
                                commission_settings = self.env['commission.settings'].search([
                                    ('sales_team_id', '=', sales_team.id),
                                    ('commission_level_id', '=', user.commission_level_id.id)
                                ])
                                if commission_settings:
                                    amount += line.price_subtotal * (commission_settings.percentage / 100)
                    commission_line_obj.create({
                        'commission_date': commission_date,
                        'sales_partner': user.partner_coman_id.id,
                        'source_document': source_document,
                        'amount': amount,
                    })
        return res
    
class SalesCommissionLines(models.Model):   
    _name = 'sale.commission.line'
    _description='sale commission Line'
    _rec_name = 'sales_partner'
    _order = "id desc"
    
    commission_date = fields.Date('Commission Date')
    sales_partner = fields.Many2one('res.partner', 'Sales Partner')
    source_document = fields.Char('Source Document')
    amount = fields.Float('Amount')
 
 
   