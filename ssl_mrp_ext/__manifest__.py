# -*- coding: utf-8 -*-
{
    'name': 'SuperSilicone MRP Extention',
    'version': '1.0',
    'author': 'Falinwa Indonesia',
    'description': '''
        Module to extend Manufacturing Resource Planning for SuperSilicone.
    ''',
    'depends': [
        'ssl_base_ext',
        'fal_mrp_work_route',
    ],
    'data': [
        'views/mrp_workcenter_view.xml',
        'views/mrp_workorder_view.xml',
    ],
    'css': [],
    'js': [],
    'installable': True,
    'active': False,
    'application': False,
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
