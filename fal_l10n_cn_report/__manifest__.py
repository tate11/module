# -*- coding: utf-8 -*-
{
    "name": "ACC: Falinwa China Report",
    "version": "1.0",
    'author': 'Falinwa Hans',
    "description": """
    Module to developed Falinwa China reporting.
    """,
    "depends": ['account', 'fal_l10n_cn', 'account_reports'],
    'init_xml': [],
    'data': [
    ],
    'update_xml': [
        'wizard/fal_journal_entry_report_wizard_view.xml',
        'views/account_financial_report_data.xml',
        'views/account_financial_report_view.xml',
    ],
    'css': [],
    'js': [
    ],
    'qweb': [],
    'installable': True,
    'active': False,
    'application': False,
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
