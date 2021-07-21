{
    'name': 'Account Invoice Approvals',
    'version': '13.0.1.0.0',
    'author': 'OasisConsultora',
    'maintainer': 'OasisConsultora',
    'website': 'oasisconsultora.com',
    'license': 'AGPL-3',
    'depends': ['account', 'approvals'],
    'data': [
        'views/approval_fields_extend.xml',
        'views/account_move_approvals.xml',
        ],
    'installable': True,
    'auto_install': False,
    'application': False,
}
