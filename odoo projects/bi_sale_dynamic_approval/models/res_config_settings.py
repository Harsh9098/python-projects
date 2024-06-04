# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    dynamic_approval_check = fields.Boolean(string='Dynamic Approval',related='company_id.dynamic_approval' , readonly=False)

class ResCompany(models.Model):
    _inherit = 'res.company'

    dynamic_approval = fields.Boolean(string='Dynamic Approval' , default=False)
    