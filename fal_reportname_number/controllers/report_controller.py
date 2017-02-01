# -*- coding: utf-8 -*-

import pdb
# from odoo.addons.web.http import Controller, route, request
from odoo.addons.report.controllers.main import ReportController
from odoo import http

import simplejson


class FalReportController(http.Controller):

    @http.route(['/report/download'], auth="user")
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
                reportname, docids = reportname.split('/')
                assert docids
                # reportname = u'sale.report_saleorder'
                # docids = 37
            except ValueError:
                reportname = reportname.split('.')[1]

            filename = reportname

            if reportname in [
                'sale.report_saleorder',
                'purchase.report_purchaseorder',
                'account.report_invoice',
                'stock.report_picking',
                'mrp.report_mrporder',
                'hr_payroll.report_payslip',
                'hr_expense.report_expense'
            ]:
                if reportname == 'sale.report_saleorder':
                    sale_obj = http.request.env['sale.order']
                    object = sale_obj.browse(int(docids))

                    filename = object.name.encode('utf-8', 'ignore') + '-' + \
                        object.partner_id.name.encode('utf-8', 'ignore')
                    # filename = SO0012

                if reportname == 'purchase.report_purchaseorder':
                    purchase_obj = http.request.env['purchase.order']
                    object = purchase_obj.browse(int(docids))

                    filename = object.name.encode('utf-8', 'ignore') + '-' + \
                        object.partner_id.name.encode('utf-8', 'ignore')
                    # filename = SO0012

                if reportname == 'account.report_invoice':
                    invoice_obj = http.request.env['account.invoice']
                    object = invoice_obj.browse(int(docids))
                    if object.number:
                        filename = object.number.encode('utf-8', 'ignore') + \
                            '-' + object.partner_id.name.encode(
                                'utf-8', 'ignore')
                    # filename = SO0012

            filename = filename.replace(",", " ")
            response.headers.set(
                'Content-Disposition',
                'attachment; filename=%s.pdf' % filename)

        return response
