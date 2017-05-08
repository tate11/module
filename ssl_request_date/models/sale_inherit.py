from odoo import api, fields, models
import logging

_logger = logging.getLogger(__name__)


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    fal_partner_request_date = fields.Datetime(string='Vendor Request Date')

    @api.multi
    def action_confirm(self):
        res = super(SaleOrder, self).action_confirm()
        for sale in self:
            sale.picking_ids.write({
                'fal_partner_request_date': sale.fal_partner_request_date
            })
        return res

    def _prepare_invoice(self):
        """
        copy additional data from sale order to invoice
        """
        invoice = super(SaleOrder, self)._prepare_invoice()
        if self.fal_partner_request_date:
            invoice['fal_partner_request_date'] = self.fal_partner_request_date
        return invoice


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    @api.multi
    def _prepare_order_line_procurement(self, group_id=False):
        vals = super(SaleOrderLine, self).\
            _prepare_order_line_procurement(group_id=group_id)
        if self.order_id.fal_partner_request_date:
            partner_date = self.order_id.fal_partner_request_date
            vals.update({
                'fal_partner_request_date': partner_date
            })
        return vals


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    fal_partner_request_date = fields.Datetime(string='Vendor Request Date')


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    fal_partner_request_date = fields.Datetime(string='Vendor Request Date')


class ProcurementOrder(models.Model):
    _inherit = 'procurement.order'

    fal_partner_request_date = fields.Datetime(string='Vendor Request Date')

    def _prepare_purchase_order_line(self, po, supplier):
        res = super(ProcurementOrder, self).\
            _prepare_purchase_order_line(po, supplier)
        vendor_proc = self.group_id.procurement_ids.\
            filtered(lambda r: r.fal_partner_request_date)
        if vendor_proc:
            if len(vendor_proc) > 1:
                vendor_proc = vendor_proc[0]
            res.update({'date_planned': vendor_proc.fal_partner_request_date})
        return res

    @api.multi
    def _prepare_purchase_order(self, partner):
        res = super(ProcurementOrder, self)._prepare_purchase_order(partner)
        exist_proc = self.group_id.procurement_ids.filtered('sale_line_id')
        if exist_proc:
            exist_proc = exist_proc[0]
            date_vendor = exist_proc.sale_line_id.order_id.\
                fal_partner_request_date
            res.update({
                'fal_partner_request_date': date_vendor
            })
        return res


class purchase_order(models.Model):

    _inherit = 'purchase.order'

    @api.model
    def _prepare_sale_order_data(
            self, name, partner, company, direct_delivery_address):
        res = super(purchase_order, self)._prepare_sale_order_data(
            name, partner, company, direct_delivery_address
        )
        if res:
            res[0].update({
                'fal_partner_request_date': self.fal_partner_request_date,
                'requested_date': self.fal_partner_request_date,
            })
        return res
