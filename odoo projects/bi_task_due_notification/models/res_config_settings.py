# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models , api

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    start_notifications = fields.Boolean(string="Delay Task Start notification")
    delay_notifications = fields.Boolean(string="Delay Task Deadline / Overdue Notification")
    start_days= fields.Integer(string='Delay Day(s):-',default=0)
    deadline_days = fields.Integer(string='Delay Deadline Day(s):-',default=0)
    
        
    def set_values(self):
        super(ResConfigSettings, self).set_values()
        config_parameter = self.env['ir.config_parameter'].sudo()

        config_parameter.set_param('start_notifications', self.start_notifications)
        config_parameter.set_param('delay_notifications', self.delay_notifications)
        config_parameter.set_param('start_days', self.start_days)
        config_parameter.set_param('deadline_days', self.deadline_days)

    @api.model
    def get_values(self):
        res = super(ResConfigSettings, self).get_values()
        config_parameter = self.env['ir.config_parameter'].sudo()

        start_notifications = config_parameter.get_param('start_notifications', default=False)
        delay_notifications = config_parameter.get_param('delay_notifications', default=False)
        start_days = int(config_parameter.get_param('start_days', default=0))
        deadline_days = int(config_parameter.get_param('deadline_days', default=0))

        res.update(
            start_notifications=start_notifications,
            delay_notifications=delay_notifications,
            start_days=start_days,
            deadline_days=deadline_days
        )

        return res

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
