#-*- coding:utf-8 -*-
import time
from openerp import netsvc
from datetime import date, datetime, timedelta

from odoo import fields, models, api, _
from odoo.tools import config, float_compare, float_is_zero
from odoo.exceptions import UserError, ValidationError


class hr_payslip(models.Model):
    _inherit = "hr.payslip"

    @api.multi
    def process_sheetprocess_sheet(self):
        move_pool = self.env['account.move']
        hr_payslip_line_pool = self.pool['hr.payslip.line']
        precision = self.env['decimal.precision'].precision_get('Payroll')
        timenow = time.strftime('%Y-%m-%d')

        for slip in self:
            line_ids = []
            debit_sum = 0.0
            credit_sum = 0.0
            date = timenow

            name = _('Payslip of %s') % (slip.employee_id.name)
            move = {
                'narration': name,
                'date': date,
                'ref': slip.number,
                'journal_id': slip.journal_id.id,
            }
            for line in slip.details_by_salary_rule_category:
                amt = slip.credit_note and -line.total or line.total
                if float_is_zero(amt, precision_digits=precision):
                    continue
                debit_account_id = line.salary_rule_id.account_debit.id
                credit_account_id = line.salary_rule_id.account_credit.id
                # modif start here
                var_aaa = line.salary_rule_id.analytic_account_id and \
                    line.salary_rule_id.analytic_account_id.id
                var_bbb = slip.contract_id.analytic_account_id and \
                    slip.contract_id.analytic_account_id.id
                anal_account = var_aaa or var_bbb or False
                if debit_account_id and amt != 0.00:
                    # end here
                    debit_line = (0, 0, {
                        'name': line.name,
                        'date': date,
                        'partner_id': hr_payslip_line_pool._get_partner_id(
                            line,
                            credit_account=False),
                        'account_id': debit_account_id,
                        'journal_id': slip.journal_id.id,
                        'debit': amt > 0.0 and amt or 0.0,
                        'credit': amt < 0.0 and -amt or 0.0,
                        # modif start here
                        'analytic_account_id': anal_account,
                        # end here
                        'tax_line_id': line.salary_rule_id.account_tax_id and \
                        line.salary_rule_id.account_tax_id.id or False,
                    })
                    line_ids.append(debit_line)
                    debit_sum += debit_line[2]['debit'] - \
                        debit_line[2]['credit']
                # modif start here
                if credit_account_id and amt != 0.00:
                    # end here
                    credit_line = (0, 0, {
                        'name': line.name,
                        'date': date,
                        'partner_id': hr_payslip_line_pool._get_partner_id(
                            line,
                            credit_account=True),
                        'account_id': credit_account_id,
                        'journal_id': slip.journal_id.id,
                        'debit': amt < 0.0 and -amt or 0.0,
                        'credit': amt > 0.0 and amt or 0.0,
                        # modif start here
                        'analytic_account_id': anal_account,
                        # end here
                        'tax_line_id': line.salary_rule_id.account_tax_id \
                        and line.salary_rule_id.account_tax_id.id or False,
                    })
                    line_ids.append(credit_line)
                    credit_sum += credit_line[2]['credit'] - \
                        credit_line[2]['debit']

            if float_compare(
                credit_sum,
                debit_sum,
                precision_digits=precision
            ) == -1:
                acc_id = slip.journal_id.default_credit_account_id.id
                if not acc_id:
                    raise ValidationError(
                        _('Configuration Error!'),
                        _('The Salary Journal "%s" has not properly configured \
                         the Credit Account!') % (slip.journal_id.name)
                    )
                adjust_credit = (0, 0, {
                    'name': _('Adjustment Entry'),
                    'date': date,
                    'partner_id': False,
                    'account_id': acc_id,
                    'journal_id': slip.journal_id.id,
                    'debit': 0.0,
                    'credit': debit_sum - credit_sum,
                    'analytic_account_id': slip.contract_id.analytic_account_id and slip.contract_id.analytic_account_id.id or False,
                })
                line_ids.append(adjust_credit)

            elif float_compare(
                debit_sum,
                credit_sum,
                precision_digits=precision
            ) == -1:
                acc_id = slip.journal_id.default_debit_account_id.id
                if not acc_id:
                    raise ValidationError(
                        _('Configuration Error!'),
                        _('The Salary Journal "%s" has not properly configured \
                         the Debit Account!') % (slip.journal_id.name)
                    )
                adjust_debit = (0, 0, {
                    'name': _('Adjustment Entry'),
                    'date': date,
                    'partner_id': False,
                    'account_id': acc_id,
                    'journal_id': slip.journal_id.id,
                    'debit': credit_sum - debit_sum,
                    'credit': 0.0,
                    'analytic_account_id': slip.contract_id.analytic_account_id and slip.contract_id.analytic_account_id.id or False,
                })
                line_ids.append(adjust_debit)
            move.update({'line_ids': line_ids})
            move_id = move_pool.create(move)
            self.write([slip.id], {'move_id': move_id, 'date': date})
            move_pool.post([move_id])
        return self.write({'paid': True, 'state': 'done'})

# end of hr_payslip()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
