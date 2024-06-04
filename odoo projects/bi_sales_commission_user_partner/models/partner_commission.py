# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.
from odoo import api, fields, models
from odoo.exceptions import ValidationError

class PartnersSetting(models.Model):
    _inherit = 'res.partner'

    commission_settings_ids = fields.One2many('commission.settings','partner_id','Commission Settings')
