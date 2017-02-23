# -*- coding: utf-8 -*-
from odoo import fields, models, api, _

class account_bank_statement(models.Model):
    _name = "account.bank.statement"
    _inherit = "account.bank.statement"

    @api.multi
    def button_confirm_bank(self):
        res = super(account_bank_statement, self).button_confirm_bank()
        for st_line in self.line_ids:
            for journtal_entry in st_line.journal_entry_ids:
                for line in journtal_entry.line_ids:
                    line.write({'analytic_account_id': st_line.analytic_account_id.id})
        return res

# end of account_bank_statement()


class account_bank_statement_line(models.Model):
    _name = "account.bank.statement.line"
    _inherit = "account.bank.statement.line"

# end of account_bank_statement_line()
