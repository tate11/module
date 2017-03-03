# -*- coding: utf-8 -*-
from odoo import fields, models


class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    commercial_partner_id = fields.Many2one(
        'res.partner',
        related='partner_id.commercial_partner_id',
        string='Commercial Entity',
        help='The commercial entity that will be used \
                on Journal Entries for this invoice',
        readonly=True,
        store=True
    )

    fal_parent_company = fields.Many2one(
        'res.partner',
        related='partner_id.fal_parent_company',
        string='Parent Company',
        help='The Parent Company for group',
        readonly=True,
        store=True
    )

# End of PurchaseOrder()
