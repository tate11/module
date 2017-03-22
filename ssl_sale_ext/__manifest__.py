# -*- coding: utf-8 -*-
{
    'name': 'SAL: SuperSilicone Sale Extention',
    'version': '1.0',
    'author': 'Kornelius K Macario (Falinwa Indonesia)',
    'description': '''
        Module to extend reporting file in Quotations.
    ''',
    'depends': [
        'ssl_base_ext',
    ],
    'data': [
        'report/ssl_sale_ext_report.xml',
        'report/wishlist_report.xml',
        'views/sale_view.xml',
        'views/partner_view.xml',
        'views/crm_lead_view.xml',
        'views/wishlist_number.xml',
    ],
    'css': [],
    'js': [],
    'installable': True,
    'active': False,
    'application': False,
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
