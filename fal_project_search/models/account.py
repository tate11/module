# -*- coding: utf-8 -*-
from odoo import fields, models, api


class AccountInvoice(models.Model):
    _inherit = 'account.invoice'

    fal_project_numbers = fields.Char(
        compute='_get_projects',
        string='Projects',
        help='The Projects',
        store=True
    )

    @api.multi
    @api.depends('invoice_line_ids')
    def _get_projects(self):
        for invoice in self:
            temp = []
            for line in invoice.invoice_line_ids:
                if line.account_analytic_id \
                        and line.account_analytic_id.code not in temp:
                    temp.append(
                        line.account_analytic_id.code or
                        line.account_analytic_id.name
                    )
                if temp:
                    invoice.fal_project_numbers = "; ".join(temp)
                else:
                    invoice.fal_project_numbers = ""
