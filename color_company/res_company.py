# -*- coding: utf-8 -*-
from odoo import fields, models, api, _


class res_company(models.Model):
    _name = "res.company"
    _inherit = "res.company"

    color = fields.Selection([
        ('aliceblue', 'aliceblue'),
        ('antiquewhite', 'antiquewhite'),
        ('aqua', 'aqua'),
        ('bisque', 'bisque'),
        ('cornsilk', 'cornsilk'),
        ('lightblue', 'lightblue'),
        ('white', 'white')], string='Color'
    )

# end of res_company()
