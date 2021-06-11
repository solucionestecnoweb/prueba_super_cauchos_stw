{
    'name': 'Sales Report Supercauchos',
    'version': '13.0.1.0.1',
    'category': 'sales',
    'author': 'Oasis Consultora C.A.',
    'license': 'AGPL-3',
    'depends': ['base', 'sale', 'sale_logic_extend'],
    'data': [
        'views/sale_order_budget_view_extend.xml',
        'report/sale_order_budget_extend.xml',
        'report/sale_order_extend.xml',
    ],
    'installable': True,
    'auto_install': False,
    'application': False,
}
