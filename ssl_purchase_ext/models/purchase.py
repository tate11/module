from odoo import models, fields, api
from odoo.tools import amount_to_text


class CustomPurchase(models.Model):
    _inherit = 'purchase.order'

    fal_port_departure = fields.Char(string="Port of Departure")
    fal_port_destination = fields.Char(string="Port of Destination")

    @api.multi
    def amount_to_text(self, amount, currency='USD'):
        return amount_to_text(amount, currency)
