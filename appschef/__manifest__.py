# -*- coding: utf-8 -*-
{
    'name': "appschef",

    'summary': "Short (1 phrase/line) summary of the module's purpose",

    'description': """
Long description of module's purpose
    """,

    'author': "My Company",
    'website': "https://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','sale'],

    # always loaded
    'data': [
        'security/groups.xml',
        'security/ir.model.access.csv',
        'views/appschef_employee.xml',
        'views/appschef_project.xml',
        'wizard/commission_rule_wizard.xml',
        'views/appschef_commission_rule.xml',
        'views/appschef_history_commission.xml',
        'views/appschef_daily_report.xml',
        'views/appschef_menu.xml',
        'views/sale_order_views.xml'
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}

