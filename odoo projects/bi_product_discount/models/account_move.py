# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.

import odoo.addons.decimal_precision as dp
from odoo import api, fields, models, _
from odoo.exceptions import AccessError, UserError, RedirectWarning, ValidationError
from odoo.tools import float_is_zero, float_compare, frozendict, formatLang, format_date, Query


class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'
 
    discount_amount = fields.Float('Discount')
    discount_per = fields.Float('Discount %')

    @api.onchange('discount_amount')
    def onchnage_discount(self):
        discount_warning = self.env['ir.config_parameter'].sudo().get_param('bi_product_discount.discount_warning')
        warning_message = self.env['ir.config_parameter'].sudo().get_param('bi_product_discount.warning_message')
        if not self.product_id.discount_method and not self.product_id.discount_amount:
            if self.discount_amount:
                self.discount = (self.discount_amount/self.price_unit*100)
        elif discount_warning:
            if self.discount_amount > self.product_id.discount_amount or self.discount_amount < self.product_id.discount_amount:
                if warning_message:
                    raise ValidationError(_(warning_message))
                else:
                    raise ValidationError(_("Please ! Don't modify discount value !!"))
        else:
            self.discount_amount =self.product_id.discount_amount

    @api.depends('quantity', 'discount','discount_amount', 'price_unit', 'tax_ids', 'currency_id')
    def _compute_totals(self):
        for line in self:
            if line.display_type != 'product':
                line.price_total = line.price_subtotal = False
            # Compute 'price_subtotal'.
            discount_warning = self.env['ir.config_parameter'].sudo().get_param('bi_product_discount.discount_warning')
            warning_message = self.env['ir.config_parameter'].sudo().get_param('bi_product_discount.warning_message')

            if line.product_id.discount_amount > 0:
                if line.discount_amount > 0:
                    if line.product_id.discount_method == 'fix':
                        line_discount_price_unit = line.price_unit - line.discount_amount
                    elif line.product_id.discount_method == 'per':
                        line_discount_price_unit = line.price_unit * (1 - (line.discount_amount / 100.0))
                else:
                    line_discount_price_unit = line.price_unit * (1 - (line.discount / 100.0))

                subtotal = line.quantity * line_discount_price_unit
                # Compute 'price_total'.
                if line.tax_ids:
                    taxes_res = line.tax_ids.compute_all(
                        line_discount_price_unit,
                        quantity=line.quantity,
                        currency=line.currency_id,
                        product=line.product_id,
                        partner=line.partner_id,
                        is_refund=line.is_refund,
                    )
                    line.price_subtotal = taxes_res['total_excluded']
                    line.price_total = taxes_res['total_included']
                else:
                    line.price_total = line.price_subtotal = subtotal
            else:
                line_discount_price_unit = line.price_unit * (1 - (line.discount / 100.0))
                subtotal = line.quantity * line_discount_price_unit

                # Compute 'price_total'.
                if line.tax_ids:
                    taxes_res = line.tax_ids.compute_all(
                        line_discount_price_unit,
                        quantity=line.quantity,
                        currency=line.currency_id,
                        product=line.product_id,
                        partner=line.partner_id,
                        is_refund=line.is_refund,
                    )
                    line.price_subtotal = taxes_res['total_excluded']
                    line.price_total = taxes_res['total_included']
                else:
                    line.price_total = line.price_subtotal = subtotal

                if discount_warning:
                    if line.discount_amount > line.product_id.discount_amount or line.discount_amount < line.product_id.discount_amount:
                        if warning_message:
                            raise ValidationError(_(warning_message))
                        else:
                            raise ValidationError(_('You cannot change the discount from sale order line'))
                else:
                    line.discount_amount =line.product_id.discount_amount

    @api.depends('tax_ids', 'currency_id', 'partner_id', 'analytic_distribution', 'balance', 'partner_id', 'move_id.partner_id', 'price_unit')
    def _compute_all_tax(self):
        for line in self:
            sign = line.move_id.direction_sign
            if line.display_type == 'tax':
                line.compute_all_tax = {}
                line.compute_all_tax_dirty = False
                continue
            if line.display_type == 'product' and line.move_id.is_invoice(True):
                discount = 0
                if line.product_id.discount_method == 'fix':
                    discount = ((line.discount_amount) / line.price_unit) * 100 or 0.00
                elif line.product_id.discount_method == 'per':
                    discount = line.discount_amount

                amount_currency = sign * line.price_unit * (1 - (discount / 100.0))
                handle_price_include = True
                quantity = line.quantity
            else:
                amount_currency = line.amount_currency
                handle_price_include = False
                quantity = 1
            compute_all_currency = line.tax_ids.compute_all(
                amount_currency,
                currency=line.currency_id,
                quantity=quantity,
                product=line.product_id,
                partner=line.move_id.partner_id or line.partner_id,
                is_refund=line.is_refund,
                handle_price_include=handle_price_include,
                include_caba_tags=line.move_id.always_tax_exigible,
                fixed_multiplicator=sign,
            )
            rate = line.amount_currency / line.balance if line.balance else 1
            line.compute_all_tax_dirty = True
            line.compute_all_tax = {
                frozendict({
                    'tax_repartition_line_id': tax['tax_repartition_line_id'],
                    'group_tax_id': tax['group'] and tax['group'].id or False,
                    'account_id': tax['account_id'] or line.account_id.id,
                    'currency_id': line.currency_id.id,
                    'analytic_distribution': (tax['analytic'] or not tax['use_in_tax_closing']) and line.analytic_distribution,
                    'tax_ids': [(6, 0, tax['tax_ids'])],
                    'tax_tag_ids': [(6, 0, tax['tag_ids'])],
                    'partner_id': line.move_id.partner_id.id or line.partner_id.id,
                    'move_id': line.move_id.id,
                    'display_type': line.display_type,
                }): {
                    'name': tax['name'],
                    'balance': tax['amount'] / rate,
                    'amount_currency': tax['amount'],
                    'tax_base_amount': tax['base'] / rate * (-1 if line.tax_tag_invert else 1),
                }
                for tax in compute_all_currency['taxes']
                if tax['amount']
            }
            if not line.tax_repartition_line_id:
                line.compute_all_tax[frozendict({'id': line.id})] = {
                    'tax_tag_ids': [(6, 0, compute_all_currency['base_tags'])],
                }

    def _convert_to_tax_base_line_dict(self):
        """ Convert the current record to a dictionary in order to use the generic taxes computation method
        defined on account.tax.
        :return: A python dictionary.
        """
        self.ensure_one()
        is_invoice = self.move_id.is_invoice(include_receipts=True)
        sign = -1 if self.move_id.is_inbound(include_receipts=True) else 1
        discount = 0
        if self.product_id.discount_method == 'fix':
            discount = ((self.discount_amount) / self.price_unit) * 100 or 0.00
        if self.product_id.discount_method == 'per':
            discount = self.discount_amount

        if discount > 0:          
            return self.env['account.tax']._convert_to_tax_base_line_dict(
                self,
                partner=self.partner_id,
                currency=self.currency_id,
                product=self.product_id,
                taxes=self.tax_ids,
                price_unit=self.price_unit if is_invoice else self.amount_currency,
                quantity=self.quantity if is_invoice else 1.0,
                discount= discount if is_invoice else 0.0,
                account=self.account_id,
                analytic_distribution=self.analytic_distribution,
                price_subtotal=sign * self.amount_currency,
                is_refund=self.is_refund,
                rate=(abs(self.amount_currency) / abs(self.balance)) if self.balance else 1.0
            )
        else:
            return self.env['account.tax']._convert_to_tax_base_line_dict(
                self,
                partner=self.partner_id,
                currency=self.currency_id,
                product=self.product_id,
                taxes=self.tax_ids,
                price_unit=self.price_unit if is_invoice else self.amount_currency,
                quantity=self.quantity if is_invoice else 1.0,
                discount= self.discount if is_invoice else 0.0,
                account=self.account_id,
                analytic_distribution=self.analytic_distribution,
                price_subtotal=sign * self.amount_currency,
                is_refund=self.is_refund,
                rate=(abs(self.amount_currency) / abs(self.balance)) if self.balance else 1.0
            )

    @api.depends('product_id', 'journal_id')
    def _compute_name(self):
        res = super(AccountMoveLine, self)._compute_name()
        
        if self.product_id:
            self.discount_amount = self.product_id.discount_amount
        return res   
