# -*- coding: utf-8 -*-

from odoo import fields, models, api, _
import odoo.addons.decimal_precision as dp
from odoo.exceptions import ValidationError


class fapiao(models.Model):
    _name = "fapiao"
    _inherit = ['mail.thread']
    _order = "fapiao_date desc, id desc"
    _description = "Fapiao"

    name = fields.Char(
        string='Fapiao Sequence Number',
        size=64
    )

    fapiao_type = fields.Selection([
        ('customer', 'Customer'),
        ('supplier', 'Supplier'),
        ('customer_credit_note', 'Customer Credit note'),
        ('customer_credit_note', 'Customer Credit note')],
        string='Fapiao Type',
        required=True,
    )

    tax_id = fields.Many2one(
        'account.tax',
        string='Tax'
    )

    total_tax_amount = fields.Float(
        compute='_total_amount_tax_fapiao',
        string='Total Tax Amount',
        help='The tax amount of Fapiao.',
        store=True,
    )

    partner_id = fields.Many2one(
        'res.partner',
        string='Partner',
        required=True
    )

    fapiao_number = fields.Char(
        string='Fapiao Number',
        size=64,
        required=True
    )

    fapiao_date = fields.Date(
        string='Fapiao Date',
        required=True,
    )

    fapiao_declaration_date = fields.Date(
        string='Declaration Date'
    )

    reception_date = fields.Date(
        string='Reception Date'
    )

    amount_with_taxes = fields.Float(
        compute='_amount_total_fapiao',
        string='Total Fapiao Amount',
        help='The total amount of Fapiao.',
        store=True,
    )

    fapiao_line_ids = fields.One2many(
        'fapiao.line',
        'fapiao_id',
        string='Fapiao Line'
    )

    tag_ids = fields.Many2many(
        'fapiao.tag.line',
        string='Tags'
    )

    notes = fields.Text(
        string='Notes'
    )

    state = fields.Selection([
        ('Draft', 'Draft'),
        ('Posted', 'Posted')],
        string='Status',
        readonly=True,
        required=True,
        default='Draft',
    )

    company_id = fields.Many2one(
        'res.company',
        string='Company',
        required=True,
        readonly=True,
        default=lambda self: self.env['res.company']._company_default_get('res.users')
    )

    @api.multi
    def _get_fapiao_line(self):
        result = {}
        for line in self.env['fapiao.line'].browse():
            result[line.fapiao_id.id] = True
        return result.keys()

    @api.multi
    def _amount_total_fapiao(self, field_name):
        res = {}
        for fapiao in self.browse():
            total_fapiao_amount = 0
            for fapiao_line in fapiao.fapiao_line_ids:
                if not fapiao_line.not_fapiao:
                    total_fapiao_amount += fapiao_line.allocated_ammount
            res[fapiao.id] = total_fapiao_amount
        return res

    def _total_amount_tax_fapiao(self, field_name):
        res = {}
        for fapiao in self.browse():

            total_fapiao_amount = 0.00
            total_tax_fapiao_amount = 0.00
            tax_obj = self.env['account.tax']

            for fapiao_line in fapiao.fapiao_line_ids:
                if not fapiao_line.not_fapiao:
                    total_fapiao_amount += fapiao_line.allocated_ammount
            if fapiao.tax_id:
                total_tax_fapiao_amount = total_fapiao_amount\
                    / (100 + fapiao.tax_id.amount) * fapiao.tax_id.amount
            res[fapiao.id] = total_tax_fapiao_amount
        return res

    def copy(self, default=None):
        default = default or {}
        default.update({
            'fapiao_line_ids': [],
        })
        return super(fapiao, self).copy(default)

    @api.multi
    def onchange_partner_id(self, partner_id):
        res = {}
        invoice_obj = self.env['account.invoice']
        partner_obj = self.env['res.partner']
        fapiao_line_obj = self.env['fapiao.line']

        # part need to be fixed

        typeinvoice = False
        if context.get('default_fapiao_type', False) == 'customer':
            typeinvoice = 'out_invoice'
        if context.get('default_fapiao_type', False) == 'supplier':
            typeinvoice = 'in_invoice'
        invoice_ids = invoice_obj.search([
            ('commercial_partner_id', '=', partner_id),
            ('state', '!=', 'cancel'),
            ('type', '=', typeinvoice)
        ])
        temp = []
        for fapiao in self.browse():
            temp_line = []
            for fapiao_line_id in fapiao.fapiao_line_ids:
                temp_line.append((2, fapiao_line_id.id))
            if temp_line:
                temp += temp_line
        for invoice_id in invoice_obj.browse(invoice_ids):
            allocated_amount_posted = 0.00
            fapiao_line_posted_ids = fapiao_line_obj.search([
                ('invoice_id', '=', invoice_id.id),
                ('fapiao_id.state', '=', 'Posted')
            ])
            for fapiao_line_posted_id in\
                    fapiao_line_obj.browse(fapiao_line_posted_ids):
                allocated_amount_posted +=\
                    fapiao_line_posted_id.allocated_ammount
            open_balance = invoice_id.amount_total - allocated_amount_posted
            if open_balance == 0:
                continue
            else:
                temp.append((0, 0, {
                    'invoice_id': invoice_id.id,
                    'invoice_date': invoice_id.date_invoice,
                    'invoice_amount_total': invoice_id.amount_total,
                    'invoice_state': invoice_id.state,
                    'full_reconcile': True,
                    'open_balance_temp': open_balance,
                    'open_balance': open_balance,
                    'allocated_ammount': open_balance,
                }))
        res['value'] = {'fapiao_line_ids': temp}
        return res

    @api.multi
    def action_validated(self):
        for fapiao in self.browse():
            for line in fapiao.fapiao_line_ids:
                if line.allocated_ammount:
                    for lines in line.invoice_id.fapiao_line_ids:
                        if lines.fapiao_id.state == 'Posted'\
                                and lines.full_reconcile:
                            raise ValidationError(
                                _('Error!'),
                                _("Line for invoice:'%s' has been reconciled!")
                                % (line.invoice_id.number)
                            )
        fapiao_number = self.env['ir.sequence'].get('fapiao.fwa1') or '/'
        return self.write({'state': 'Posted', 'name': fapiao_number})
    # raise (_('The bank account of a bank journal\
    #     must belong to the same company (%s).') % self.company_id.name)
    '''
    A bank account can belong to a customer/supplier,
    in which case their partner_id is the customer/supplier.
    '''

    @api.multi
    def action_cancel_fapiao(self):
        return self.write({'state': 'Draft'})

    @api.multi
    def onclick_reconcile_all_fapiao(self):
        fapiao_line_obj = self.env['fapiao.line']
        for fapiao in self.browse():
            temp_checkbox = []
            temp_ids = []
            for fapiao_line in fapiao.fapiao_line_ids:
                temp_checkbox.append(fapiao_line.full_reconcile)
                temp_ids.append(fapiao_line.id)
            if False in temp_checkbox:
                for fapiao_line in fapiao.fapiao_line_ids:
                    fapiao_line_obj.write(fapiao_line.id, {
                        'full_reconcile': True,
                        'allocated_ammount': fapiao_line.open_balance or 0.0
                    })
            else:
                for fapiao_line in fapiao.fapiao_line_ids:
                    fapiao_line_obj.write(fapiao_line.id, {
                        'full_reconcile': False,
                        'allocated_ammount': 0.0
                    })
        return True

# end of fapiao()


class fapiao_tag_line(models.Model):
    _name = 'fapiao.tag.line'
    _description = "Fapiao Tag Line"

    name = fields.Char(
        string='Name')

# end of fapiao_tag_line()


class account_invoice(models.Model):
    _inherit = 'account.invoice'

    fapiao_line_ids = fields.One2many(
        'fapiao.line',
        'invoice_id',
        string='Fapiao Line'
    )

    fapiao_line_ids_display = fields.One2many(
        'fapiao.line',
        string='Fapiao Lines',
        compute='_get_lines',
        method=True
    )

    def _get_lines(self):
        temp = []
        res = {}
        for invoice in self.browse():
            for fapiao_line in invoice.fapiao_line_ids:
                if not fapiao_line.not_fapiao and\
                    fapiao_line.fapiao_state == 'Posted' and\
                        fapiao_line.allocated_ammount:
                    temp.append(fapiao_line.id)
            res[invoice.id] = temp
        return res

    def copy(self):
        default = {}
        default.update({
            'fapiao_line_ids': [],
        })
        return super(account_invoice, self).copy(default)

# end of account_invoice()


class fapiao_line(models.Model):
    _name = 'fapiao.line'
    _description = "Fapiao Line"

    fapiao_id = fields.Many2one(
        'fapiao',
        string='Fapiao',
        ondelete='cascade',
        select=1
    )

    fapiao_number = fields.Char(
        related='fapiao_id.fapiao_number',
        string='Fapiao Number',
        store=False
    )

    fapiao_date = fields.Date(
        related='fapiao_id.fapiao_date',
        string='Fapiao Date',
        store=False
    )

    fapiao_state = fields.Selection(
        related='fapiao_id.state',
        string='Fapiao Status',
        store=False
    )

    invoice_id = fields.Many2one(
        'account.invoice',
        string='Invoice',
        required=True
    )

    invoice_date = fields.Date(
        related='invoice_id.date_invoice',
        string='Invoice Date',
        store=False
    )

    invoice_amount_total = fields.Monetary(
        related='invoice_id.amount_total',
        string='Invoice Amount Total',
        store=False
    )

    invoice_state = fields.Selection(
        related='invoice_id.state',
        string='Invoice Status',
        store=False
    )

    full_reconcile = fields.Boolean(
        string='Full Reconcile')

    allocated_ammount = fields.Float(
        string='Allocated Amount'
    )

    open_balance_temp = fields.Float(
        compute='_get_open_balance_temp',
        string='Open Balance',
        store=False
    )

    open_balance = fields.Float(
        string='Open Balance',
    )

    not_fapiao = fields.Boolean(
        string='Not Fapiao'
    )

    def onchange_full_reconcile(self, full_reconcile, open_balance):
        res = {}
        if self.full_reconcile:
            res['value'] = {
                'allocated_ammount': self.open_balance,
            }
        else:
            res['value'] = {
                'allocated_ammount': 0,
            }
        return res

    @api.multi
    def onchange_allocated_ammount(self, allocated_ammount, open_balance):
        res = {}
        if self.allocated_ammount == self.open_balance:
            res['value'] = {
                'full_reconcile': True,
            }
        else:
            res['value'] = {
                'full_reconcile': False,
            }
        return res

    @api.multi
    def _get_open_balance_temp(self, field_name):
        res = {}
        for fapiao_line in self.browse():
            res[fapiao_line.id] = fapiao_line.open_balance
        return res

    @api.multi
    def open_invoice(self):
        return {
            'type': 'ir.actions.act_window',
            'name': self.invoice_id.number,
            'res_model': 'account.invoice',
            'res_id': self.invoice_id.id,
            'view_type': 'form',
            'view_mode': 'form',
            'target': 'new',
            'nodestroy': True,
        }

# end of fapiao_line()
