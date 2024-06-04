# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.
{
    'name': 'Customer Credit Limit',
    'version': '17.0.0.0',
    'description': '''custom module ''',
    'depends': ['base','sale' , 'account'],
    'data': [
       'security/ir.model.access.csv',
       'wizard/credit_limt_wizard.xml',
       'data/block_acc_email.xml',
       'views/credit_limit.xml',
    ],
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
