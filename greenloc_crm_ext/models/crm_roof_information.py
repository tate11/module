# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models


class greenloc_crm_roof_information(models.Model):

    _name = 'greenloc.crm.roof.information'

    name = fields.Char("Name")
    crm_lead_id = fields.Many2one("crm.lead", "Lead")
    roof_surface = fields.Integer("Roof Surface")
    sun_eyes_tools = fields.Integer("Sun Eyes Tools")
    sun_eyes_tools_pdf = fields.Binary(string="SunEyes Tool's PDF")
    sun_eyes_tools_pdf_fname = fields.Char("SunEyes Tool's PDF Fname")
