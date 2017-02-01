# -*- coding: utf-8 -*-
from datetime import datetime, date, timedelta

from odoo import fields, models, api, _
import time


class account_invoice(models.Model):
    _name = "account.invoice"
    _inherit = "account.invoice"

    def _create_invoice_reminder(self, ids=False, advance_date=3):
        if not ids:
            ids = self.search([])
        return self.create_invoice_reminder(ids, advance_date=advance_date)

    def create_invoice_reminder(self, ids, advance_dates=[3]):
        mail_obj = self.env['mail.mail']
        ir_attachment_obj = self.env['ir.attachment']
        for advance_date in advance_dates:
            advance_date = date.today() + timedelta(advance_date)
            invoice_due_ids = self.search([
                ('date_due', '=', advance_date),
                ('type', '=', 'out_invoice'),
                ('state', 'not in', ['draft', 'cancel', 'paid'])])
            template_id = self.env['ir.model.data'].\
                get_object_reference(
                    'fal_invoice_reminder',
                    'email_template_invoice_reminder')[1]
            if invoice_due_ids:
                for invoice_due_id in self.browse(invoice_due_ids):
                    if invoice_due_id.partner_id.invoice_reminder \
                            and invoice_due_id.partner_id.email:
                        self.env['email.template'].send_mail(
                            template_id, invoice_due_id.id, force_send=True)
        return True

# end of account_invoice()
