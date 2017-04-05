# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models
from odoo.exceptions import UserError
from odoo.tools.translate import _
import base64


class crm_re_send_model1_mail(models.TransientModel):

    _name = 'crm.re.send.model1.mail'

    # Re-send model1 email
    @api.multi
    def resend_model1_mail(self):
        # Should only accessed from RDV VT Stage\
        for lead in self.env['greenloc.crm.lead.docs.sign.attachment'].browse(self._context['active_ids']):
            template = self.env['ir.model.data'].xmlid_to_object('greenloc_crm_ext.lead_pdf_request_email')
            mail = template.send_mail(lead.id, force_send=True)
            self.env['mail.mail'].browse(mail).fal_lead_id = lead.id
        return True
