# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.

import odoo.addons.decimal_precision as dp
from odoo import api, fields, models, _
from odoo.exceptions import AccessError, UserError, RedirectWarning, ValidationError
from odoo.tools import float_is_zero, float_compare


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    discount_per = fields.Float('Discount %')
    discount_amount = fields.Float('Discount')


    @api.onchange('product_id')
    def _compute_name(self):
        res = super(SaleOrderLine, self)._compute_name()
        
        if self.product_id:
            self.discount_amount = self.product_id.discount_amount
        return res

    @api.onchange('discount_amount')
    def onchnage_discount(self):
        discount_warning = self.env['ir.config_parameter'].sudo().get_param('bi_product_discount.discount_warning')
        warning_message = self.env['ir.config_parameter'].sudo().get_param('bi_product_discount.warning_message')
        if discount_warning:
            if self.discount_amount > self.product_id.discount_amount or self.discount_amount < self.product_id.discount_amount:
                if warning_message:
                    raise ValidationError(_(warning_message))
                else:
                    raise ValidationError(_('You cannot change the discount from sale order line'))
        else:
            self.discount_amount =self.product_id.discount_amount

    def _prepare_invoice_line(self, **optional_values):
        res = super(SaleOrderLine,self)._prepare_invoice_line(**optional_values)
        res.update({'discount_amount': self.discount_amount,
                    })
        return res

    @api.depends('product_uom_qty', 'discount', 'discount_amount', 'price_unit', 'tax_id')
    def _compute_amount(self):
        """
        Compute the amounts of the SO line.
        """
        for line in self:
            if line.product_id.discount_method == 'fix':
                price = line.price_unit - line.product_id.discount_amount            
            elif line.product_id.discount_method == 'per':
                price = line.price_unit * (1 - (line.product_id.discount_amount or 0.0) / 100.0)
            else:
                price = line.price_unit * (1 - (line.discount or 0.0) / 100.0)
            taxes = line.tax_id.compute_all(price, line.order_id.currency_id, line.product_uom_qty, product=line.product_id, partner=line.order_id.partner_shipping_id)
            line.update({
                'price_tax': sum(t.get('amount', 0.0) for t in taxes.get('taxes', [])),
                'price_total': taxes['total_included'],
                'price_subtotal': taxes['total_excluded'],
            })

    def _convert_to_tax_base_line_dict(self):
        """ Convert the current record to a dictionary in order to use the generic taxes computation method
        defined on account.tax.

        :return: A python dictionary.
        """
        self.ensure_one()
        discount = 0
        if self.product_id.discount_method == 'fix':
            discount = ((self.discount_amount) / self.price_unit) * 100 or 0.00
        if self.product_id.discount_method == 'per':
            discount = self.discount_amount

        if discount > 0:
            return self.env['account.tax']._convert_to_tax_base_line_dict(
                self,
                partner=self.order_id.partner_id,
                currency=self.order_id.currency_id,
                product=self.product_id,
                taxes=self.tax_id,
                price_unit=self.price_unit,
                quantity=self.product_uom_qty,
                discount= discount,
                price_subtotal=self.price_subtotal,
            )
        else:
            return self.env['account.tax']._convert_to_tax_base_line_dict(
                self,
                partner=self.order_id.partner_id,
                currency=self.order_id.currency_id,
                product=self.product_id,
                taxes=self.tax_id,
                price_unit=self.price_unit,
                quantity=self.product_uom_qty,
                discount=self.discount,
                price_subtotal=self.price_subtotal,
            )