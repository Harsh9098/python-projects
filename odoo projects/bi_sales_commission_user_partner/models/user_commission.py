# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.
from odoo import api, fields, models

class ResUsers(models.Model):
    _inherit = 'res.users'

    manage_sale_commission = fields.Boolean(string="Manage Sale commission")
    