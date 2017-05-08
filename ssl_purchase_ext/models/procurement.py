from odoo import models, api, fields


class ProcurementOrder(models.Model):
    _inherit = 'procurement.order'

    fal_port_departure = fields.Char(string="Port of Departure")
    fal_port_destination = fields.Char(string="Port of Destination")
    fal_payment_term_id = fields.Many2one(
        'account.payment.term', string='Payment term')
    fal_deposit_term_id = fields.Many2one(
        'fal.deposit.term', string='Deposit Term')
    fal_payment_mean_id = fields.Many2one(
        'fal.payment.mean', string='Payment Mean')
    fal_incoterm_id = fields.Many2one(
        'stock.incoterms', string='Incoterm')
    fal_sale_user_id = fields.Many2one(
        'res.users', string='Sale Order Responsible')
    fal_sale_line_name = fields.Char(string='SO Line Desc')
    fal_sale_note = fields.Text(string='SO Note')
    fal_easy_sale_client_ref = fields.Char(
        string='Sale Order Client Ref')
    fal_pcs_unit = fields.Float(
        string='Pcs per Unit',
    )

    @api.multi
    def _prepare_purchase_order(self, partner):
        res = super(ProcurementOrder, self)._prepare_purchase_order(partner)
        if partner.fal_ssl_company:
            proc = self.group_id.procurement_ids.filtered(
                lambda r: not r.purchase_line_id)
            if proc:
                proc = proc[0]
                res.update({
                    'payment_term_id': proc.fal_payment_term_id.id,
                    'incoterm_id': proc.fal_incoterm_id.id,
                    'fal_payment_mean_id': proc.fal_payment_mean_id.id,
                    'fal_deposit_term_id': proc.fal_deposit_term_id.id,
                    'fal_port_departure': proc.fal_port_departure,
                    'fal_port_destination': proc.fal_port_destination,
                    'fal_sale_user_id': proc.fal_sale_user_id.id,
                    'notes': proc.fal_sale_note,
                    'fal_easy_sale_client_ref': proc.fal_easy_sale_client_ref,
                })
        return res

    @api.multi
    def _prepare_purchase_order_line(self, po, supplier):
        res = super(ProcurementOrder, self).\
            _prepare_purchase_order_line(po, supplier)
        thisproc = self[0]
        proc = self.group_id.procurement_ids.filtered(
            lambda r: not r.purchase_line_id and
            r.product_id == thisproc.product_id
        )
        product_lang = self.product_id.with_context({
            'lang': supplier.name.lang,
            'partner_id': supplier.name.id,
        })
        name = product_lang.display_name
        if product_lang.description_purchase:
            name += '\n' + product_lang.description_purchase
        if proc:
            proc = proc[0]
            res.update({
                'name': proc.fal_sale_line_name or name,
                'fal_pcs_unit': proc.fal_pcs_unit,
            })
        return res

    @api.multi
    def make_po(self):
        res = super(ProcurementOrder, self).make_po()
        procs = self.browse(res)
        groups = self.env['procurement.group']
        for proc in procs:
            groups |= proc.group_id
        for gr in groups:
            proc_pur = gr.procurement_ids.filtered(
                lambda r: r.purchase_line_id
            )
            proc_sale = gr.procurement_ids.filtered(
                lambda r: r.sale_line_id
            )
            if proc_pur and proc_sale:
                sale = proc_sale[0].sale_line_id.order_id
                pur = proc_pur[0].purchase_line_id.order_id
                sale.write({'fal_purchase_doc': pur.name})
        return res
