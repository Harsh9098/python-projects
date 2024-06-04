# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models,api, _

class Approval(models.Model):
    _name = "approval"
    _description = "Approval"

    name = fields.Char(required=True, index=True, string="Name")
    minimum_amount = fields.Float(string='Minimum Amount')
    sale_person = fields.Boolean('Sales Person Always in CC')
    approval_line_ids = fields.One2many(
        'approval.line',
        'approval_id',
        string='Approval Lines'
    )