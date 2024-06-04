# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.
from odoo import fields, models

class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    purchase_commission_user_ids = fields.One2many('commission.settings', 'purchase_order_id', 'Commission Settings')

    def button_confirm(self):
        res = super(PurchaseOrder, self).button_confirm()

        calculation_setting = self.env['ir.config_parameter'].sudo().get_param('commission_calculation_setting', 'product')

        commission_conf_setting = self.env['ir.config_parameter'].sudo().get_param('commission_conf_setting', 'purchase_order_commission')

        for order in self:
            for user in order.purchase_commission_user_ids:
                commission_date = fields.Date.today()
                source_document = order.name
                amount = 0.0

                if commission_conf_setting == 'purchase_order_commission':
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

                    commission_line_obj = self.env['sale.commission.line']
                    commission_line_obj.create({
                        'commission_date': commission_date,
                        'sales_partner': user.partner_coman_id.id,
                        'source_document': source_document,
                        'amount': amount,
                    })
        return res

