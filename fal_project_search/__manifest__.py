# -*- coding: utf-8 -*-

{
    'name': 'Project Search',
    'version': '1.0',
    'author': 'Falinwa Limited',
    'description': '''
        Module to add view to search by Project.
    ''',
    'depends': [
        'base',
        'account',
        'account_accountant',
        'sale',
        'purchase',
        'project'
    ],
    'init_xml': [],
    'data': [
    ],
    'update_xml': [
        'views/account_view.xml',
        'views/purchase_view.xml'
    ],
    'css': [],
    'installable': True,
    'active': False,
    'application': False,
    'js': []
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
