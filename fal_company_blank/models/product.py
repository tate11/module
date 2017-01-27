# -*- coding: utf-8 -*-
from odoo import fields, models, api, _


class product_template(models.Model):
    _name = "product.template"
    _inherit = "product.template"

    company_id = fields.Many2one(default=False)
# end of product_template()
