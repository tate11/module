# -*- coding: utf-8 -*-
from odoo import fields, models, api


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    fal_project_numbers = fields.Char(
        compute='_get_projects',
        string='Projects',
        help='The Projects',
        store=True
    )

    @api.multi
    @api.depends('order_line')
    def _get_projects(self):
        for purchase in self:
            temp = []
            for line in purchase.order_line:
                if line.account_analytic_id \
                        and line.account_analytic_id.code not in temp:
                    temp.append(
                        line.account_analytic_id.code or
                        line.account_analytic_id.name
                    )
                if temp:
                    purchase.fal_project_numbers = "; ".join(temp)
                else:
                    purchase.fal_project_numbers = ""
