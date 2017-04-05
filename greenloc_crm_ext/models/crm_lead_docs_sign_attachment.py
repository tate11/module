# -*- coding: utf-8 -*-
from openerp import api, fields, models, _


class greenloc_crm_lead_docs_sign_attachment(models.Model):
    _name = 'greenloc.crm.lead.docs.sign.attachment'

    inactive = fields.Boolean("Inactive")
    lead_id = fields.Many2one("crm.lead", "lead")
    name = fields.Char("Document Name")
    code = fields.Char("Document Code")
    version = fields.Integer("Version Initial")
    version_signed = fields.Integer("Signed Version")
    initial_doc_ids = fields.One2many('ir.attachment', 'fal_greenloc_crm_lead_docs_initial_attachment', 'Initial Documents', domain=[('fal_protected', '=', False)])
    initial_doc_id = fields.Many2one('ir.attachment', 'Initial Document')
    initial_doc_id_binary = fields.Binary('Initial Document File', related="initial_doc_id.datas")
    initial_doc_id_fname = fields.Char('Initial Document Fname', related="initial_doc_id.datas_fname")
    signed_doc_ids = fields.One2many('ir.attachment', 'fal_greenloc_crm_lead_docs_sign_attachment', 'Signed Documents', domain=[('fal_protected', '=', True)])
    signed_doc_id = fields.Many2one('ir.attachment', 'Signed Document')
    signed_doc_id_binary = fields.Binary('Signed Document File', related="signed_doc_id.datas")
    signed_doc_id_fname = fields.Char('Signed Document Fname', related="signed_doc_id.datas_fname")


class greenloc_crm_universign(models.Model):
    _name = 'greenloc.crm.universign'

    lead_id = fields.Many2one("crm.lead", "lead", ondelete='cascade')
    fal_universign_login = fields.Char('Universign Login')
    fal_universign_server = fields.Char('Universign Server')
    fal_universign_type = fields.Selection([('reg', 'Regular'),
                                            ('l3', 'L3')], 'Document Type', default="reg")
    fal_universign_url = fields.Char('Universign URL')
    fal_universign_id = fields.Char('Universign ID')
    fal_universign_doc_received = fields.Boolean('Universign Received')
    fal_universign_doc_failed = fields.Selection([('expired', 'Expired'),
                                                  ('canceled', 'Canceled'),
                                                  ('failed', 'Failed')], 'Universign Failed')
