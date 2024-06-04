# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Product Discount Limit on Sales & Invoice',
    'version': '17.0.0.0',
    'category': 'Sales',
    'summary': 'Sale order Product Discount Limitation invoice Product Discount Limitation sales discount limit invoice discount limit sales product discount limit invoice product discount limit product sales discount limitation product invoice discount limitation',
    'description' :"""
    		This odoo app helps user to limit fixed or percentage discount on product for app like sale, purchase and invoice. User have option to select discount type and enter discount amount or percentage, enable or disable warning functionality, and can add warning message for discount limit. On order line while user selects product then added discount will automatically added from selected product and warning will raise with added message if user try to modify or change discount value, It will automatically set to default value if changed.
    		
    		Product discount limit
    		Product discount limit warning
    		Product Discount warning
    		Product discount limit
    		Product fixed discount limit
    		Product percentage discount limit
    		Product fixed discount limit warning
    		Product percentage discount limit warning
    """,
    'author': 'BrowseInfo',
    'website': 'https://www.browseinfo.com',
    "price": 15,
    "currency": 'EUR',
        'depends': ['base','product','sale_management','account'],
    'data': [
        'views/product_view.xml',
        'views/sale_view.xml',
        'views/account_move_view.xml',
        'views/res_config.xml',
    ],
    'demo': [],
    'test': [],
    'installable': True,
    'auto_install': False,
    'live_test_url':'https://youtu.be/R96hpKNBsy4',
    "images":['static/description/Banner.gif'],
    'license': 'OPL-1',
}
