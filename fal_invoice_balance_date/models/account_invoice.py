from odoo import models, fields, api, exceptions, _

import openerp.addons.decimal_precision as dp
import time


class account_invoice(models.Model):
    _name = "account.invoice"
    _inherit = "account.invoice"

    def _amount_balance_date(self):
        """Function of the field residual. It computes the residual amount (balance) for each invoice"""
        context = dict(self._context)
        ctx = context.copy()
        result = {}
        currency_obj = self.env['res.currency']
        for invoice in self:
            amount_paids = 0.00
            for payment in invoice.payment_ids:
                if context.get('wizard_data_date',False) and payment.payment_date <= context.get('wizard_data_date',False):
                    ctx['date'] = payment.payment_date
                    ctx['check_move_validity'] = False
                    aml_obj = self.pool.get('account.move.line')
                    debit, credit, amount_currency, currency_id = aml_obj.compute_amount_fields(payment.amount, payment.currency_id, payment.company_id.currency_id, context=ctx)
                    amount_paid = 0.00
                    if invoice.type in ['out_invoice','in_refund']:
                        amount_paid = credit
                    else:
                        amount_paid = debit
                    if payment.currency_id and payment.currency_id.id == invoice.currency_id.id:
                        amount_paid = abs(amount_currency)
                    else:
                        amount_paid = currency_obj.compute(payment.company_id.currency_id.id, invoice.currency_id.id, amount_paid, context=ctx)
                    amount_paids += amount_paid
            #prevent the residual amount on the invoice to be less than 0
            result[invoice.id] = max(invoice.amount_total - amount_paids, 0.00)
        return result

    def _balance_date_search(self, obj, name, args):
        context = dict(self._context)
        ctx = context.copy()
        invoice_ids = self.search([('date', '<=', context.get('wizard_data_date')), ('state', 'not in', ['draft', 'cancel'])])
        currency_obj = self.env['res.currency']
        temp = []
        for invoice in self.browse(invoice_ids):
            amount_paids = 0
            for payment in invoice.payment_ids:
                if context.get('wizard_data_date',False) and payment.payment_date <= context.get('wizard_data_date',False):
                    ctx['date'] = payment.payment_date
                    ctx['check_move_validity'] = False
                    aml_obj = self.pool.get('account.move.line')
                    debit, credit, amount_currency, currency_id = aml_obj.compute_amount_fields(payment.amount, payment.currency_id, payment.company_id.currency_id, context=ctx)
                    amount_paid = 0
                    if invoice.type in ['out_invoice', 'in_refund']:
                        amount_paid = credit
                    else:
                        amount_paid = debit
                    if payment.currency_id and payment.currency_id.id == invoice.currency_id.id:
                        amount_paid = abs(amount_currency)
                    else:
                        amount_paid = currency_obj.compute(payment.company_id.currency_id.id, invoice.currency_id.id, amount_paid, context=ctx)
                    amount_paids += amount_paid
            if max(invoice.amount_total - amount_paids, 0.0) > 0.00:
                temp.append(invoice.id)
        return [('id', 'in', temp)]

    amount_balance_date = fields.Float(
        compute='_amount_balance_date',
        string='Balance on Date',
        store=False,
        help="The balance amount based on date."
    )

# end of account_invoice()
