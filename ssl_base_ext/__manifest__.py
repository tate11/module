# -*- coding: utf-8 -*-
{
    'name': 'GEN: SuperSilicone Base Module',
    'version': '1.0',
    'author': 'Falinwa Indonesia',
    'description': '''
    This module has features:\n
    1. Generic configuration/function that can be inherited by other \
    specific SuperSilicone modules\n
    2. Provide additional fields for SuperSilicone\n
    3. Be a connector between specific SuperSilicone modules and \
    Falinwa modules\n
    ''',
    'depends': [
        'product',
        'sale',
        'sale_margin',
        'stock',
        'account',
        'fal_product_size_detail',
        'fal_product_old_ref',
        'fal_product_variants_attribute',
        'sale_stock',
        'fal_payment_mean',
        'fal_sale_deposit_term',
        'fal_partner_qualification',
        'fal_crm_wishlist',
        'sale_order_dates',
        'mrp',
        'inter_company_rules',
        'purchase',
        'fal_company_code',
        'fal_sale_order_sequence',
        'contacts',
        'fal_product_template_bom',
        'fal_account_invoice_sequence'
    ],
    'data': [
        'views/partner_view.xml',
        'views/product_view.xml',
        'data/res.company.csv',
    ],
    'css': [],
    'js': [],
    'installable': True,
    'active': False,
    'application': False,
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
