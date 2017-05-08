from odoo import models, fields, api
from odoo.tools import amount_to_text

import logging

_logger = logging.getLogger(__name__)


class CustomInvoice(models.Model):
    _inherit = 'account.invoice'

    fal_port_departure = fields.Char(string="Port of Departure")
    fal_port_destination = fields.Char(string="Port of Destination")
    fal_partner_request_date = fields.Datetime(string="Vendor Request Date")
    fal_client_order_ref = fields.Char(string='Customer Reference')
    fal_incoterm_id = fields.Many2one(
        'stock.incoterms',
        string='Incoterm'
    )
    fal_eco_source = fields.Char(string='ECO Customer Ref.')
    fal_company_code = fields.Char(
        related='company_id.fal_code',
        string='Company Code'
    )

    @api.multi
    def amount_to_text(self, amount, currency='USD'):
        return amount_to_text(amount, currency)


class AccountInvoiceLine(models.Model):
    _inherit = 'account.invoice.line'

    fal_old_ref = fields.Char(
        string='Old Ref.',
        compute='get_old_ref',
    )
    fal_pcs_unit = fields.Float(
        string='Pcs per Unit',
        default=0.0
    )
    fal_price_pcs = fields.Float(
        string='Price per Pcs',
        compute='get_fal_price_pcs'
    )
    fal_sale_id = fields.Many2one(
        'sale.order',
        compute='get_fal_sale_line',
        string='Sale Source',
    )

    @api.depends(
        'sale_line_ids',
        'sale_line_ids.order_id',
    )
    def get_fal_sale_line(self):
        for line in self:
            for order_line in line.sale_line_ids:
                if order_line.order_id:
                    line.fal_sale_id = order_line.order_id
                    break

    @api.depends(
        'price_unit',
        'fal_pcs_unit',
    )
    def get_fal_price_pcs(self):
        for line in self:
            if line.fal_pcs_unit == 0.0:
                line.fal_price_pcs = 0.0
            else:
                line.fal_price_pcs = line.price_unit / line.fal_pcs_unit

    @api.depends(
        'product_id', 'product_id.product_tmpl_id',
        'product_id.product_tmpl_id.fal_old_ref')
    def get_old_ref(self):
        for line in self:
            line.fal_old_ref = line.product_id.product_tmpl_id.fal_old_ref

    @api.multi
    def show_bom_structure(self):
        for line in self:
            return line.product_id.product_tmpl_id.get_bom_structure()
