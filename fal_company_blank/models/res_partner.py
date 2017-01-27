# -*- coding: utf-8 -*-
from odoo import fields, models, api, _


class res_partner(models.Model):
    _name = "res.partner"
    _inherit = "res.partner"

    company_id = fields.Many2one(default=False)

# end of res_partner()
