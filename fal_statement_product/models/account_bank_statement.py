# -*- coding: utf-8 -*-
from odoo import fields, models, api, _


class account_bank_statement_line(models.Model):
    _name = 'account.bank.statement.line'
    _inherit = 'account.bank.statement.line'

    product_id = fields.Many2one('product.product', 'Product')


    @api.onchange('product_id')
    def onchange_product_id(self):
        val = {'name': '', 'account_id' : False}
        if self.product_id:
            product = self.env['product.product']
            val['name'] = product.description or product.name
            if product.categ_id.property_account_general_id:
                val['account_id'] = product.categ_id.property_account_general_id or False
            if product.property_account_general_id:
                val['account_id'] = product.property_account_general_id or False
        return {'value': val}

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
