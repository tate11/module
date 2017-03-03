# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2010 Tiny SPRL (<http://tiny.be>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from odoo import fields, models, api, _
from odoo.exceptions import UserError


class account_bank_statement(models.Model):
    _inherit = 'account.bank.statement'

    @api.onchange('journal_id')
    def onchange_journal_id(self, statement_id, journal_id):
        if not journal_id:
            return {}
        res = super(account_bank_statement, self).onchange_journal_id(statement_id, journal_id)
        account_id = self.env['account.journal'].read(journal_id, ['default_debit_account_id'])['default_debit_account_id']
        res['value'].update({'account_id': account_id})
        return res

    # Duplicate method with odoo v.9
    # !There is a possibility that this function already implemented in odoo v.9 in function _end_balance()! 
    # Generate Error : TypeError: _end_balance() takes at least 6 arguments (5 given) 
    # Solution : (A) Changing _end_balance name in this file to _fal_end_balance(self, cursor, user, ids, name, attr, context=None)
    def _fal_end_balance(self, cursor, user, ids, name, attr, context=None):
        if context is None:
            context = {}
        res = {}
        res_currency_obj = self.env['res.currency']
        res_users_obj = self.env['res.users']
        company_currency_id = res_users_obj.browse(cursor, user, user).company_id.currency_id.id
        for statement in self:
            res[statement.id] = statement.balance_start
            stmt_currency_id = statement.currency_id.id
            for line in statement.line_ids:
                res[statement.id] += line.amount

            """
            for move_line in statement.move_line_ids:
                if move_line.currency_id.id == stmt_currency_id and move_line.amount_currency != 0:
                    if move_line.debit > 0 and move_line.account_id.id in \
                                [statement.journal_id.default_debit_account_id.id, statement.journal_id.default_credit_account_id.id]:
                        res[statement.id] += move_line.amount_currency
                    else:
                        if move_line.credit > 0 and move_line.account_id.id in \
                                    [statement.journal_id.default_debit_account_id.id, statement.journal_id.default_credit_account_id.id]:
                            res[statement.id] += move_line.amount_currency
                else:
                    ctx = context.copy()
                    ctx.update({'date': move_line.date})
                    if move_line.debit > 0 and move_line.account_id.id in \
                                [statement.journal_id.default_debit_account_id.id, statement.journal_id.default_credit_account_id.id]:
                            res[statement.id] += res_currency_obj.compute(cursor,
                                    user, company_currency_id, stmt_currency_id,
                                    move_line.debit, context=ctx)
                    else:
                        if move_line.credit > 0 and move_line.account_id.id in \
                                [statement.journal_id.default_debit_account_id.id, statement.journal_id.default_credit_account_id.id]:
                            res[statement.id] -= res_currency_obj.compute(cursor,
                                    user, company_currency_id, stmt_currency_id,
                                    move_line.credit, context=ctx)
            """
        return res

    @api.multi
    def _margin_compute(self):
        res = {}
        res_currency_obj = self.env['res.currency']
        res_users_obj = self.env['res.users']
        company_currency_id = res_users_obj.browse(cursor, user, user).company_id.currency_id.id
        for statement in self.browse(cursor, user):
            res[statement.id] = statement.balance_end_real - statement.balance_end
        return res

    @api.multi
    def _get_statement(self):
        result = {}
        for line in self.env['account.bank.statement.line']:
            result[line.statement_id.id] = True
        return result.keys()

    margin_compute = fields.Float(
        compute='_margin_compute',
        string="Computed Margin",
        help='Margin as calculated Ending balance minuse Computed Balance',
        store=True,
    )
    temp_state = fields.Char(string='Temp', size=64)
    balance_end = fields.Float(
        compute='_fal_end_balance',
        string="Computed Balance",
        help='Balance as calculated based on Starting Balance and transaction lines',
        store=True
    )

    @api.multi
    def button_dummy(self):
        if context is None:
            context = {}
        for statement in self:
            if statement.temp_state and statement.temp_state == '1' :
                self.write({'temp_state':'2'})
            else:
                self.write({'temp_state':'1'})
        return self.write({})

    @api.multi
    def button_line_delete(self):
        for statement in self:
            if statement.move_line_ids:
                self.write({'move_line_ids': [(5, False, False)], })
        return self.write({})

    """
    def button_confirm_bank(self, cr, uid, ids, context=None):
        if context is None:
            context = {}
        res = super(account_bank_statement, self).button_confirm_bank(cr, uid, ids, context=context)
        for statement in self.browse(cr, uid, ids, context=context):
            for statement_line in statement.line_ids:
                if not statement_line.account_id:
                    raise orm.except_orm(_('Error!'),_('There\'s still bank statement line that has no account yet, please filled it or click reconcile button.'))
        return res
    """
    @api.multi
    def _prepare_move_line_vals(self, st_line, move_id, debit, credit, currency_id=False,
                amount_currency=False, account_id=False, partner_id=False):
        res = super(account_bank_statement, self)._prepare_move_line_vals(st_line, move_id, debit, credit, currency_id=currency_id,
                amount_currency=amount_currency, account_id=account_id, partner_id=partner_id)
        res['analytic_account_id'] = st_line.analytic_account_id.id
        return res

# end of account_bank_statement()


class account_bank_statement_line(models.Model):
    _name = "account.bank.statement.line"
    _inherit = "account.bank.statement.line"

    analytic_account_id = fields.Many2one(
        'account.analytic.account',
        string='Analytic Account'
    )

    @api.multi
    def cancel(self):
        bank_statement_obj = self.env['account.bank.statement']
        for line in self:
            if line.statement_id.state == 'confirm':
                bank_statement_obj.write([line.statement_id.id], {
                    'state': 'draft'
                })
        return super(account_bank_statement_line, self).cancel()

# end of account_bank_statement_line()


class account_voucher(models.Model):
    _name = 'account.voucher'
    _inherit = 'account.voucher'

    @api.multi
    def cancel_voucher(self):
        reconcile_pool = self.env['account.move.reconcile']
        move_pool = self.env['account.move']

        for voucher in self:
            # refresh to make sure you don't unlink an already removed move
            voucher.refresh()
            recs = []
            for line in voucher.move_ids:
                if line.statement_id and line.statement_id.state == 'confirm':
                    raise UserError(_("Warning"), _('Can\'t be unreconciled because the bank statement: "%s" is already closed, Please open the bank statement first!') % line.statement_id.name)

        return super(account_voucher, self).cancel_voucher()

# end of account_voucher()
