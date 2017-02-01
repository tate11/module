# -*- coding: utf-8 -*-
{
    "name": "Timesheet Invoice Ext",
    "version": "1.0",
    "author": "Falinwa Limited (Hans Yonathan)",
    "description": """
    Module to add feature to have timesheet line invoiceable.
    """,
    "summary": '-',
    "depends": [
        'base',
        'hr',
        'hr_timesheet',
        'hr_timesheet_sheet',
        'sale_timesheet',
    ],
    'init_xml': [],
    'data': [
        'wizard/hr_timesheet_invoice_create_view.xml',
        'security/ir.model.access.csv',
        'views/hr_view.xml',
    ],
    'css': [],
    'js': [],
    'installable': True,
    'active': False,
    'application': False,
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
