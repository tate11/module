from odoo import fields, models, api, _

import openerp.addons.decimal_precision as dp
from openerp.tools import DEFAULT_SERVER_DATE_FORMAT, DEFAULT_SERVER_DATETIME_FORMAT, DATETIME_FORMATS_MAP, float_compare
import time


class bank_balance_computation_wizard(models.TransientModel):
    _name = "bank.balance.computation.wizard"
    _description = "Bank Balance Computation Wizard"

    state = fields.Selection([
        ('draft', 'Draft'),
        ('done', 'Done')],
        'Done', required=True,
        default='draft')
    date_start = fields.Date('Start Date')
    date_stop = fields.Date('End Date')
    target_moves = fields.Selection([
        ('posted', 'All Posted Entries'),
        ('all', 'All Entries')],
        'Target Moves', required=True,
        default='posted')
    temp = fields.One2many(
        'bank.balances.line',
        'wizard_id',
        'Temp', readonly=True)

    @api.multi
    def _check_duration(self):
        obj_fy = self.browse()
        if obj_fy.date_stop < obj_fy.date_start:
            return False
        return True

    _constraints = [
        (_check_duration,
            'Error!\nThe start date of a fiscal year must precede its end date.',
            ['date_start', 'date_stop'])
    ]

    @api.multi
    def _get_default_temp(
        self,
        target_moves='posted',
        date_start=False,
        date_stop=False
    ):
        account_obj = self.env['account.account']
        journal_item_obj = self.env['account.move.line']
        bank_account_ids = account_obj.search([
            ('user_type_id.name', '=', 'Bank and Cash')])
        temp = []
        args = []
        if date_start and date_stop:
            args.append(('date', '>=', date_start))
            args.append(('date', '<=', date_stop))
        if target_moves == 'posted':
            args.append(('move_id.state', '=', target_moves))
        for bank_account_id in account_obj.browse(bank_account_ids):
            journal_item_ids = journal_item_obj.search([
                ('account_id', '=', bank_account_id.id)] + args)
            balance_ccr = balance_bcr = 0.00
            for journal_item_id in journal_item_obj.browse(journal_item_ids):
                if journal_item_id.credit:
                    balance_ccr -= journal_item_id.credit
                else:
                    balance_ccr += journal_item_id.debit
                if bank_account_id.currency_id.id:
                    balance_bcr += journal_item_id.amount_currency
                else:
                    if journal_item_id.credit:
                        balance_bcr -= journal_item_id.credit
                    else:
                        balance_bcr += journal_item_id.debit
            temp.append((0, 0, {
                'bank_name_id': bank_account_id.id,
                'balance_in_company_currency': balance_ccr,
                'company_currency_id': bank_account_id.company_id.currency_id.id,
                'balance_in_bank_currency': balance_bcr,
                'bank_currency_id': bank_account_id.currency_id and bank_account_id.currency_id.id or bank_account_id.company_id.currency_id.id,
                'bank_currency_id': bank_account_id.currency_id and bank_account_id.currency_id.id or bank_account_id.company_id.currency_id.id,
            }))
        return temp

    _defaults = {
        'temp': _get_default_temp,
    }

    @api.multi
    def filter_bank_balance(self):
        data_wizard = self.browse()[0]
        account_obj = self.env['account.account']
        journal_item_obj = self.env['account.move.line']

        # get temp
        temp = self._get_default_temp(
            target_moves=data_wizard.target_moves,
            date_start=data_wizard.date_start,
            date_stop=data_wizard.date_stop
        )

        temp_del = []
        # delete all
        for temp_id in self.browse()[0].temp:
            temp_del.append((2, temp_id.id))
        self.write({'temp': temp_del})

        # generate new
        self.write({
            'temp': temp,
            'state': 'done',
        })

        return {
            'type': 'ir.actions.act_window',
            'name': "Bank Balance",
            'res_model': 'bank.balance.computation.wizard',
            # 'res_id': ids[0],
            'view_type': 'form',
            'view_mode': 'form',
            'target': 'new',
            'nodestroy': True,
        }

# end of bank_balance_computation_wizard()


class bank_balances_line(models.TransientModel):
    _name = "bank.balances.line"
    _description = "Bank Balances Line"

    wizard_id = fields.Many2one('bank.balance.computation.wizard', 'Wizard')
    bank_name_id = fields.Many2one('account.account', 'Bank Name')
    balance_in_company_currency = fields.Float('Balance (CCR)')
    company_currency_id = fields.Many2one('res.currency', 'Company Currency')
    balance_in_bank_currency = fields.Float('Balance (BCR)')
    bank_currency_id = fields.Many2one('res.currency', 'Bank Currency')


# end of bank_balances_line()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
