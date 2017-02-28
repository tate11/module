# -*- coding: utf-8 -*-
from odoo import api, fields, models


class purchase_order(models.Model):
    _inherit = "purchase.order"

    fal_partner_contact_person_id = fields.Many2one(
        'res.partner',
        'Contact Person'
    )
    fal_user_id = fields.Many2one(
        'res.users',
        'Purchases Person',
        select=True,
        track_visibility='onchange'
    )

    @api.multi
    def onchange_partner_id(self, part):
        res = super(purchase_order, self).\
            onchange_partner_id(part)
        partner = self.env['res.partner'].\
            browse(part)
        res['value']['fal_partner_contact_person_id'] =\
            partner.child_ids and partner.child_ids[0].id or False
        return res

# end of purchase_order()
