# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Task Delay and Overdue Task Notification',
    'version': '17.0.0.0',
    'description': '''custom module ''',

    'depends': ['base','project'],
    'data': [
      
        'data/remider_start_mail_data.xml',
        'data/remider_deadline_mail_data.xml',
        'data/scheduled_action.xml',
        'views/res_config_settings.xml',
        'views/project_task_inherit.xml',
        
        
    ],
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}

