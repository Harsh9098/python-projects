# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.
from odoo import fields, models

class ApprovalLine(models.Model):
    _name = "approval.line"
    _description = "Approval Line"
    _rec_name = 'level'

    approve_process_by = fields.Selection(
        string='Approve Process By',
        selection=[('user', 'User'),('group', 'Group')], default="user")
    level = fields.Integer(string='Level')
    group_ids = fields.Many2many(string='Group Name',comodel_name='res.groups')
    user_ids = fields.Many2many('res.users')
    approval_id = fields.Many2one('approval', string='Approvals')
