# -*- coding: utf-8 -*-
from odoo import models, fields


class ResPartner(models.Model):
    _inherit = "res.partner"

    fal_parent_company = fields.Many2one(
        'res.partner',
        string='Parent Company'
    )

    voucher_ids = fields.One2many(
        'account.voucher', 'partner_id',
        string='Voucher',
        readonly=True
    )

    purchase_order_ids = fields.One2many(
        'purchase.order', 'partner_id',
        string='Purchase Order'
    )

# End of ResPartner()
