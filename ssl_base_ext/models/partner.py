from odoo import fields, models


class resPartner(models.Model):
    _inherit = 'res.partner'

    fal_related_company_ids = fields.One2many(
        'res.company',
        'partner_id',
        string='Related Company'
    )
