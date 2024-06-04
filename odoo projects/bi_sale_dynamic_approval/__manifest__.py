# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.
{
    'name': 'Sales Order Dynamic Approval ',
    'version': '17.0.0.0',
    'description': '''custom module ''',

    'depends': ['base','sale_management','sale'],
    'data': [
        'security/ir.model.access.csv',
        'views/approval_form.xml',
        'views/res_config_settings_views.xml',
        'views/sale_oder.xml',
        'views/approval_line.xml',
        'wizard/sale_order_reject_views.xml',
    ],
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}
