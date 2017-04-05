# -*- coding: utf-8 -*-
from openerp import api, fields, models, _


class greenloc_crm_lead_technical_visit(models.Model):
    _name = 'greenloc.crm.lead.technical.visit'

    lead_id = fields.Many2one("crm.lead", "Lead")
    date = fields.Datetime("Date")
    vt_realised = fields.Boolean("VT Realised")
    vt_validated = fields.Boolean("VT Validated")
    notes = fields.Text("Notes")
