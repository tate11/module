# -*- coding: utf-8 -*-
from odoo import fields, models, api, _


class account_bank_statement_line(models.Model):
    _name = 'account.bank.statement.line'
    _inherit = 'account.bank.statement.line'

    product_id = fields.Many2one('product.product', 'Product')

    @api.onchange('product_id')
    def _onchange_product_id(self):
        if self.product_id:
            if not self.name:
                self.name = self.product_id.display_name or ''
            self.unit_amount = self.product_id.\
                price_compute('standard_price')[self.product_id.id]
            self.product_uom_id = self.product_id.uom_id
            self.tax_ids = self.product_id.supplier_taxes_id
            account = self.product_id.\
                product_tmpl_id._get_product_accounts()['expense']
            if account:
                self.account_id = account

# end of account_bank_statement_line()


class product_category(models.Model):
    _name = 'product.category'
    _inherit = 'product.category'

    property_account_general_id = fields.Many2one(
        'account.account',
        string="General Account",
        help="This account will be used for statement\
        instead of the default one to value for the current product."
    )

# end of product_category()


class product_template(models.Model):
    _name = 'product.template'
    _inherit = 'product.template'

    property_account_general_id = fields.Many2one(
        'account.account',
        string="General Account",
        help="This account will be used for statement\
        instead of the default one to value for the current product."
    )

# end of product_product()
