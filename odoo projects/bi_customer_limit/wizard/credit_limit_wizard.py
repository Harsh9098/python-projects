# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.
from odoo import models, fields, api


class CustomerCreditLimitWizard(models.TransientModel):
    _name = 'credit.limit.wizard'
    _description = 'Customer Credit Limit Wizard'

    name = fields.Char(string='Name')
    current_order = fields.Char(string="Current Order")
    credit_limit=  fields.Integer(string="Credit Limit")
    put_on_hold =  fields.Boolean(string="Put On Hold") 
    total_receivable = fields.Float(string="Total Receivable")
    current_quatations = fields.Float(string="Current Quatations")
    due_after = fields.Float(string="Due After This Quatations")
    exceeded_amount=fields.Float(string="Exceeded Amount")

   