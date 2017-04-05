# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models
from odoo.exceptions import UserError
from odoo.tools.translate import _
import base64


class crm_docs_upload_signed(models.TransientModel):

    _name = 'crm.docs.upload.signed'

    greenloc_crm_lead_docs_sign_attachment_id = fields.Many2one('greenloc.crm.lead.docs.sign.attachment', string='Crm Docs')
    docs = fields.Binary('Document')
    docs_name = fields.Char()

    @api.multi
    def action_uploads(self):
        """ Upload document as attachment to corresponding Crm Docs
        """
        self.ensure_one()
        crm_doc_id = self.env['greenloc.crm.lead.docs.sign.attachment'].browse(self._context['active_id'])
        doc = self.env['ir.attachment'].create({
                    'name': self.docs_name,
                    'datas_fname': self.docs_name + '.pdf',
                    'datas': self.docs,
                    'type': 'binary',
                    'res_model': 'crm.lead',
                    'res_id': crm_doc_id.lead_id.id,
                    'res_name': crm_doc_id.lead_id.name,
                    'fal_lead_id': crm_doc_id.lead_id.id,
                    'fal_protected': True,
                })
        crm_doc_id.write({'signed_doc_id': doc.id, 'signed_doc_ids': [(4, doc.id)], 'version_signed': crm_doc_id.version_signed + 1})
