# -*- coding: utf-8 -*-
# from odoo.addons.web.http import Controller, route, request
from odoo.addons.report.controllers.main import ReportController
from odoo import http
import simplejson
import logging

_logger = logging.getLogger(__name__)


class FalReportController(ReportController):
    @http.route(['/report/download'], type='http', auth="user")
    def report_download(self, data, token):
        # picking_obj = http.request.env['stock.picking']
        # mo_obj = http.request.env['mrp.production']
        # payslip_obj = http.request.env['hr.payslip']
        # expense_obj = http.request.env['hr.expense.expense']

        requestcontent = simplejson.loads(data)

        url, type = requestcontent[0], requestcontent[1]
        # url = u'/report/pdf/sale.report_saleorder/37'
        # type = u'qweb-pdf'

        response = ReportController().report_download(data, token)

        if type == 'qweb-pdf':
            reportname = url.split('/report/pdf/')[1].split('?')[0]
            # reportname = u'sale.report_saleorder/37'
            try:
                reportname, _docids = reportname.split('/')
                assert _docids
                # reportname = u'sale.report_saleorder'
                # docids = 37
            except ValueError:
                reportname = reportname.split('.')[1]

            filename = reportname

            if reportname in [
                'ssl_sale_ext.report_saleorder_document_ssl',
                'ssl_purchase_ext.report_purchases_document_ssl',
                'ssl_account_ext.report_invoices_document_ssl',
                'ssl_sale_ext.report_saleorder_document_pipeline',
            ]:
                for docids in _docids.split(','):
                    # Sales Order
                    s = 'ssl_sale_ext.report_saleorder_document_ssl'
                    if reportname == s:
                        sale_obj = http.request.env['sale.order']
                        object = sale_obj.browse(int(docids))

                        state_obj = object.state.encode('utf-8', 'ignore')
                        if state_obj in ['draft', 'sent', 'cancel']:
                            state_obj = 'Quotation'
                        elif state_obj in ['sale', 'done']:
                            state_obj = 'Sale Order'

                        filename = object.name.encode(
                            'utf-8', 'ignore') + '-' + state_obj

                    # Purchase Order
                    p = 'ssl_purchase_ext.report_purchases_document_ssl'
                    if reportname == p:
                        purchase_obj = http.request.env['purchase.order']
                        object = purchase_obj.browse(int(docids))
                        state_obj = object.state.encode('utf-8', 'ignore')
                        if state_obj in ['draft', 'sent', 'cancel']:
                            state_obj = 'Request for Quotation'
                        elif state_obj in ['purchase', 'done']:
                            state_obj = 'Purchase Order'
                        elif state_obj in ['to approve']:
                            state_obj = 'To Approve'

                        filename = object.name.encode(
                            'utf-8', 'ignore') + '-' + state_obj

                    # Account Invoice
                    i = 'ssl_account_ext.report_invoices_document_ssl'
                    if reportname == i:
                        invoice_obj = http.request.env['account.invoice']
                        object = invoice_obj.browse(int(docids))
                        state_obj = object.state.encode('utf-8', 'ignore')
                        type_obj = object.type.encode('utf-8', 'ignore')

                        if state_obj in [
                            'draft',
                            'proforma',
                            'proforma2',
                            'cancelled'
                        ] and type_obj == 'out_invoice':
                            state_obj = 'Proforma Invoice'
                        elif type_obj == 'in_invoice':
                            state_obj = 'Vendor Bill'
                        elif state_obj in ['open', 'paid'] and \
                                type_obj == 'out_invoice':
                            state_obj = 'Invoice'

                        if object.number:
                            filename = object.number.encode(
                                'utf-8', 'ignore') + '-' + state_obj
                        else:
                            filename = object.fal_draft_number.encode(
                                'utf-8', 'ignore') + '-' + state_obj
                    # Wishlist
                    w = 'ssl_sale_ext.report_saleorder_document_pipeline'
                    if reportname == w:
                        crm_obj = http.request.env['crm.lead']
                        object = crm_obj.browse(int(docids))

                        filename = object.fal_wishlist_number.encode(
                            'utf-8', 'ignore') + '-' + 'Wishlist'
                        # filename = SO0012

            filename = filename.replace(",", " ")
            response.headers.set(
                'Content-Disposition',
                'attachment; filename=%s.pdf' % filename)

        return response
