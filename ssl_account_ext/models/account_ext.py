from odoo import models, fields, api
from odoo.tools import amount_to_text


class CustomInvoice(models.Model):
    _inherit = 'account.invoice'

    fal_port_departure = fields.Char(string="Port of Departure")
    fal_port_destination = fields.Char(string="Port of Destination")

    @api.multi
    def amount_to_text(self, amount, currency='USD'):
        return amount_to_text(amount, currency)
