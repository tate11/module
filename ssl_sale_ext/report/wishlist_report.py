# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, models
from odoo.report import report_sxw
import logging
_logger = logging.getLogger(__name__)


class report_wishlist(report_sxw.rml_parse):

    def set_context(self, objects, data, ids, report_type=None):
        res = super(report_wishlist, self).set_context(
            objects, data, ids, report_type=report_type)

        leads = self.localcontext.get('objects', False)

        header = []
        pricelist_data = []
        for lead in leads:
            for line in lead.fal_lead_ids:
                for item in line.wishlist_price_ids:
                    header.append(item.min_qty)

        if header:
            header = list(set(header))
            header.sort()
            pricelist_items = {}

            for lead in leads:
                for line in lead.fal_lead_ids:
                    for item in line.wishlist_price_ids:
                        if line not in pricelist_items:
                            pricelist_items[line] = {item.min_qty: item.price}
                        else:
                            pricelist_items[line].update(
                                {item.min_qty: item.price})
                    if line not in pricelist_items:
                        pricelist_items[line] = {}
                    if line in pricelist_items.keys():
                        price_line = pricelist_items.get(line)
                        cur_head = price_line.keys()
                        if len(cur_head) != len(header):
                            diff = list(set(cur_head) - set(header)) + \
                                list(set(header) - set(cur_head))
                            diff.sort()
                            for d in diff:
                                price_line[d] = 'empty'
            if pricelist_items:
                for k, v in pricelist_items.iteritems():
                    pricelist_items[k] = sorted(
                        v.items(), key=lambda tup: tup[0])

            pricelist_data = pricelist_items.items()
            _logger.info(pricelist_data)

        header = [int(x) for x in header]

        self.localcontext.update({
            'get_header': lambda: header,
            'get_value': lambda: pricelist_data,
            'get_header_length': lambda: len(header),
        })
        return res


class WishlistReport(models.AbstractModel):
    """Model used to embed old style reports"""
    _name = 'report.ssl_sale_ext.report_saleorder_document_pipeline'
    _template = 'ssl_sale_ext.report_saleorder_document_pipeline'
    _wrapped_report_class = report_wishlist
    _inherit = 'report.abstract_report'
