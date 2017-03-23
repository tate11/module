# -*- coding: utf-8 -*-
{
    'name': 'PUR: SuperSilicone Purchase Extention',
    'version': '1.0',
    'author': 'Kornelius K Macario (Falinwa Indonesia)',
    'description': '''
        Module to extend reporting file in Purchase Order.
    ''',
    'depends': [
        'ssl_base_ext',
    ],
    'data': [
        # 'report/ssl_purchase_ext_report.xml',
        'report/purchase_report.xml',
        'views/purchase_ext_view.xml',
    ],
    'css': [],
    'js': [],
    'installable': True,
    'active': False,
    'application': False,
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
