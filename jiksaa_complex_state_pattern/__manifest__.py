# -*- coding: utf-8 -*-
{
    'name': "Complex State Design Pattern",

    'summary': """This module shows example of State design pattern usage""",

    'description': """This module shows example of State design pattern usage""",

    'author': "Jiksaa",
    'website': "http://www.github.com/jiksaa",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/12.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Design Patterns',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'mail'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/views.xml',
        'data/counter_states.xml',
    ],
    # only loaded in demonstration mode
    'demo': [],
    'pre_init_hook': 'pre_init'
}