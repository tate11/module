# -*- coding: utf-8 -*-
from odoo import fields, models, api, _
from openerp.exceptions import UserError


class hr_timesheet_invoice_create(models.TransientModel):
    _name = 'hr.timesheet.invoice.create'
    _description = 'Create invoice from timesheet'

    #date = fields.Boolean('Date', help='The real date of each work will be displayed on the invoice')
    #time = fields.Boolean('Time spent', help='The time of each work done will be displayed on the invoice')
    #name = fields.Boolean('Description', help='The detail of each work done will be displayed on the invoice')
    #price = fields.Boolean('Cost', help='The cost of each work done will be displayed on the invoice. You probably don\'t want to check this')
    #product = fields.Many2one('product.product', 'Force Product', help='Fill this field only if you want to force to use a specific product. Keep empty to use the real product that comes from the cost.')

    @api.multi
    def do_create(self):
        # Create an invoice based on selected timesheet lines
        analytic_line_obj = self.env['account.analytic.line']
        invoice_obj = self.env['account.invoice']
        invs = []
        invoices = {}
        for analytic_line in analytic_line_obj.browse(self.env.context.get('active_ids', False)):
            if not analytic_line.to_invoice:
                raise UserError(_('Trying to invoice non invoiceable line for %s.') % (analytic_line.product_id.name))
            if analytic_line.invoice_id:
                raise UserError(_("There's is line that already invoiced"))
            group_key = analytic_line.task_id.sale_line_id.order_id.id
            if group_key not in invoices:
                inv_id = invoice_obj.create(analytic_line._prepare_timesheet_invoice(analytic_line.task_id.sale_line_id.order_id.partner_invoice_id, analytic_line.task_id.sale_line_id.order_id.company_id, analytic_line.task_id.sale_line_id.order_id.currency_id))
                invoices[group_key] = inv_id.id
                invs.append(inv_id.id)
            account = analytic_line.task_id.sale_line_id.product_id.property_account_income_id or analytic_line.task_id.sale_line_id.product_id.categ_id.property_account_income_categ_id
            if not account:
                raise UserError(_('Please define income account for this product: "%s" (id:%d) - or for its category: "%s".') % \
                                (analytic_line.task_id.sale_line_id.product_id.name, analytic_line.task_id.sale_line_id.product_id.id, analytic_line.task_id.sale_line_id.product_id.categ_id.name))

            fpos = analytic_line.task_id.sale_line_id.order_id.fiscal_position_id or analytic_line.task_id.sale_line_id.order_id.partner_id.property_account_position_id
            if fpos:
                account = fpos.map_account(account)

            invoice_line_id = self.env['account.invoice.line'].create({
                'name': analytic_line.task_id.sale_line_id.name,
                'sequence': analytic_line.task_id.sale_line_id.sequence,
                'origin': analytic_line.task_id.sale_line_id.order_id.name,
                'account_id': account.id,
                'price_unit': analytic_line.task_id.sale_line_id.price_unit,
                'quantity': analytic_line.unit_amount,
                'discount': analytic_line.to_invoice.factor,
                'uom_id': analytic_line.task_id.sale_line_id.product_uom.id,
                'product_id': analytic_line.task_id.sale_line_id.product_id.id or False,
                'invoice_line_tax_ids': [(6, 0, analytic_line.task_id.sale_line_id.tax_id.ids)],
                'account_analytic_id': analytic_line.task_id.sale_line_id.order_id.project_id.id,
                'invoice_id': invoices[group_key],
                'sale_line_ids': [(6, 0, [analytic_line.task_id.sale_line_id.id])],
            })
            analytic_line.invoice_id = invoices[group_key]

        imd = self.env['ir.model.data']
        action = imd.xmlid_to_object('account.action_invoice_tree1')
        list_view_id = imd.xmlid_to_res_id('account.invoice_tree')
        form_view_id = imd.xmlid_to_res_id('account.invoice_form')


        return {
            'name': action.name,
            'help': action.help,
            'type': action.type,
            'views': [[list_view_id, 'tree'], [form_view_id, 'form'], [False, 'graph'], [False, 'kanban'], [False, 'calendar'], [False, 'pivot']],
            'target': action.target,
            'context': action.context,
            'res_model': action.res_model,
            'domain' : "[('id', 'in', %s)]" % invs
        }

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:

