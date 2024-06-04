# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.
{
    'name': 'Sales Commission for Users and Partner',
    'version': '17.0.0.0',
    'description': '''custom module ''',
    'depends': ['base','sale_management' , 'purchase' , 'contacts'],
    'data': [
       'security/ir.model.access.csv',
        'views/user_commission.xml',
        'views/commission_level.xml',
        'views/product_commisiion.xml',
        'views/sale_team.xml',
        'views/product_category.xml',
        'views/partner_commission.xml',
        'views/res_config_settings.xml',
        'views/sale_order.xml',
        'views/purchase_order.xml',
    ],
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}

