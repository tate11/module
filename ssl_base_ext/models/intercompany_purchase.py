from odoo import models, api, _


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    @api.one
    def _prepare_sale_order_data(
            self, name, partner, company, direct_delivery_address):
        '''
        Overriden version on intercompany modules
        '''
        partner_addr = partner.sudo().\
            address_get(['invoice', 'delivery', 'contact'])
        warehouse = company.warehouse_id and \
            company.warehouse_id.company_id.id == company.id and \
            company.warehouse_id or False
        if not warehouse:
            raise Warning(
                _('Configure correct warehouse for company(%s) \
                    from Menu: Settings/Users/Companies' % (company.name)))
        sq = self.env['ir.sequence']
        partner_shipping = direct_delivery_address or partner_addr['delivery']
        return {
            'name': sq.sudo().next_by_code('fal.sale.quotation.number') or '/',
            'company_id': company.id,
            'warehouse_id': warehouse.id,
            'client_order_ref': name,
            'partner_id': partner.id,
            'pricelist_id': partner.property_product_pricelist.id,
            'partner_invoice_id': partner_addr['invoice'],
            'date_order': self.date_order,
            'fiscal_position_id': partner.property_account_position_id.id,
            'user_id': False,
            'auto_generated': True,
            'auto_purchase_order_id': self.id,
            'partner_shipping_id': partner_shipping
        }
