# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.
from odoo import  fields, models

class ProductTemplateSetting(models.Model):
    _inherit = 'product.template'

    commission_settings_ids = fields.One2many('commission.settings','product_id','Commission Settings')
    commission_product = fields.Boolean(string="Commission Product")