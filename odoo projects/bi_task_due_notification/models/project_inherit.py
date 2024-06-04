# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models , api
from datetime import timedelta

class TaskNotification(models.Model):
    _inherit ='project.task'
    
    start_date = fields.Date(string='Start Date')
    date_deadline = fields.Date(string='Deadline')
    task_completed = fields.Boolean(string="Task Completed" ,default=False)
    notified = fields.Boolean(string="Notified", default=False)
    deadline_notified = fields.Boolean(string="Deadline Notified", default=False)
    
    @api.onchange('stage_id')
    def task_complete(self):
        if self.stage_id.name == 'Done':
            self.task_completed = True
        else:
            self.task_completed = False

    def send_start_notification_email(self):
        today = fields.Date.today()
        start_days = int(self.env['ir.config_parameter'].sudo().get_param('start_days'))
        start_date_check = today - timedelta(days=start_days)
        
        tasks = self.search([('start_date', '=', start_date_check), ('notified', '=', False)], order='id', limit=1)
        template = self.env.ref('bi_task_due_notification.reminder_task_notification')

        processed_tasks = []

        for task in tasks:
            template.send_mail(task.id, force_send=True)
            task.write({'notified': True})
            processed_tasks.append(task.id)

        return processed_tasks
    
    def send_deadline_notification_email(self):
        today = fields.Date.today()
        deadline_days = int(self.env['ir.config_parameter'].sudo().get_param('deadline_days'))
        deadline_date_check = today + timedelta(days=deadline_days)
        tasks = self.search([('date_deadline', '=', deadline_date_check), ('deadline_notified', '=', False)], order='id', limit=1)
        template = self.env.ref('bi_task_due_notification.reminder_deadline_task_notification')

        processed_tasks = []

        for task in tasks:
            template.send_mail(task.id, force_send=True)
            task.write({'deadline_notified': True})
            processed_tasks.append(task.id)

        return processed_tasks
    
    def write(self, vals):
        res = super(TaskNotification, self).write(vals)
    
        if 'start_date' in vals:
            for record in self:
                if record.start_date:
                    record.notified = False
        
        if 'date_deadline' in vals:
            for record in self:
                if record.date_deadline:
                    record.deadline_notified = False

        return res

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
