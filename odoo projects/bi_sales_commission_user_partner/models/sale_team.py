# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.
from odoo import  fields, models

class SaleTeamSetting(models.Model):
    _inherit = 'crm.team'
    
    commission_settings_ids = fields.One2many('commission.settings','sales_team_id','Commission Settings')      
    