# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.
{
    'name': 'Product Weight Calculation',
    'version': '17.0.0.0',
    'description': '''custom module ''',

    'depends': ['sale_management','stock'],
    'data': [
        'views/saleorder_invoice.xml',
       'views/weight_total.xml',
    ],
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}


