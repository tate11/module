from odoo import models, fields, api
from odoo.tools import amount_to_text


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    def _default_no_deposit(self):
        return self.env.ref('fal_sale_deposit_term.no_deposit').id

    fal_deposit_term_id = fields.Many2one(
        default=lambda self: self._default_no_deposit()
    )
    fal_margin_percentage = fields.Float(
        compute='_compute_margin_percent',
        string='Margin (%)'
    )
    fal_port_departure = fields.Char(string="Port of Departure")
    fal_port_destination = fields.Char(string="Port of Destination")

    @api.onchange('partner_id')
    def onchange_partner_id(self):
        res = super(SaleOrder, self).onchange_partner_id()
        if self.partner_id:
            self.payment_term_id = self.partner_id.fal_payment_term_id
            self.incoterm = self.partner_id.fal_incoterm_id
        return res

    @api.depends('margin', 'amount_untaxed')
    def _compute_margin_percent(self):
        for order in self:
            if order.amount_untaxed:
                order.fal_margin_percentage = order.margin / order.\
                    amount_untaxed * 100.0

    @api.multi
    def amount_to_text(self, amount, currency='USD'):
        return amount_to_text(amount, currency)


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    @api.onchange('product_uom')
    def product_uom_change(self):
        return super(SaleOrderLine, self).product_uom_change()
