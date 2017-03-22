from odoo import models, fields


class ResPartner(models.Model):
    _inherit = 'res.partner'

    fal_payment_term_id = fields.Many2one(
        'account.payment.term', string='Payment Term'
    )

    fal_incoterm_id = fields.Many2one(
        'stock.incoterms', string='Incoterm'
    )
