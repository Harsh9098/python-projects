# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.
from odoo import models, fields, api

class SaleOrderTotal(models.Model):
    _inherit = 'sale.order'
 
    total_weight = fields.Float(string="Total Weight(KG)", compute='_compute_total_weight', store=True)

    @api.depends('order_line.weight')
    def _compute_total_weight(self):
        for order in self:
            order.total_weight = sum(order.order_line.mapped('weight'))

class AccountMoveTotal(models.Model):
    _inherit = 'account.move'
   
    invoice_weight = fields.Float(string="Total Weight(KG)", compute='_compute_invoice_weight', store=True)
    
    @api.depends('invoice_line_ids.weight_invoice')
    def _compute_invoice_weight(self):
        for invoice in self:
            invoice.invoice_weight = sum(float(line.weight_invoice) for line in invoice.invoice_line_ids)

class StockPickingTotal(models.Model):
    _inherit = "stock.picking"   

    total_weight = fields.Float(string="Total Weight(KG)", compute='_compute_total_weight', store=True)

    @api.depends('move_ids.weight_stock')
    def _compute_total_weight(self):
        for picking in self:
            picking.total_weight = sum(picking.move_ids.mapped('weight_stock'))