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
    fal_purchase_doc = fields.Char(string='Purchase Order')
    fal_company_code = fields.Char(
        related='company_id.fal_code',
        string='Company Code'
    )
    fal_easy_sale_order = fields.Char(
        string='Source ECO'
    )
    fal_easy_sale_client_ref = fields.Char(
        string='ECO Client Ref')

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

    def _prepare_invoice(self):
        """
        copy additional data from sale order to invoice
        """
        invoice = super(SaleOrder, self)._prepare_invoice()
        if self.fal_port_departure:
            invoice['fal_port_departure'] = self.fal_port_departure
        if self.fal_port_destination:
            invoice['fal_port_destination'] = self.fal_port_destination
        if self.client_order_ref:
            invoice['fal_client_order_ref'] = self.client_order_ref
        if self.incoterm:
            invoice['fal_incoterm_id'] = self.incoterm.id
        if self.fal_easy_sale_client_ref:
            invoice['fal_eco_source'] = self.fal_easy_sale_client_ref
        return invoice


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

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

    @api.depends(
        'product_id', 'product_id.product_tmpl_id',
        'product_id.product_tmpl_id.fal_old_ref')
    def get_old_ref(self):
        for line in self:
            line.fal_old_ref = line.product_id.product_tmpl_id.fal_old_ref

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

    @api.multi
    def _prepare_invoice_line(self, qty):
        self.ensure_one()
        res = super(SaleOrderLine, self)._prepare_invoice_line(qty)
        if self.fal_pcs_unit:
            res['fal_pcs_unit'] = self.fal_pcs_unit
        return res

    @api.onchange('product_uom')
    def product_uom_change(self):
        return super(SaleOrderLine, self).product_uom_change()

    @api.multi
    def _prepare_order_line_procurement(self, group_id=False):
        res = super(SaleOrderLine, self)._prepare_order_line_procurement(
            group_id=group_id)
        suppliers = self.product_id.seller_ids.filtered(
            lambda r: not r.product_id or r.product_id == self.product_id)
        if suppliers:
            supplier = suppliers[0]
            partner = supplier.name
            if partner.fal_ssl_company:
                res['fal_port_departure'] = self.order_id.fal_port_departure
                res['fal_port_destination'] = self.order_id.\
                    fal_port_destination
                res['fal_payment_term_id'] = self.order_id.payment_term_id.id
                res['fal_deposit_term_id'] = self.order_id.\
                    fal_deposit_term_id.id
                res['fal_payment_mean_id'] = self.order_id.\
                    fal_payment_mean_id.id
                res['fal_incoterm_id'] = self.order_id.incoterm.id
                res['fal_sale_user_id'] = self.order_id.user_id.id
                res['fal_sale_line_name'] = self.name
                res['fal_sale_note'] = self.order_id.note
                res['fal_easy_sale_client_ref'] = self.order_id.\
                    client_order_ref
                res['fal_pcs_unit'] = self.fal_pcs_unit
        return res

    @api.multi
    def show_bom_structure(self):
        for line in self:
            return line.product_id.product_tmpl_id.get_bom_structure()
