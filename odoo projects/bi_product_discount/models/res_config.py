# -*- coding: utf-8 -*-
# Part of Browseinfo. See LICENSE file for full copyright and licensing details.


from odoo import fields,models,api, _


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'
    
    discount_warning = fields.Boolean(string='Product Discount Limit Warning')
    warning_message=fields.Text(string='Warning Message')
    

    def get_values(self):
        res = super(ResConfigSettings, self).get_values()
        res.update(
            discount_warning = self.env['ir.config_parameter'].sudo().get_param('bi_product_discount.discount_warning'),
            warning_message=self.env['ir.config_parameter'].sudo().get_param('bi_product_discount.warning_message')
        )
        return res

    def set_values(self):
        super(ResConfigSettings, self).set_values()
        self.env['ir.config_parameter'].sudo().set_param('bi_product_discount.discount_warning', self.discount_warning)
        self.env['ir.config_parameter'].sudo().set_param('bi_product_discount.warning_message', self.warning_message)

