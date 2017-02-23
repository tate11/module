# -*- coding: utf-8 -*-
from odoo import fields, models, api, _
import odoo.addons.decimal_precision as dp
import time


class account_invoice(models.Model):
    _name = 'account.invoice'
    _inherit = 'account.invoice'

    @api.multi
    @api.depends('account.move.line')
    def _get_payment_ids_fal(self):
        result = {}
        for move in self:
            result[move.invoice_id.id] = True
        return result.keys()

    @api.multi
    def _get_effective_payment_dates(self):
        result = {}
        for invoice in self:
            temp = []
            for payment in invoice.payment_ids:
                temp.append(payment.payment_date)
            result[invoice.id] = ";".join(temp)
        return result

    fal_risk_level = fields.Integer(
        string='Risk Level',
        size=1,
        help="Risk Level define in number 1 - 9"
    )
    fal_risk_level_name = fields.Char(
        'Risk Level Name',
        size=64,
        help="Risk Level Name"
    )
    fal_effective_payment_dates = fields.Char(
        compute='_get_effective_payment_dates',
        string='Effective Payment Dates',
        help="The efective payment dates.",
        store=True
    )
    fal_use_late_payment_statement = fields.Boolean(
        'Use late payment statement'
    )
    fal_company_code = fields.Many2one(
        'company_id.code',
        string='Company Code'
    )

# end of account_invoice()


class account_bank_statement(models.Model):
    _name = 'account.bank.statement'
    _inherit = 'account.bank.statement'

    fal_description = fields.Text('Description')
    fal_remark = fields.Text('Remark')

# end of account_bank_statement()


class account_bank_statement_line(models.Model):
    _name = 'account.bank.statement.line'
    _inherit = 'account.bank.statement.line'

    ref = fields.Char('Reference', size=64)

# end of account_bank_statement_line()


class account_analytic_account(models.Model):
    _name = 'account.analytic.account'
    _inherit = 'account.analytic.account'

    description = fields.Text('Description')


    @api.multi
    def project_create(self, analytic_account_id):
        '''
        Give Classic project a check when this called
        '''
        res = super(account_analytic_account, self).project_create(analytic_account_id)
        if res:
            project_pool = self.env['project.project']
            project_pool.write(res, {'classic_project': True})
            return res
        return False

# end of account_analytic_account()
