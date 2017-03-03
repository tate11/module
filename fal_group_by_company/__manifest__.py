# -*- coding: utf-8 -*-

{
    'name': 'Group by Company',
    'version': '1.0',
    'author': 'Falinwa Limited',
    'description': '''
        Module to give group by company.
    ''',
    'depends': [
        'sale',
        'purchase',
        'account',
        'account_voucher'
    ],
    'init_xml': [],
    'data': [],
    'update_xml': [
        'views/general_view.xml',
    ],
    'css': [],
    'installable': True,
    'active': False,
    'application': False,
    'js': [],
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
