from odoo import fields, models, api, _
import odoo.addons.decimal_precision as dp


class account_invoice(models.Model):
    _name = "account.invoice"
    _inherit = "account.invoice"

    def _amount_line_tax(self, line):
        val = 0.0
        rate_ids = self.env['res.currency'].search([('name', '=', 'HKD')], limit=1)
        taxes_ids = [x.id for x in line.tax_id]
        tax_line = self.env['account.tax'].browse(taxes_ids)
        for c in tax_line.compute_all(line.price_unit, rate_ids[0], line.product_uom_qty, line.product_id, line.order_id.partner_id)['taxes']:
            val += c.get('amount', 0.0)
        return val

    def _get_invoice_line_fal(self):
        result = {}
        for line in self.env['account.invoice.line'].browse():
            result[line.invoice_id.id] = True
        return result.keys()

    def _get_invoice_tax_fal(self):
        result = {}
        for tax in self.env['account.invoice.tax'].browse():
            result[tax.invoice_id.id] = True
        return result.keys()

    @api.one
    @api.depends(
        'invoice_line_ids.price_subtotal',
        'tax_line_ids.amount',
        'currency_id',
        'date_invoice'
    )
    def _amount_all_hkd(self):
        cur_obj = self.env['res.currency']
        res = {}
        self.amount_untaxed = sum(line.price_subtotal for line in self.invoice_line_ids)
        self.amount_tax = sum(line.amount for line in self.tax_line_ids)
        self.amount_total = self.amount_untaxed + self.amount_tax
        k = 0.0
        for invoice in self.currency_id.with_context(date=self.date_invoice):
            rate_ids = cur_obj.search([('name', '=', 'HKD')], limit=1)
            if self.currency_id != rate_ids:
                k = self.currency_id.compute(self.amount_total, self.currency_id)
            else:
                k = self.amount_total
            self.amount_total_hkd = k

    @api.one
    @api.depends(
        'invoice_line_ids.price_subtotal',
        'tax_line_ids.amount',
        'currency_id',
        'date_invoice'
    )
    def _amount_untaxed_hkd(self):
        cur_obj = self.env['res.currency']
        res = {}
        self.amount_untaxed = sum(line.price_subtotal for line in self.invoice_line_ids)
        self.amount_tax = sum(line.amount for line in self.tax_line_ids)
        self.amount_total = self.amount_untaxed + self.amount_tax
        k = 0.0
        for invoice in self.currency_id.with_context(date=self.date_invoice):
            rate_ids = cur_obj.search([('name', '=', 'HKD')], limit=1)
            if self.currency_id != rate_ids:
                k = self.currency_id.compute(self.amount_untaxed, self.currency_id)
            else:
                k = self.amount_untaxed
            self.untaxed_amount_hkd = k

    @api.one
    @api.depends(
        'currency_id',
        'invoice_line_ids.price_subtotal'
    )
    def _amount_ballance_hkd(self):
        """Function of the field residua. It computes the residual amount (balance) for each invoice"""
        context = dict(self._context)
        ctx = context.copy()
        result = {}
        currency_obj = self.env['res.currency']
        rate_ids = currency_obj.search([('name', '=', 'HKD')], limit=1)
        for invoice in self:
            temp = invoice.residual
            cur = invoice.currency_id
            for rate_id in currency_obj.browse(rate_ids):
                if cur != rate_id:
                    temp = self.currency_id.compute(self.residual, self.currency_id)
                else:
                    temp = self.residual
        invoice.amount_ballance_hkd = temp

    untaxed_amount_hkd = fields.Float(
        compute='_amount_untaxed_hkd',
        string='Subtotal (HKD)',
        track_visibility='always',
        store=True
    )
    amount_total_hkd = fields.Float(
        compute='_amount_all_hkd',
        string='Total (HKD)',
        help="The total amount in HKD.",
        store=True
    )
    amount_ballance_hkd = fields.Float(
        compute='_amount_ballance_hkd',
        string='Balance (HKD)',
        help="The balance amount in HKD."
    )

# end of account_invoice()


class account_move_line(models.Model):
    _name = 'account.move.line'
    _inherit = 'account.move.line'

    @api.multi
    def _amount_all_to_hk(self):
        currency_pool = self.env['res.currency']
        rs_data = {}
        for line in self:
            context = dict(self._context)
            ctx = context.copy()
            ctx.update({'date': line.date})
            res = {}
            res['fal_debit_hk'] = 0.0
            res['fal_credit_hk'] = 0.0
            rate_ids = currency_pool.search([('name', '=', 'HKD')], limit=1)
            for rate_id in currency_pool.browse(rate_ids):
                rate_hk = rate_id
                origin_currency = line.journal_id.company_id.currency_id
                if origin_currency == rate_id:
                    res['fal_debit_hk'] = abs(line.debit)
                    res['fal_credit_hk'] = abs(line.credit)
                else:
                    # always use the amount booked in the company currency as the basis of the conversion into the voucher currency
                    res['fal_debit_hk'] = currency_pool.compute(origin_currency.id, rate_hk.id, abs(line.debit))
                    res['fal_credit_hk'] = currency_pool.compute(origin_currency.id, rate_hk.id, abs(line.credit))

                rs_data[line.id] = res
        return rs_data

    fal_debit_hk = fields.Float(
        compute='_amount_all_to_hk',
        string='Debit (HKD)',
        help="Debit in HKD."
    )
    fal_credit_hk = fields.Float(
        compute='_amount_all_to_hk',
        string='Credit (HKD)',
        help="Credit in HKD."
    )

# end of account_move_line()
