# -*- coding: utf-8 -*-
from odoo import fields, models, api, _
import odoo.addons.decimal_precision as dp


class purchase_order(models.Model):
    _name = "purchase.order"
    _inherit = "purchase.order"

    def _amount_line_tax(self, line):
        val = 0.0
        rate_ids = self.env['res.currency'].search([('name', '=', 'HKD')], limit=1)
        taxes_ids = [x.id for x in line.tax_id]
        tax_line = self.env['account.tax'].browse(taxes_ids)
        for c in tax_line.compute_all(line.price_unit, rate_ids[0], line.product_uom_qty, line.product_id, line.order_id.partner_id)['taxes']:
            val += c.get('amount', 0.0)
        return val

    @api.multi
    def _get_order_fal(self):
        result = {}
        for line in self.env['purchase.order.line'].browse():
            result[line.order_id.id] = True
        return result.keys()

    @api.multi
    def _get_invoice_ids_fal(self):
        invoices = {}
        for invoice_ids in self.env['account.invoice'].browse():
            invoices[invoice_ids.id] = True
        purchase_ids = []
        if invoices:
            purchase_ids = self.env['purchase.order'].search([('invoice_ids', 'in', invoices.keys())])
        return purchase_ids

    @api.one
    @api.depends(
        'order_line.price_total',
        'order_line.invoice_lines',
        'order_line.invoice_lines.invoice_id.state'
    )
    def _total_uninvoice(self):
        for order in self:
            temp = 0.0
            for invoice_id in order.invoice_ids:
                if invoice_id.state not in ('draft', 'cancel'):
                    temp += invoice_id.amount_total
        self.total_uninvoice = order.amount_total - temp

    @api.one
    @api.depends(
        'currency_id',
        'order_line.price_total',
        'order_line.invoice_lines',
        'order_line.invoice_lines.invoice_id.state',
        'date_order'
    )
    def _total_uninvoice_hkd(self):
        cur_obj = self.env['res.currency']
        for order in self:
            rate_ids = cur_obj.search([('name', '=', 'HKD')], limit=1)
            amount = temp = 0.0
            for invoice_id in order.invoice_ids:
                if invoice_id.state not in ('draft', 'cancel'):
                    temp += invoice_id.amount_total
            result = temp
            for invoice in self.currency_id.with_context(date=self.date_order):
                if self.currency_id != rate_ids:
                    amount = self.currency_id.compute(result, self.currency_id)
                else:
                    amount = result
        self.total_uninvoice_hkd = amount

    @api.one
    @api.depends('order_line.price_total')
    def _amount_all_hkd(self):
        cur_obj = self.env['res.currency']
        for order in self:
            amount = 0.0
            rate_ids = cur_obj.search([('name', '=', 'HKD')], limit=1)
            for line in order.order_line:
                amount = line.price_subtotal + line.price_tax
                if order.currency_id != rate_ids:
                    amount_total = order.currency_id.compute(
                        amount,
                        line.currency_id
                    )
                else:
                    amount_total = amount
        self.amount_total_hkd = amount_total

    @api.one
    @api.depends('order_line.price_total')
    def _amount_untaxed_hkd(self):
        cur_obj = self.env['res.currency']
        amount = 0.0
        for order in self:
            rate_ids = cur_obj.search([('name', '=', 'HKD')], limit=1)
            for line in order.order_line:
                amount += line.price_subtotal
                if order.currency_id != rate_ids:
                    amount_total = order.currency_id.compute(
                        amount,
                        line.currency_id
                    )
                else:
                    amount_total = amount
        self.untaxed_amount_hkd = amount_total

    untaxed_amount_hkd = fields.Float(
        compute='_amount_untaxed_hkd',
        string='Untaxed Amount (HKD)',
        help="The untaxed amount in HKD."
    )
    amount_total_hkd = fields.Float(
        compute='_amount_all_hkd',
        string='Total (HKD)',
        help="The total amount in HKD."
    )
    total_uninvoice = fields.Float(
        compute='_total_uninvoice',
        string='Total Uninvoice',
        help="The total uninvoice."
    )
    total_uninvoice_hkd = fields.Float(
        compute='_total_uninvoice_hkd',
        string='Total Uninvoice (HKD)',
        help="The total uninvoice in HKD."
    )

# end of purchase_order()
