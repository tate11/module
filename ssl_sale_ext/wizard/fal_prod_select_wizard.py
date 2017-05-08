from odoo import models, api, fields
import logging
_logger = logging.getLogger(__name__)


class FalProdSelectWizard(models.TransientModel):
    _inherit = 'fal.prod.select.wizard'

    @api.multi
    def get_order_line(self, product_id, sale):
        res = super(FalProdSelectWizard, self).get_order_line(product_id, sale)
        res['order_line'][0][2].update({'fal_pcs_unit': self.fal_pcs_unit})
        return res

    @api.model
    def get_wishlist_pricelist(self, item, product):
        '''
        Inherited fromm original version.
        Reason: SSL only manage pricelist with option product variant
        only.
        '''
        to_create = []
        pricelist = item.partner_id and\
            item.partner_id.property_product_pricelist or False
        if pricelist and product:
            for line in pricelist.item_ids:
                cond1 = line.applied_on == '0_product_variant' and\
                    line.product_id == product
                if cond1:
                    to_create.append((0, 0, {
                        'min_qty': line.min_quantity,
                        'product_uom_id': product.uom_id.id,
                        'currency_id': pricelist.currency_id.id,
                        'price': self._get_display_price(
                            product, pricelist, line.min_quantity
                        )
                    }))
        return to_create
