# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.
from odoo import  fields, models

class ProductCategorySetting(models.Model):
    _inherit = 'product.category'

    product_category_ids = fields.One2many('commission.settings','product_category_id','Commission Settings')
