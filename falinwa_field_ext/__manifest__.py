# -*- coding: utf-8 -*-
{
    "name": "Falinwa Field Extends Module",
    "version": "1.0",
    'author': 'Falinwa Hans',
    "description": """
    Module to add additional field for falinwa
    """,
    "depends": [
        'base',
        'account',
        'analytic',
        'project',
        'hr_timesheet',
        'hr_timesheet_sheet',
    ],
    'init_xml': [],
    'update_xml': [
        'views/account_view.xml',
        'views/project_view.xml',
        'views/fal_account_invoice.xml',
        # 'views/hr_view.xml',
    ],
    'css': [],
    'js': [],
    'installable': True,
    'active': False,
    'application': False,
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
