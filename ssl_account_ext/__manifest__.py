# -*- coding: utf-8 -*-
{
    'name': 'SuperSilicone Account Extention',
    'version': '1.0',
    'author': 'Falinwa Indonesia',
    'description': '''
        Module to extend reporting file in Customer Invoice.
    ''',
    'depends': [
        'ssl_base_ext',
    ],
    'data': [
        'report/report.xml',
        'views/account_ext_view.xml'
    ],
    'css': [],
    'js': [],
    'installable': True,
    'active': False,
    'application': False,
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
