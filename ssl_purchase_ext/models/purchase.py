from odoo import models, fields, api
from odoo.tools import amount_to_text


class CustomPurchase(models.Model):
    _inherit = 'purchase.order'

    fal_port_departure = fields.Char(string="Port of Departure")
    fal_port_destination = fields.Char(string="Port of Destination")
    fal_deposit_term_id = fields.Many2one(
        'fal.deposit.term', string='Deposit Term'
    )
    fal_payment_mean_id = fields.Many2one(
        'fal.payment.mean', string='Payment Mean')
    fal_sale_user_id = fields.Many2one(
        'res.users', string='Sale Order Responsible')
    fal_easy_sale_order = fields.Char(
        string='Sale Order',
        compute='get_ef_sale_order_name'
    )
    fal_easy_sale_client_ref = fields.Char(
        string='Sale Order Client Ref')
    fal_company_code = fields.Char(
        related='company_id.fal_code',
        string='Company Code'
    )

    @api.multi
    def amount_to_text(self, amount, currency='USD'):
        return amount_to_text(amount, currency)

    @api.model
    def _prepare_sale_order_data(
            self, name, partner, company, direct_delivery_address):
        res = super(CustomPurchase, self)._prepare_sale_order_data(
            name, partner, company, direct_delivery_address
        )
        if res:
            res[0].update({
                'payment_term_id': self.payment_term_id.id,
                'incoterm': self.incoterm_id.id,
                'fal_payment_mean_id': self.fal_payment_mean_id.id,
                'fal_deposit_term_id': self.fal_deposit_term_id.id,
                'fal_port_departure': self.fal_port_departure,
                'fal_port_destination': self.fal_port_destination,
                'fal_easy_sale_order': self.fal_easy_sale_order,
                'fal_easy_sale_client_ref': self.fal_easy_sale_client_ref,
            })
        return res

    @api.model
    def _prepare_sale_order_line_data(self, line, company, sale_id):
        res = super(CustomPurchase, self)._prepare_sale_order_line_data(
            line, company, sale_id)
        if res:
            res.update({
                'name': line.name or line.product_id.name,
                'fal_pcs_unit': line.fal_pcs_unit,
            })
        return res

    @api.depends('origin')
    def get_ef_sale_order_name(self):
        for purc in self:
            if purc.company_id.fal_code == 'E' and 'ECO' in purc.origin:
                origin = purc.origin
                name = origin.split(':')
                if name:
                    purc.fal_easy_sale_order = name[0]

    @api.multi
    def button_confirm(self):
        res = super(CustomPurchase, self).button_confirm()
        for pur in self:
            for line in pur.order_line:
                for proc in line.procurement_ids:
                    proc_sale = proc.group_id.procurement_ids.filtered(
                        lambda r: r.sale_line_id
                    )
                    if proc_sale:
                        sale = proc_sale[0].sale_line_id.order_id
                        sale.write({'fal_purchase_doc': pur.name})
                        return res
        return res

    def _prepare_invoice_line_from_po_line(self, line):
        invoice = super(CustomPurchase, self)._prepare_invoice_line_from_po_line(line)
        if self.fal_easy_sale_client_ref:
            invoice['fal_eco_source'] = self.fal_easy_sale_client_ref
        return invoice


class PurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'

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
