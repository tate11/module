# -*- coding: utf-8 -*-
from odoo import fields, models, api, _
from datetime import datetime, timedelta
from openerp.exceptions import UserError
import time


class hr_timesheet_invoice_factor(models.Model):
    _name = "hr_timesheet_invoice.factor"
    _description = "Invoice Rate"
    _order = 'factor'

    name = fields.Char('Internal Name', required=True, translate=True)
    customer_name = fields.Char('Name', help="Label for the customer")
    factor = fields.Float(
        'Discount (%)',
        required=True,
        help="Discount in percentage")

# end of hr_timesheet_invoice_factor()


class account_analytic_account(models.Model):
    _inherit = "account.analytic.account"

    to_invoice = fields.Many2one(
        'hr_timesheet_invoice.factor',
        'Timesheet Invoicing Ratio',
        help="You usually invoice 100% of the timesheets. \
        But if you mix fixed price and timesheet invoicing, \
        you may use another ratio. For instance, \
        if you do a 20% advance invoice (fixed price, based on a sales order),\
        you should invoice the rest on timesheet with a 80% ratio.")

# end of account_analytic_account()


class account_analytic_line(models.Model):
    _inherit = 'account.analytic.line'

    invoice_id = fields.Many2one(
        'account.invoice',
        'Invoice',
        ondelete="set null",
        copy=False)
    to_invoice = fields.Many2one(
        'hr_timesheet_invoice.factor',
        'Invoiceable',
        help="It allows to set the discount while making invoice, \
        keep empty if the activities should not be invoiced.")

    @api.onchange('account_id')
    def onchange_account_id(self):
        if self.account_id:
            self.to_invoice = self.account_id.to_invoice.id

    @api.model
    def create(self, vals):
        if not vals.get('to_invoice', False):
            vals['to_invoice'] = self.env['account.analytic.account'].\
                browse(vals['account_id']).to_invoice.id
        return super(account_analytic_line, self).create(vals)

    @api.multi
    def write(self, vals):
        self._check_inv(vals)
        return super(account_analytic_line, self).write(vals)

    @api.multi
    def _check_inv(self, vals):
        if ( not vals.has_key('invoice_id')) or vals['invoice_id' ] == False:
            for line in self:
                if line.invoice_id:
                    raise UserError(_('Error!'),
                        _('You cannot modify an invoiced analytic line!'))
        return True

    @api.model
    def _prepare_timesheet_invoice(self, partner_id, company_id, currency_id):
        """ returns values used to create main invoice from analytic lines"""
        account_payment_term_obj = self.env['account.payment.term']
        invoice_name = self.account_id.name

        date_due = False
        if partner_id.property_payment_term_id:
            pterm_list = account_payment_term_obj.compute(
                partner_id.property_payment_term_id.id, value=1,
                date_ref=time.strftime('%Y-%m-%d'))
            if pterm_list:
                pterm_list = [line[0] for line in pterm_list]
                pterm_list.sort()
                date_due = pterm_list[-1]
        return {
            'name': "%s - %s" % (time.strftime('%d/%m/%Y'), invoice_name),
            'partner_id': partner_id.id,
            'company_id': company_id.id,
            'payment_term': partner_id.property_payment_term_id.id or False,
            'account_id': partner_id.property_account_receivable_id.id,
            'currency_id': currency_id.id,
            'date_due': date_due,
            'fiscal_position': partner_id.property_account_position_id.id
        }

# end of account_analytic_line()


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    timesheet_ids = fields.Many2many(compute='_compute_timesheet_ids')
    timesheet_count = fields.Float(compute='_compute_timesheet_ids')

    @api.multi
    @api.depends('project_id.line_ids')
    def _compute_timesheet_ids(self):
        for order in self:
            order.timesheet_ids = self.env['account.analytic.line'].\
                search([
                    ('is_timesheet', '=', True),
                    ('account_id', '=', order.project_id.id),
                    ('task_id.sale_line_id', 'in', order.order_line.ids)
                ]) if order.project_id else []
            order.timesheet_count = round(sum(
                [line.unit_amount for line in order.timesheet_ids]), 2)


class procurement_order(models.Model):
    _inherit = "procurement.order"

    @api.model
    def _create_service_task(self, procurement):
        res = super(procurement_order, self)._create_service_task(procurement)
        self.env['project.task'].browse(res).name = '%s:%s' %\
            (procurement.origin or '', procurement.sale_line_id.name)
        return res

# end of procurement_order()
