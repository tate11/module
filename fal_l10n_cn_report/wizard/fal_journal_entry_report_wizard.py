from odoo import fields, models, api, _
from datetime import datetime, date, timedelta
from openerp.exceptions import UserError, ValidationError
from openerp.tools import DEFAULT_SERVER_DATE_FORMAT


class fal_journal_entry_report_wizard(models.TransientModel):
    _name = "fal.journal.entry.report.wizard"

    start_date = fields.Date(string='Start Date', required=1)
    end_date = fields.Date(string='End Date', required=1)

    @api.multi
    def action_print(self):
        self.ensure_one()
        account_move_obj = self.env['account.move']
        if self.end_date < self.start_date:
            raise UserError(_("Start date cannot be greater then end date!"))
        account_move_ids = account_move_obj.search([
            ('date', '>=', self.start_date),
            ('date', '<=', self.end_date)])
        return self.env['report'].get_action(
            account_move_ids, 'fal_l10n_cn_report.fal_journal_entry_report')

# end of validate_sales_forecast_history_wizard()
