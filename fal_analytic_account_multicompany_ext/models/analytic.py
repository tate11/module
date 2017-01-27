# -*- coding: utf-8 -*-
from odoo import fields, models, api
from openerp.tools.translate import _


class AccountAnalytic(models.Model):
    _inherit = "account.analytic.account"

    company_id = fields.Many2one(required=False, default=False)
