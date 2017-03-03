# -*- coding: utf-8 -*-
from odoo import fields, models


class AccountInvoice(models.Model):
    _inherit = "account.invoice"

    fal_parent_company = fields.Many2one(
        'res.partner',
        related='partner_id.fal_parent_company',
        string='Parent Company',
        help='The Parent Company for group',
        readonly=True,
        store=True
    )

# End of AccountInvoice()
