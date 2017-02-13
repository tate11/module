# -*- coding: utf-8 -*-
from odoo import models, fields, api, _


class invoice_balance_wizard(models.TransientModel):
    _name = "invoice.balance.wizard"
    _description = "Invoice Balance Wizard"

    to_date = fields.Date(string='To', required=True)
    type = fields.Selection([
        ('all', 'All'),
        ('out_invoice', 'Customer Invoice'),
        ('in_invoice', 'Supplier Invoice'),
        ('out_refund', 'Customer Refund'),
        ('in_refund', 'Supplier Refund')],
        string='Type',
        select=True,
        change_default=True,
        required=True
    )

    @api.multi
    def search_invoice_balance_date(self):
        ctx = dict(self._context)
        data_wizard = self.read()[0]
        domain = []
        if data_wizard['type'] != 'all':
            domain = [('type', '=', data_wizard['type'])]
        domain += [
            ('state', 'not in', ['draft', 'cancel']),
            ('date', '<=', data_wizard['to_date']),
            ('amount_balance_date', '!=', 0.00)]
        ctx['wizard_data_date'] = data_wizard['to_date']
        return {
            'type': 'ir.actions.act_window',
            'name': 'Invoices Balance Based on ' + str(data_wizard['to_date']),
            'res_model': 'account.invoice',
            'view_mode': 'tree',
            'view_type': 'form',
            'view_id': self.env['ir.model.data'].get_object_reference(
                    'fal_invoice_balance_date',
                    'invoice_tree_fal_balance_date')[1],
            'domain': domain,
            'target': 'current',
            'context': ctx,
        }

# end of invoice_balance_wizard()
