# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.
from odoo import fields, models, _
from odoo.exceptions import ValidationError

class CommissionConfigSetting(models.TransientModel):
    _inherit = "res.config.settings"
    
    calculation_setting = fields.Selection([('sales_team', 'Sales Team'),
                                           ('product_category','Product Category'),
                                           ('product', 'Product'),
                                           ('partner', 'Partner'),
                                            ], string='Commission Calculation Based On ', default='product')

    commission_conf_setting = fields.Selection([('sale_order_commission', 'Commission based on Sales Order'),
                                                ('purchase_order_commission', 'commission based on Purchase')], string='Commission based on Sales Order', default='sale_order_commission')

    def default_get(self, fields):
        res = super(CommissionConfigSetting, self).default_get(fields)
        res.update({
            'calculation_setting': self.env['ir.config_parameter'].sudo().get_param('commission_calculation_setting', 'product'),
            'commission_conf_setting': self.env['ir.config_parameter'].sudo().get_param('commission_conf_setting', 'sale_order_commission'),
        })
        return res

    def set_values(self):
        super(CommissionConfigSetting, self).set_values()
        self.env['ir.config_parameter'].sudo().set_param('commission_calculation_setting', self.calculation_setting)
        self.env['ir.config_parameter'].sudo().set_param('commission_conf_setting', self.commission_conf_setting)
    
        if self.commission_conf_setting == 'purchase_order_commission' and self.calculation_setting == 'sales_team':
                raise ValidationError(_("Cannot select 'Sales Team' for calculation setting when 'Commission based on Purchase' is selected."))