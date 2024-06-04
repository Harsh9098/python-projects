# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.
from odoo import models, fields

class SaleOrderLineInvoice(models.Model):
    _inherit = 'sale.order.line'

    weight = fields.Float(string="Weight(KG)", related='product_id.product_tmpl_id.weight', readonly=True)

    def _prepare_invoice_line(self, **optional_values):
        res = super(SaleOrderLineInvoice, self)._prepare_invoice_line(**optional_values)
        res['weight_invoice'] = self.weight
        return   res

class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    weight_invoice = fields.Char(string="Weight(KG)")

class StockPicking(models.Model):
    _inherit = "stock.move"   
    
    weight_stock = fields.Float(string="Weight(KG)", related='sale_line_id.weight', readonly=True)
