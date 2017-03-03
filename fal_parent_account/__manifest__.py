# -*- coding: utf-8 -*-
{
    "name": "Parent Account",
    "version": "1.0",
    'author': 'Falinwa Hans',
    "description": """
    Module to get back the parent account
    """,
    "depends": [
        'account', 'analytic', 'project'
        ],
    'data': [
        'wizard/account_analytic_chart_view.xml',
        'views/account_view.xml',
        'views/project_view.xml',
    ],
    'css': [],
    'js': [],
    'installable': True,
    'active': False,
    'application': False,
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
