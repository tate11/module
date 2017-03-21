from odoo import models, fields, api, _


class AccountMoveLine(models.Model):
    _name = "account.move.line"
    _inherit = "account.move.line"

    def _invoice(self, cursor, user, ids, name, arg, context=None):
        return super(AccountMoveLine, self)._invoice(cursor, user, ids, name, arg, context)

    def _invoice_search(self, cursor, user, obj, name, args, context=None):
        return super(AccountMoveLine, self)._invoice_search(cursor, user, obj, name, args, context)

    @api.multi
    def _get_move_lines(self):
        result = []
        for move in self:
            for line in move.line_id:
                result.append(line.id)
        return result

    @api.multi
    def _get_invoices(self):
        result = []
        for invoice in self:
            if invoice.move_id:
                for line in invoice.move_id.line_id:
                    result.append(line.id)
        return result

    invoice = fields.Many2many(
        'account.invoice',
        compute='_invoice',
        string='Invoice',
        type='many2one',
    )

# end of account_move_line()
