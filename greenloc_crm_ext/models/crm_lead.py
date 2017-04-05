# -*- coding: utf-8 -*-
from openerp import api, fields, models, _
import base64
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT
from dateutil.relativedelta import relativedelta
from datetime import datetime, date, timedelta
from odoo.addons.greenloc_crm_ext.controllers import universign
from odoo.exceptions import UserError

CRM_LEAD_FIELDS_TO_MERGE = [
    'name',
    'partner_id',
    'campaign_id',
    'company_id',
    'country_id',
    'team_id',
    'state_id',
    'stage_id',
    'medium_id',
    'source_id',
    'user_id',
    'title',
    'city',
    'contact_name',
    'description',
    'email',
    'fax',
    'mobile',
    'partner_name',
    'phone',
    'probability',
    'planned_revenue',
    'street',
    'street2',
    'zip',
    'create_date',
    'date_action_last',
    'date_action_next',
    'email_from',
    'email_cc',
    'partner_name',
    'fal_model_1_pdf',
    'fal_model_1_pdf_fname']


class crm_lead(models.Model):
    _inherit = 'crm.lead'

    # Default Value
    def _get_roof_information_default(self):
        return [(0, 0,  {'name': _('Roof 1')}), (0, 0,  {'name': _('Roof 2')}), (0, 0,  {'name': _('Roof 3')}), (0, 0,  {'name': _('Roof 4')})]

    # Domain function
    @api.model
    def _getUserGroupId(self):
        technician_group = self.env.ref('greenloc_crm_ext.group_greenloc_technician').users.ids
        return [('id', 'in', technician_group)]

    # Adding some required field

    fal_sequence = fields.Char(string='Sequence',
                               copy=False)
    fal_quality_user_id = fields.Many2one("res.users", "Quality Person", track_visibility='onchange')
    fal_salesperson_user_id = fields.Many2one("res.users", "Validator Person", track_visibility='onchange')
    fal_lead_stage = fields.Selection([('draft', 'Draft'),
                                       ('new', 'New'),
                                       ('to_control', 'To Control'),
                                       ('affected', 'Affected')],
                                      string="Lead Stage", default='draft', track_visibility='onchange')
    fal_send_email_customer = fields.Boolean(string="Send Email to customer")
    fal_send_email_other = fields.Char(string="Also send Email to")
    fal_roof_surface = fields.Integer(string='Total Roof Surface', compute="_get_roof_surface_total")
    fal_sun_eyes_tools = fields.Float(string="Average Sun Eyes Tools", compute="_get_sun_eyes_average")
    fal_france_building = fields.Boolean(string='Is a France Building')
    fal_recall_reason = fields.Text(string="Recall Reason")
    fal_lost_reason = fields.Text(string="Lost Reason")
    fal_partner_child_ids = fields.One2many('res.partner', 'lead_id', string='Partner Contacts', related="partner_id.child_ids")
    fal_marital_status = fields.Selection([('married', 'Married'),
                                          ('single', 'Single'),
                                          ('widower', 'Widower',),
                                          ('pacs', 'Pacs'),
                                          ('concubinage', 'Concubinage')],
                                          string="Marital Status")
    fal_wedding_contract = fields.Char(string="Wedding Contract")
    fal_root_surface_pdf = fields.Binary(string="Root Surface's PDF")
    fal_root_surface_pdf_fname = fields.Char("Root Surface's PDF Fname")
    fal_sun_eyes_tools_pdf = fields.Binary(string="SunEyes Tool's PDF")
    fal_sun_eyes_tools_pdf_fname = fields.Char("SunEyes Tool's PDF Fname")
    fal_roof_information_ids = fields.One2many("greenloc.crm.roof.information", "crm_lead_id", "Roof Information", default=_get_roof_information_default)
    fal_solargis_csv = fields.Binary(string="Solargis CSV")
    fal_solargis_csv_fname = fields.Char("Solargis CSV Fname")
    fal_parcel_no = fields.Char(string="Parcell Number")
    fal_section = fields.Char(string="Section Number")
    fal_contenance_1 = fields.Integer(string="Contenance 1")
    fal_contenance_2 = fields.Integer(string="Contenance 2")
    fal_contenance_3 = fields.Integer(string="Contenance 3")
    fal_place_says = fields.Char(string="Place Says")
    fal_goods = fields.Selection([('common', 'common'),
                                  ('clean', 'Clean')], string="Goods")
    fal_ownership = fields.Selection([('alone', 'Alone'),
                                      ('indivision', 'Indivision'),
                                      ('co_ownership_or_similar', 'Co-ownership or similar'),
                                      ('usufruct_and_bare_ownership', 'Usufruct and bare ownership'),
                                      ('right_of_use_and_habitation', 'Right of use and habitation')], string="Ownership")
    fal_model_1_pdf = fields.Binary(string="Model 1's PDF")
    fal_model_1_pdf_fname = fields.Char("Model 1's PDF Fname")
    fal_cadastre_pdf = fields.Binary(string="Cadastre's PDF")
    fal_cadastre_pdf_fname = fields.Char("Cadastre's PDF Fname")
    fal_quality_team_notes = fields.Text(string="QT Notes", help="Quality Team's Notes")
    fal_mail_ids = fields.One2many('mail.mail', 'fal_lead_id', string="Mail")
    fal_is_dia = fields.Boolean('Different Installation Address')
    fal_dia_street = fields.Char('Installation Address', compute="_get_fal_dia_street", inverse="_set_fal_dia_street")
    fal_dia_street2 = fields.Char('Installation Address 2', compute="_get_fal_dia_street2", inverse="_set_fal_dia_street2")
    fal_dia_city = fields.Char('Installation City', compute="_get_fal_dia_city", inverse="_set_fal_dia_city")
    fal_dia_state = fields.Many2one("res.country.state", 'Installation State', compute="_get_fal_dia_state", inverse="_set_fal_dia_state", ondelete='restrict')
    fal_dia_zip = fields.Char('Installation Zip', compute="_get_fal_dia_zip", inverse="_set_fal_dia_zip")
    fal_dia_country_id = fields.Many2one('res.country', 'Installation Country', compute="_get_fal_dia_country", inverse="_set_fal_dia_country", ondelete='restrict')
    fal_dia_depart_no = fields.Char(string="Department N°", compute='_compute_department_no', store=True)
    fal_dia_partner_latitude = fields.Float(string='Geo Latitude', digits=(16, 5))
    fal_dia_partner_longitude = fields.Float(string='Geo Longitude', digits=(16, 5))
    fal_dia_date_localization = fields.Date(string='Geolocation Date')
    fal_last_date_signature_request = fields.Date("Last Signature Request at")
    fal_website_form_result = fields.Selection([('lost', 'Lost'),
                                                ('won', 'Won'),
                                                ('recall', 'Recall')], 'Website Result')
    fal_document_signature_ids = fields.One2many('greenloc.crm.lead.docs.sign.attachment', 'lead_id', 'Signature Documents')
    fal_crm_universign_ids = fields.One2many('greenloc.crm.universign', 'lead_id', 'Universign')
    fal_is_complex = fields.Boolean('Is Complex')
    fal_is_rdvvt = fields.Boolean('Is RDV VT')
    fal_is_l3 = fields.Boolean('Is L3')
    fal_lead_origin = fields.Selection([('fo', 'FO'),
                                        ('grl', 'GRL'),
                                        ('prl', 'PRL'),
                                        ('ntc', 'NTC')], 'Lead Origin')
    fal_technical_visit_ids = fields.One2many("greenloc.crm.lead.technical.visit", 'lead_id', 'Technical Visit')
    fal_no_of_recall = fields.Integer("Number of Recall", default=0)
    technician_id = fields.Many2one("res.users", "VT Technician", domain=_getUserGroupId)
    # Relate field email and phone
    email_from = fields.Char(related="partner_id.email")
    phone = fields.Char(related="partner_id.phone")
    mobile = fields.Char(related="partner_id.mobile")

    # Remove later if it's not needed
    # fal_signature_request_ids = fields.One2many('signature.request', 'fal_lead_id', 'Sign Documents')

    # Compute Method
    @api.one
    @api.depends('fal_dia_zip')
    def _compute_department_no(self):
        if self.fal_dia_zip:
            self.fal_dia_depart_no = self.fal_dia_zip[0:2]

    @api.one
    @api.depends('fal_roof_information_ids', 'fal_roof_information_ids.roof_surface')
    def _get_roof_surface_total(self):
        if self.fal_roof_information_ids:
            total_roof_surface = 0
            for fal_roof_information_id in self.fal_roof_information_ids:
                total_roof_surface += fal_roof_information_id.roof_surface
            self.fal_roof_surface = total_roof_surface

    @api.one
    @api.depends('fal_roof_information_ids', 'fal_roof_information_ids.roof_surface', 'fal_roof_information_ids.sun_eyes_tools')
    def _get_sun_eyes_average(self):
        if self.fal_roof_information_ids:
            average_sun_eyes_tools = 0
            total_roof_surface = 0
            for fal_roof_information_id in self.fal_roof_information_ids:
                average_sun_eyes_tools += fal_roof_information_id.roof_surface * fal_roof_information_id.sun_eyes_tools
                total_roof_surface += fal_roof_information_id.roof_surface
            if total_roof_surface != 0:
                self.fal_sun_eyes_tools = average_sun_eyes_tools / total_roof_surface
            else:
                self.fal_sun_eyes_tools = average_sun_eyes_tools / 1

    @api.one
    @api.depends('fal_partner_child_ids', 'fal_partner_child_ids.state_id')
    def _get_fal_dia_state(self):
        if self.fal_partner_child_ids:
            for fal_partner_child_id in self.fal_partner_child_ids:
                if fal_partner_child_id.type == 'other' and (fal_partner_child_id.name and fal_partner_child_id.name.lower() in ["adresse d'installation", "addresse d'installation", "installation address"]):
                    self.fal_dia_state = fal_partner_child_id.state_id and fal_partner_child_id.state_id.id or False

    @api.one
    def _set_fal_dia_state(self):
        for fal_partner_child_id in self.fal_partner_child_ids:
            if fal_partner_child_id.type == 'other' and (fal_partner_child_id.name and fal_partner_child_id.name.lower() in ["adresse d'installation", "addresse d'installation", "installation address"]):
                fal_partner_child_id.state_id = self.fal_dia_state and self.fal_dia_state.id or False

    @api.one
    @api.depends('fal_partner_child_ids', 'fal_partner_child_ids.street')
    def _get_fal_dia_street(self):
        if self.fal_partner_child_ids:
            for fal_partner_child_id in self.fal_partner_child_ids:
                if fal_partner_child_id.type == 'other' and (fal_partner_child_id.name and fal_partner_child_id.name.lower() in ["adresse d'installation", "addresse d'installation", "installation address"]):
                    self.fal_dia_street = fal_partner_child_id.street

    @api.one
    def _set_fal_dia_street(self):
        for fal_partner_child_id in self.fal_partner_child_ids:
            if fal_partner_child_id.type == 'other' and (fal_partner_child_id.name and fal_partner_child_id.name.lower() in ["adresse d'installation", "addresse d'installation", "installation address"]):
                fal_partner_child_id.street = self.fal_dia_street

    @api.one
    @api.depends('fal_partner_child_ids', 'fal_partner_child_ids.street2')
    def _get_fal_dia_street2(self):
        if self.fal_partner_child_ids:
            for fal_partner_child_id in self.fal_partner_child_ids:
                if fal_partner_child_id.type == 'other' and (fal_partner_child_id.name and fal_partner_child_id.name.lower() in ["adresse d'installation", "addresse d'installation", "installation address"]):
                    self.fal_dia_street2 = fal_partner_child_id.street2

    @api.one
    def _set_fal_dia_street2(self):
        for fal_partner_child_id in self.fal_partner_child_ids:
            if fal_partner_child_id.type == 'other' and (fal_partner_child_id.name and fal_partner_child_id.name.lower() in ["adresse d'installation", "addresse d'installation", "installation address"]):
                fal_partner_child_id.street2 = self.fal_dia_street2

    @api.one
    @api.depends('fal_partner_child_ids', 'fal_partner_child_ids.city')
    def _get_fal_dia_city(self):
        if self.fal_partner_child_ids:
            for fal_partner_child_id in self.fal_partner_child_ids:
                if fal_partner_child_id.type == 'other' and (fal_partner_child_id.name and fal_partner_child_id.name.lower() in ["adresse d'installation", "addresse d'installation", "installation address"]):
                    self.fal_dia_city = fal_partner_child_id.city

    @api.one
    def _set_fal_dia_city(self):
        for fal_partner_child_id in self.fal_partner_child_ids:
            if fal_partner_child_id.type == 'other' and (fal_partner_child_id.name and fal_partner_child_id.name.lower() in ["adresse d'installation", "addresse d'installation", "installation address"]):
                fal_partner_child_id.city = self.fal_dia_city

    @api.one
    @api.depends('fal_partner_child_ids', 'fal_partner_child_ids.zip')
    def _get_fal_dia_zip(self):
        if self.fal_partner_child_ids:
            for fal_partner_child_id in self.fal_partner_child_ids:
                if fal_partner_child_id.type == 'other' and (fal_partner_child_id.name and fal_partner_child_id.name.lower() in ["adresse d'installation", "addresse d'installation", "installation address"]):
                    self.fal_dia_zip = fal_partner_child_id.zip

    @api.one
    def _set_fal_dia_zip(self):
        for fal_partner_child_id in self.fal_partner_child_ids:
            if fal_partner_child_id.type == 'other' and (fal_partner_child_id.name and fal_partner_child_id.name.lower() in ["adresse d'installation", "addresse d'installation", "installation address"]):
                fal_partner_child_id.zip = self.fal_dia_zip

    @api.one
    @api.depends('fal_partner_child_ids', 'fal_partner_child_ids.country_id')
    def _get_fal_dia_country(self):
        if self.fal_partner_child_ids:
            for fal_partner_child_id in self.fal_partner_child_ids:
                if fal_partner_child_id.type == 'other' and (fal_partner_child_id.name and fal_partner_child_id.name.lower() in ["adresse d'installation", "addresse d'installation", "installation address"]):
                    self.fal_dia_country_id = fal_partner_child_id.country_id and fal_partner_child_id.country_id.id or False

    @api.one
    def _set_fal_dia_country(self):
        for fal_partner_child_id in self.fal_partner_child_ids:
            if fal_partner_child_id.type == 'other' and (fal_partner_child_id.name and fal_partner_child_id.name.lower() in ["adresse d'installation", "addresse d'installation", "installation address"]):
                fal_partner_child_id.country_id = self.fal_dia_country_id and self.fal_dia_country_id.id or False

    # Re-send model1 mail
    @api.multi
    def re_send_model1_mail(self):
        template = self.env['ir.model.data'].xmlid_to_object('greenloc_crm_ext.lead_pdf_request_email')
        mail = template.send_mail(self.id, force_send=True)
        self.env['mail.mail'].browse(mail).fal_lead_id = self.id
        return True

    # Call Geolocation of Partner
    @api.multi
    def lead_geo_localize(self):
        # Call Installation Address Geolocation method, copy the value of partner to lead
        for lead in self:
            for fal_partner_child_id in lead.fal_partner_child_ids:
                if fal_partner_child_id.type == 'other' and (fal_partner_child_id.name and fal_partner_child_id.name.lower() in ["adresse d'installation", "addresse d'installation", "installation address"]):
                    if fal_partner_child_id.geo_localize():
                        lead.fal_dia_partner_latitude = fal_partner_child_id.partner_latitude
                        lead.fal_dia_partner_longitude = fal_partner_child_id.partner_longitude
                        lead.fal_dia_date_localization = fal_partner_child_id.date_localization

    # Merge lead with head selected.
    @api.multi
    def merge_opportunity(self, user_id=False, team_id=False):
        """ Merge opportunities in one. Different cases of merge:
                - merge leads together = 1 new lead
                - merge at least 1 opp with anything else (lead or opp) = 1 new opp
            The resulting lead/opportunity will be the most important one (based on its confidence level)
            updated with values from other opportunities to merge.
            :param user_id : the id of the saleperson. If not given, will be determined by `_merge_data`.
            :param team : the id of the sales team. If not given, will be determined by `_merge_data`.
            :return crm.lead record resulting of th merge
        """
        if len(self.ids) <= 1:
            raise UserError(_('Please select more than one element (lead or opportunity) from the list view.'))

        # Sorting the leads/opps according to the confidence level of its stage, which relates to the probability of winning it
        # The confidence level increases with the stage sequence, except when the stage probability is 0.0 (Lost cases)
        # An Opportunity always has higher confidence level than a lead, unless its stage probability is 0.0
        def opps_key(opportunity):
            sequence = -1
            if opportunity.stage_id.on_change:
                sequence = opportunity.stage_id.sequence
            return (sequence != -1 and opportunity.type == 'opportunity'), sequence, -opportunity.id
        opportunities = self.sorted(key=opps_key, reverse=True)

        # get SORTED recordset of head and tail, and complete list
        opportunities_head = opportunities[0]
        opportunities_tail = opportunities[1:]

        # Override Falinwa Greenloc
        # If head is defined in merge, use it.
        if 'head_selected' in self.env.context and self.env.context['head_selected']:
            opportunities_head = self.env.context['head_selected']
            opportunities_tail = False
            opportunities_tail = self.browse()
            for opportunity in opportunities:
                if not opportunity == opportunities_head:
                    opportunities_tail += opportunity
            opportunities = opportunities_head + opportunities_tail

        # merge all the sorted opportunity. This means the value of
        # the first (head opp) will be a priority.
        merged_data = opportunities._merge_data(list(CRM_LEAD_FIELDS_TO_MERGE))

        # force value for saleperson and sales team
        if user_id:
            merged_data['user_id'] = user_id
        if team_id:
            merged_data['team_id'] = team_id

        # merge other data (mail.message, attachments, ...) from tail into head
        opportunities_head.merge_dependences(opportunities_tail)

        # check if the stage is in the stages of the sales team. If not, assign the stage with the lowest sequence
        if merged_data.get('team_id'):
            team_stage_ids = self.env['crm.stage'].search(['|', ('team_id', '=', merged_data['team_id']), ('team_id', '=', False)], order='sequence')
            if merged_data.get('stage_id') not in team_stage_ids.ids:
                merged_data['stage_id'] = team_stage_ids[0].id if team_stage_ids else False

        # write merged data into first opportunity
        opportunities_head.write(merged_data)

        # delete tail opportunities
        # we use the SUPERUSER to avoid access rights issues because as the user had the rights to see the records it should be safe to do so
        opportunities_tail.sudo().unlink()

        return opportunities_head

    # Action Phone Call
    @api.multi
    def action_phone_call(self):
        """ Link to open sent appraisal"""
        self.ensure_one()
        return {
            "type": "ir.actions.act_url",
            "url": "http://192.168.1.218/apicall.php?dest=" + str(self.phone) + "&poste=" + str(self.env['res.users'].browse(self._uid).partner_id.phone),
            "target": "new",
        }

    # Action Mobile Call
    @api.multi
    def action_mobile_call(self):
        """ Link to open sent appraisal"""
        self.ensure_one()
        return {
            "type": "ir.actions.act_url",
            "url": "http://192.168.1.218/apicall.php?dest=" + str(self.mobile) + "&poste=" + str(self.env['res.users'].browse(self._uid).partner_id.phone),
            "target": "new",
        }

    # Action Fetch Mail
    @api.multi
    def fetch_pdf_email_from_greenloc(self):
        attachment_name = self.env.context['attachment_name']
        lead_id = self.env.context['active_id']
        attachment_id = self.env['ir.attachment'].search([('res_id', '=', lead_id), ('res_model', '=', 'crm.lead'), ('name', '=', attachment_name)], limit=1)
        self.browse(lead_id).fal_model_1_pdf = attachment_id.datas
        self.browse(lead_id).fal_model_1_pdf_fname = attachment_name
        self.browse(lead_id).action_set_to_control_lead_stage()

    # Affect Lead or Opportunity
    @api.model
    def affect_lead_quality(self):
        lead_id = self.env['crm.lead'].search([('active', '=', True), ('type', '=', 'lead'), ('fal_lead_stage', '=', 'affected'), ('fal_quality_user_id', '=', self.env.uid), ('fal_is_complex', '=', False)], order='write_date asc', limit=1)
        if not lead_id:
            lead_id = self.env['crm.lead'].search([('active', '=', True), ('type', '=', 'lead'), ('fal_lead_stage', '=', 'to_control'), ('fal_quality_user_id', '=', False), ('fal_is_complex', '=', False)], order='write_date asc', limit=1)
        if lead_id:
            view_id = self.env['ir.model.data'].get_object_reference('greenloc_crm_ext', 'crm_case_form_view_leads_greenloc')[1]
            lead_id.action_set_to_affected_lead_stage()
            return {
                "type": "ir.actions.act_window",
                "res_model": "crm.lead",
                "view_mode": "form",
                "view_type": "form",
                "view_id": view_id,
                "res_id": lead_id.id,
                "tag": 'reload',
                'target': 'current',
            }
        return {
                'type': 'ir.actions.act_url',
                'target': 'self',
                'url': '/web',
            }

    @api.model
    def affect_opportunity_salesperson(self):
        new_stage = self.env['ir.model.data'].xmlid_to_object('crm.stage_lead1').id
        lead_id = self.env['crm.lead'].search([('active', '=', True), ('type', '=', 'opportunity'), ('stage_id', '=', new_stage), ('fal_salesperson_user_id', '=', False), ('fal_is_complex', '=', False)], order='write_date asc', limit=1)
        if lead_id:
            view_id = self.env['ir.model.data'].get_object_reference('greenloc_crm_ext', 'crm_case_form_view_oppor_greenloc')[1]
            lead_id.action_set_next_stage()
            lead_id.fal_salesperson_user_id = self._uid
            return {
                "type": "ir.actions.act_window",
                "res_model": "crm.lead",
                "view_mode": "form",
                "view_type": "form",
                "view_id": view_id,
                "res_id": lead_id.id,
                "tag": 'reload',
                'target': 'current',
            }
        return {
                'type': 'ir.actions.act_url',
                'target': 'self',
                'url': '/web',
            }

    # Skip crm.lead2ooprtunity
    @api.multi
    def action_fast_convert_to_opportunity(self):
        self.ensure_one()
        for lead in self:
            crm_lead_2_opportunity_values = {
                'team_id': self.env['res.users'].browse(self._uid).sale_team_id.id or lead.team_id.id or False,
                'action': 'create',
                'opportunity_ids': [(4, lead.id)],
                'name': 'convert',
                'user_id': self._uid}
            self.env['crm.lead2opportunity.partner'].sudo().create(crm_lead_2_opportunity_values).with_context(active_ids=[lead.id]).action_apply()
            template = self.env['ir.model.data'].xmlid_to_object('greenloc_crm_ext.new_opportunity_greenloc_email')
            mail = template.send_mail(lead.id, force_send=True)
            self.env['mail.mail'].browse(mail).fal_lead_id = lead.id
            if self.env['res.users'].browse(self._uid).has_group('sales_team.group_sale_manager'):
                return lead.redirect_opportunity_view()
            else:
                return self.affect_lead_quality()

    # Action Methods (Change Stage for Leads)
    @api.multi
    def action_set_to_draft_lead_stage(self):
        for lead in self:
            lead.write({'fal_lead_stage': 'draft', 'fal_quality_user_id': False})
            if self.env['res.users'].browse(self._uid).has_group('sales_team.group_sale_manager'):
                return True
            else:
                return self.affect_lead_quality()
        return True

    @api.multi
    def action_set_to_new_lead_stage(self):
        for lead in self:
            lead.write({'fal_lead_stage': 'new', 'user_id': self._uid})
        menu_ids = self.env.ref('greenloc_crm_ext.greenloc_menu_crm_leads_operator').id
        if self.env['res.users'].browse(self._uid).has_group('sales_team.group_sale_manager'):
            return True
        else:
            return {
                'type': 'ir.actions.client',
                'tag': 'reload',
                'params': {'menu_id': menu_ids or False},
                'target': 'current',
            }
        return True

    @api.multi
    def action_set_to_control_lead_stage(self):
        for lead in self:
            lead.write({'fal_lead_stage': 'to_control'})
        menu_ids = self.env.ref('greenloc_crm_ext.greenloc_menu_crm_leads_operator').id
        if self.env['res.users'].browse(self._uid).has_group('sales_team.group_sale_manager'):
            return True
        else:
            return {
                'type': 'ir.actions.client',
                'tag': 'reload',
                'params': {'menu_id': menu_ids or False},
                'target': 'current',
            }
        return True

    @api.multi
    def action_set_to_affected_lead_stage(self):
        for lead in self:
            lead.write({'fal_lead_stage': 'affected', 'fal_quality_user_id': self._uid})
            # We don't need it anymore
            # template = self.env['ir.model.data'].xmlid_to_object('greenloc_crm_ext.lead_to_affected_email')
            # mail = template.send_mail(lead.id, force_send=True)
            # self.env['mail.mail'].browse(mail).fal_lead_id = lead.id
        return True

    @api.multi
    def action_set_lost(self):
        """ Lost semantic: probability = 0, active = False """
        self.write({'probability': 0, 'active': False})
        # Send Email to customer
        if self.fal_lead_stage == 'affected' and self.type == 'lead':
            template = self.env['ir.model.data'].xmlid_to_object('greenloc_crm_ext.lost_opportunity_greenloc_email')
            mail = template.send_mail(self.id, force_send=True)
            self.env['mail.mail'].browse(mail).fal_lead_id = self.id
        if self.env['res.users'].browse(self._uid).has_group('sales_team.group_sale_manager'):
            return True
        elif 'view_form_source' in self.env.context and self.env.context['view_form_source'] == 'lead':
            return self.affect_lead_quality()
        else:
            if self.env['res.users'].browse(self._uid).has_group('greenloc_crm_ext.group_greenloc_salesperson'):
                menu_ids = self.env.ref('greenloc_crm_ext.greenloc_menu_crm_opportunity_salesperson').id
                return {
                    'type': 'ir.actions.client',
                    'tag': 'reload',
                    'params': {'menu_id': menu_ids or False},
                    'target': 'current',
                }
            else:
                return {
                    'type': 'ir.actions.act_url',
                    'target': 'self',
                    'url': '/web',
                }

    @api.multi
    def action_set_won(self):
        """ Won semantic: probability = 100 (active untouched) """
        for lead in self:
            stage_id = lead._stage_find(domain=[('probability', '=', 100.0), ('on_change', '=', True)])
            lead.write({'stage_id': stage_id.id, 'probability': 100})
            # Send Email To Customer
            attachment_ids = []
            for document_sign in lead.fal_document_signature_ids:
                if not document_sign.inactive:
                    if document_sign.signed_doc_id:
                        attachment = document_sign.signed_doc_id
                        attachment_ids.append(attachment.id)
            email_values = {'attachment_ids': attachment_ids}
            template = self.env['ir.model.data'].xmlid_to_object('greenloc_crm_ext.opportunity_to_won_email')
            mail = template.with_context().send_mail(self.id, force_send=True, email_values=email_values)
            self.env['mail.mail'].browse(mail).fal_lead_id = self.id
        return True

    # Action Methods (Change Stage)
    @api.multi
    def action_set_l3_stage(self):
        for lead in self:
            stage_id = self.env.ref('greenloc_crm_ext.greenloc_lead_workflow_6')
            lead.write({'stage_id': stage_id.id, 'fal_is_l3': True})
        return True

    @api.multi
    def action_set_l3_to_rdvvt_stage(self):
        # Should only accessed from RDV VT Stage
        for lead in self:
            stage_id = self.env.ref('greenloc_crm_ext.greenloc_lead_workflow_5')
            lead.write({'stage_id': stage_id.id, 'fal_is_l3': False})
        return True

    @api.multi
    def action_set_rdvvt_stage(self):
        for lead in self:
            stage_id = self.env.ref('greenloc_crm_ext.greenloc_lead_workflow_5')
            # Check VT Technician Login
            if lead.technician_id and lead.technician_id.fal_universign_login and lead.technician_id.fal_universign_password:
                lead.generate_documents_rdvvt()
                lead.write({'stage_id': stage_id.id, 'fal_is_rdvvt': True})
            else:
                raise UserError(_("Please provide Technician in the Lead, also make sure Universign login and password is set on the technician user."))
        return True

    @api.multi
    def action_set_rdvvt_to_won__stage(self):
        # Should only accessed from RDV VT Stage
        for lead in self:
            stage_id = lead._stage_find(domain=[('probability', '=', 100.0), ('on_change', '=', True)])
            lead.write({'stage_id': stage_id.id, 'probability': 100, 'fal_is_rdvvt': False})
        return True

    @api.multi
    def action_set_next_stage(self):
        for lead in self:
            stage_id = lead._stage_find(domain=[('probability', '>', lead.probability), ('on_change', '=', True)])
            lead.write({'stage_id': stage_id.id, 'probability': stage_id.probability})
        return True

    @api.multi
    def action_set_opportunity_new(self):
        for lead in self:
            new_stage = self.env.ref('crm.stage_lead1')
            lead.write({'stage_id': new_stage.id, 'probability': new_stage.probability, 'fal_no_of_recall': (lead.fal_no_of_recall + 1)})
            self.fal_salesperson_user_id = False
            if self.env['res.users'].browse(self._uid).has_group('sales_team.group_sale_manager'):
                return True
            else:
                menu_ids = self.env.ref('greenloc_crm_ext.greenloc_menu_crm_opportunity_salesperson').id
                return {
                        'type': 'ir.actions.client',
                        'tag': 'reload',
                        'params': {'menu_id': menu_ids or False},
                        'target': 'current',
                    }
        return True

    @api.multi
    def action_set_prev_stage(self):
        for lead in self:
            stage_id = lead._stage_find(domain=[('probability', '<', lead.probability), ('on_change', '=', True)], order="sequence desc")
            lead.write({'stage_id': stage_id.id, 'probability': stage_id.probability})
            if stage_id == self.env.ref('crm.stage_lead1'):
                self.fal_salesperson_user_id = False
                if self.env['res.users'].browse(self._uid).has_group('sales_team.group_sale_manager'):
                    return True
                else:
                    menu_ids = self.env.ref('greenloc_crm_ext.greenloc_menu_crm_opportunity_salesperson').id
                    return {
                            'type': 'ir.actions.client',
                            'tag': 'reload',
                            'params': {'menu_id': menu_ids or False},
                            'target': 'current',
                        }
        return True

    @api.multi
    def _onchange_partner_id_values(self, partner_id):
        """Recover first and last names from partner if available."""
        result = super(crm_lead, self)._onchange_partner_id_values(partner_id)
        if partner_id:
            partner = self.env["res.partner"].browse(partner_id)
            if not partner.is_company:
                result.update({
                    "contact_name": partner.firstname,
                    "contact_lastname": partner.lastname,
                    "fal_marital_status": partner.fal_marital_status,
                    "fal_wedding_contract": partner.fal_wedding_contract,
                })

        return result

    def send_mail_model1_pdf(self):
        template = self.env['ir.model.data'].xmlid_to_object('greenloc_crm_ext.lead_pdf_request_email')
        mail = template.send_mail(self.id, force_send=True)
        self.env['mail.mail'].browse(mail).fal_lead_id = self.id
        return True

    @api.model
    def create(self, vals):
        vals['fal_sequence'] = self.env['ir.sequence'].next_by_code('crm.lead') or 'New'
        result = super(crm_lead, self).create(vals)
        # Give new Name, if it's from website, otherwise it should be from import. Do not change the name
        if result.fal_website_form_result:
            record_new_name = "GRL_" + str(result.fal_sequence)
            if result.partner_id.company_type == 'person':
                record_new_name += " - PART - "
            else:
                record_new_name += " - PRO - "
            if result.fal_is_complex:
                record_new_name += result.partner_id.name
            else:
                record_new_name += result.partner_id.lastname + "/" + result.partner_id.firstname
            result.update({'name': record_new_name})
        # Send Email to greenloc to generate PDF
        result.send_mail_model1_pdf()
        return result

    # Block writing on fal_lead_origin if you are not admin
    @api.multi
    def write(self, vals):
        partner_id = False
        if 'partner_id' in vals:
            partner_id = vals['partner_id']
        if ('fal_lead_origin' in vals or (partner_id and partner_id != self.partner_id.id)) and not self.env['res.users'].browse(self._uid).has_group('base.group_erp_manager'):
            raise UserError(_("Only User with group : Administration(Access Right) can edit Lead Origin or Customer."))
        return super(crm_lead, self).write(vals)

    # Send document to universign
    @api.multi
    def send_to_universign(self, universign_docs=False, universign_signers=False, main_partner=False):
        universign_connector = universign.UniversignConnector()
        # Removing False value on signers
        if universign_signers:
            for universign_signer in universign_signers:
                for key in universign_signer:
                    if universign_signer[key] == False:
                        universign_signer.pop(key, None)
        result = universign_connector.request_sign(universign_name=self.name, universign_docs=universign_docs, universign_signers=universign_signers)
        self.fal_crm_universign_ids = [(0, 0, {'lead_id': self.id, 'fal_universign_url': result['url'], 'fal_universign_id': result['id'], 'fal_universign_login': "candidature.greenloc@green-loc.fr", 'fal_universign_server': '@ws.universign.eu/sign/rpc/', 'fal_universign_type': 'reg'})]
        if result:
            email_to = universign_signers[0]['emailAddress']
            template = self.env['ir.model.data'].xmlid_to_object('greenloc_crm_ext.universign_greenloc_email')

            attachment_ids = []
            for document_sign in universign_docs:
                attachment = self.env['ir.attachment'].search([('name', '=', document_sign['name'])], limit=1)
                attachment_ids.append(attachment.id)
            email_values = {'attachment_ids': attachment_ids}
            mail = template.with_context(email_to=email_to).send_mail(self.id, force_send=True, email_values=email_values)
            self.env['mail.mail'].browse(mail).fal_lead_id = self.id

    # Send document to universign Rdvvt
    @api.multi
    def send_rdvvt_to_universign(self, universign_docs=False, universign_signers=False, main_partner=False):
        universign_connector = universign.UniversignConnector()
        # Removing False value on signers
        if universign_signers:
            for universign_signer in universign_signers:
                for key in universign_signer:
                    if universign_signer[key] == False:
                        universign_signer.pop(key, None)
        result = universign_connector.request_sign_l3(universign_name=self.name, universign_docs=universign_docs, universign_signers=universign_signers, universign_login=self.technician_id.fal_universign_login, universign_password=self.technician_id.fal_universign_password)
        self.fal_crm_universign_ids = [(0, 0, {'lead_id': self.id, 'fal_universign_url': result['url'], 'fal_universign_id': result['id'], 'fal_universign_login': self.technician_id.fal_universign_login, 'fal_universign_server': '@sign.test.cryptolog.com/sign/rpc/', 'fal_universign_type': 'l3'})]

    # Cron to receive from universign
    @api.model
    def cron_receive_universign(self, universign_docs=False, universign_signers=False):
        universign_connector = universign.UniversignConnector()
        tehcnician_vt = [(technician.fal_universign_login, technician.fal_universign_password) for technician in self.env['res.users'].search([('fal_universign_login', '!=', False), ('fal_universign_password', '!=', False)])]
        # Universign 1st Doc
        for lead_universign in self.env['greenloc.crm.universign'].search([('fal_universign_id', '!=', False), ('fal_universign_doc_received', '=', False), ('fal_universign_doc_failed', '=', False), ('lead_id', '!=', False), ('fal_universign_type', '=', 'reg')]):
            results = universign_connector.request_get(universign_id=lead_universign.fal_universign_id, lead_id=lead_universign.lead_id.id, technician=tehcnician_vt)
            if results in ['expired', 'canceled', 'failed']:
                affected_stage = self.env.ref('greenloc_crm_ext.greenloc_lead_workflow_1')
                lead_universign.lead_id.write({'stage_id': affected_stage.id, 'probability': affected_stage.probability})
                lead_universign.fal_universign_doc_failed = results
            if results and results not in ['expired', 'canceled', 'failed']:
                for result in results:
                    attachment = self.env['ir.attachment'].create({
                        'name': 'Signed - ' + result,
                        'datas_fname': 'Signed - ' + result + '.pdf',
                        'datas': results[result],
                        'type': 'binary',
                        'res_model': 'crm.lead',
                        'fal_protected': True,
                        'res_model': 'crm.lead',
                        'res_id': lead_universign.lead_id.id,
                        'res_name': lead_universign.lead_id.name,
                        'fal_lead_id': lead_universign.lead_id.id,
                    })
                    match_doc = self.env['ir.attachment'].search([('name', '=', result)], limit=1)
                    if match_doc:
                        greenloc_docs = match_doc.fal_greenloc_crm_lead_docs_initial_attachment
                        greenloc_docs.signed_doc_ids = [(4, attachment.id)]
                        greenloc_docs.signed_doc_id = attachment.id
                        greenloc_docs.signed_doc_id_binary = attachment.datas
                        greenloc_docs.signed_doc_id_fname = attachment.datas_fname
                lead_universign.fal_universign_doc_received = True
                lead_universign.lead_id.action_set_won()
        # Universign L3 Doc
        for lead_universign in self.env['greenloc.crm.universign'].search([('fal_universign_id', '!=', False), ('fal_universign_doc_received', '=', False), ('fal_universign_doc_failed', '=', False), ('lead_id', '!=', False), ('fal_universign_type', '=', 'l3')]):
            results = universign_connector.request_get(universign_id=lead_universign.fal_universign_id, lead_id=lead_universign.lead_id.id, technician=tehcnician_vt)
            if results in ['expired', 'canceled', 'failed']:
                lead_universign.fal_universign_doc_failed = results
            if results and results not in ['expired', 'canceled', 'failed']:
                for result in results:
                    attachment = self.env['ir.attachment'].create({
                        'name': 'Signed - ' + result,
                        'datas_fname': 'Signed - ' + result + '.pdf',
                        'datas': results[result],
                        'type': 'binary',
                        'res_model': 'crm.lead',
                        'fal_protected': True,
                        'res_model': 'crm.lead',
                        'res_id': lead_universign.lead_id.id,
                        'res_name': lead_universign.lead_id.name,
                        'fal_lead_id': lead_universign.lead_id.id,
                    })
                    match_doc = self.env['ir.attachment'].search([('name', '=', result)], limit=1)
                    if match_doc:
                        greenloc_docs = match_doc.fal_greenloc_crm_lead_docs_initial_attachment
                        greenloc_docs.signed_doc_ids = [(4, attachment.id)]
                        greenloc_docs.signed_doc_id = attachment.id
                        greenloc_docs.signed_doc_id_binary = attachment.datas
                        greenloc_docs.signed_doc_id_fname = attachment.datas_fname
                lead_universign.fal_universign_doc_received = True
                lead_universign.lead_id.action_set_l3_stage()

    # Generate neccesary document
    @api.multi
    def generate_documents(self):
        self.ensure_one()
        self.fal_last_date_signature_request = fields.Date.today()
        universign_docs = []
        universign_signers = []
        # For annexe 7
        partner_date_format = self.partner_id.lang and self.env['res.lang'].search([('code', '=', self.partner_id.lang)], limit=1).date_format or DEFAULT_SERVER_DATE_FORMAT
        # Plus 10 years 6 month
        dateplus10years = datetime.strptime(self.fal_last_date_signature_request, DEFAULT_SERVER_DATE_FORMAT) + relativedelta(years=10, months=6)
        dateplus10years = datetime.strftime(dateplus10years, partner_date_format)
        # Plus 10 years 6 month min 1 days
        dateplus10yearsmin1days = datetime.strptime(self.fal_last_date_signature_request, DEFAULT_SERVER_DATE_FORMAT) + relativedelta(years=10, months=6)
        dateplus10yearsmin1days = dateplus10yearsmin1days - relativedelta(days=1)
        dateplus10yearsmin1days = datetime.strftime(dateplus10yearsmin1days, partner_date_format)
        # Plus 20 years 6 month
        dateplus20years = datetime.strptime(self.fal_last_date_signature_request, DEFAULT_SERVER_DATE_FORMAT) + relativedelta(years=20, months=6)
        dateplus20years = datetime.strftime(dateplus20years, partner_date_format)

        # Partner Check and Added + Check if there is child with no email
        # 1.  Main Partner
        universign_signers.append({'firstname': self.partner_id.firstname, 'lastname': self.partner_id.lastname, 'emailAddress': self.partner_id.email, 'certificateType': 'simple'})
        # 2.  Co Partner
        multiple_owner_check = False
        for fal_partner_child_id in self.fal_partner_child_ids:
            if fal_partner_child_id.fal_is_owner:
                multiple_owner_check = True
                universign_signers.append({'firstname': fal_partner_child_id.firstname, 'lastname': fal_partner_child_id.lastname, 'emailAddress': fal_partner_child_id.email, 'certificateType': 'simple'})
                if not fal_partner_child_id.email:
                    raise UserError(_("Please provide Email for main partner and all related contacts (That is Lodger or Owner)."))

        available_docs_by_code = {docs.code: docs.id for docs in self.fal_document_signature_ids}

        # 3.  Lodger
        lodger_check = False
        for fal_partner_child_id in self.fal_partner_child_ids:
            if fal_partner_child_id.fal_is_lodger:
                lodger_check = True
                universign_signers.append({'firstname': fal_partner_child_id.firstname, 'lastname': fal_partner_child_id.lastname, 'emailAddress': fal_partner_child_id.email, 'certificateType': 'simple'})
                if not fal_partner_child_id.email:
                    raise UserError(_("Please provide Email for main partner and all related contacts (That is Lodger or Owner)."))

        # Logic to select the document, also to determine the behavior to add to docs list or just adding to available docs list
        # Logic to select child ids that is Installation Address
        dia_street = self.fal_dia_street or False
        dia_street2 = self.fal_dia_street2 or False
        dia_zip = self.fal_dia_zip or False
        dia_city = self.fal_dia_city or False
        if not multiple_owner_check:
            if lodger_check:
                generated_docs = self.with_context(dia_street=dia_street, dia_street2=dia_street2, dia_zip=dia_zip, dia_city=dia_city).generate_report_single_with_lodger()
                if 's_with' in available_docs_by_code:
                    self.env['greenloc.crm.lead.docs.sign.attachment'].browse(available_docs_by_code['s_with']).write({'initial_doc_ids': [(4, generated_docs.id)], 'initial_doc_id': generated_docs.id})
                else:
                    self.env['greenloc.crm.lead.docs.sign.attachment'].create({'name': _("Single With Lodger"), 'code': 's_with', 'lead_id': self.id, 'initial_doc_ids': [(4, generated_docs.id)], 'initial_doc_id': generated_docs.id, 'version': 1})
            else:
                generated_docs = self.with_context(dia_street=dia_street, dia_street2=dia_street2, dia_zip=dia_zip, dia_city=dia_city).generate_report_single_no_lodger()
                if 's_no' in available_docs_by_code:
                    self.env['greenloc.crm.lead.docs.sign.attachment'].browse(available_docs_by_code['s_no']).write({'initial_doc_ids': [(4, generated_docs.id)], 'initial_doc_id': generated_docs.id})
                else:
                    self.env['greenloc.crm.lead.docs.sign.attachment'].create({'name': _("Single No Lodger"), 'code': 's_no', 'lead_id': self.id, 'initial_doc_ids': [(4, generated_docs.id)], 'initial_doc_id': generated_docs.id, 'version': 1})
        else:
            if lodger_check:
                generated_docs = self.with_context(dia_street=dia_street, dia_street2=dia_street2, dia_zip=dia_zip, dia_city=dia_city).generate_report_multi_with_lodger()
                if 'm_with' in available_docs_by_code:
                    self.env['greenloc.crm.lead.docs.sign.attachment'].browse(available_docs_by_code['m_with']).write({'initial_doc_ids': [(4, generated_docs.id)], 'initial_doc_id': generated_docs.id})
                else:
                    self.env['greenloc.crm.lead.docs.sign.attachment'].create({'name': _("Multi With Lodger"), 'code': 'm_with', 'lead_id': self.id, 'initial_doc_ids': [(4, generated_docs.id)], 'initial_doc_id': generated_docs.id, 'version': 1})
            else:
                generated_docs = self.with_context(dia_street=dia_street, dia_street2=dia_street2, dia_zip=dia_zip, dia_city=dia_city).generate_report_multi_no_lodger()
                if 'm_no' in available_docs_by_code:
                    self.env['greenloc.crm.lead.docs.sign.attachment'].browse(available_docs_by_code['m_no']).write({'initial_doc_ids': [(4, generated_docs.id)], 'initial_doc_id': generated_docs.id})
                else:
                    self.env['greenloc.crm.lead.docs.sign.attachment'].create({'name': _("Multi No Lodger"), 'code': 'm_no', 'lead_id': self.id, 'initial_doc_ids': [(4, generated_docs.id)], 'initial_doc_id': generated_docs.id, 'version': 1})

        # Prepare docs to send to universign, also signers position and index
        signatureFields = []
        for signer_idx in range(len(universign_signers)):
            signatureFields.append({'page': 1, 'x': 80, 'y': 42, 'signerIndex': signer_idx})
        universign_docs.append({'name': generated_docs.name, 'content': generated_docs.datas, 'signatureFields': signatureFields})
        # Send to Universign
        # self.send_to_universign(universign_docs=universign_docs, universign_signers=universign_signers, main_partner=True)
        return True

    # Generate neccesary document
    @api.multi
    def generate_documents_rdvvt(self):
        self.ensure_one()
        self.fal_last_date_signature_request = fields.Date.today()
        universign_docs = []
        universign_signers = []
        # Partner Check and Added + Check if there is child with no email
        # 1.  Main Partner
        universign_signers.append({'firstname': self.partner_id.firstname, 'lastname': self.partner_id.lastname, 'emailAddress': self.partner_id.email, 'certificateType': 'advanced'})
        # 2.  Co Partner
        multiple_owner_check = False
        for fal_partner_child_id in self.fal_partner_child_ids:
            if fal_partner_child_id.fal_is_owner:
                multiple_owner_check = True
                universign_signers.append({'firstname': fal_partner_child_id.firstname, 'lastname': fal_partner_child_id.lastname, 'emailAddress': fal_partner_child_id.email, 'certificateType': 'advanced'})
                if not fal_partner_child_id.email:
                    raise UserError(_("Please provide Email for main partner and all related contacts (That is Lodger or Owner)."))

        available_docs_by_code = {docs.code: docs.id for docs in self.fal_document_signature_ids}

        # 3.  Lodger
        lodger_check = False
        for fal_partner_child_id in self.fal_partner_child_ids:
            if fal_partner_child_id.fal_is_lodger:
                lodger_check = True
                universign_signers.append({'firstname': fal_partner_child_id.firstname, 'lastname': fal_partner_child_id.lastname, 'emailAddress': fal_partner_child_id.email, 'certificateType': 'advanced'})
                if not fal_partner_child_id.email:
                    raise UserError(_("Please provide Email for main partner and all related contacts (That is Lodger or Owner)."))

        # Logic to select the document, also to determine the behavior to add to docs list or just adding to available docs list
        # Logic to select child ids that is Installation Address
        dia_street = self.fal_dia_street or False
        dia_street2 = self.fal_dia_street2 or False
        dia_zip = self.fal_dia_zip or False
        dia_city = self.fal_dia_city or False
        if not multiple_owner_check:
            if lodger_check:
                generated_docs = self.with_context(dia_street=dia_street, dia_street2=dia_street2, dia_zip=dia_zip, dia_city=dia_city).generate_report_l3_single_with_lodger()
                if 's3_with' in available_docs_by_code:
                    self.env['greenloc.crm.lead.docs.sign.attachment'].browse(available_docs_by_code['s3_with']).write({'initial_doc_ids': [(4, generated_docs.id)], 'initial_doc_id': generated_docs.id})
                else:
                    self.env['greenloc.crm.lead.docs.sign.attachment'].create({'name': _("Single L3 With Lodger"), 'code': 's3_with', 'lead_id': self.id, 'initial_doc_ids': [(4, generated_docs.id)], 'initial_doc_id': generated_docs.id, 'version': 1})
            else:
                generated_docs = self.with_context(dia_street=dia_street, dia_street2=dia_street2, dia_zip=dia_zip, dia_city=dia_city).generate_report_l3_single_no_lodger()
                if 's3_no' in available_docs_by_code:
                    self.env['greenloc.crm.lead.docs.sign.attachment'].browse(available_docs_by_code['s3_no']).write({'initial_doc_ids': [(4, generated_docs.id)], 'initial_doc_id': generated_docs.id})
                else:
                    self.env['greenloc.crm.lead.docs.sign.attachment'].create({'name': _("Single L3 No Lodger"), 'code': 's3_no', 'lead_id': self.id, 'initial_doc_ids': [(4, generated_docs.id)], 'initial_doc_id': generated_docs.id, 'version': 1})
        else:
            if lodger_check:
                generated_docs = self.with_context(dia_street=dia_street, dia_street2=dia_street2, dia_zip=dia_zip, dia_city=dia_city).generate_report_l3_multi_with_lodger()
                if 'm3_with' in available_docs_by_code:
                    self.env['greenloc.crm.lead.docs.sign.attachment'].browse(available_docs_by_code['m3_with']).write({'initial_doc_ids': [(4, generated_docs.id)], 'initial_doc_id': generated_docs.id})
                else:
                    self.env['greenloc.crm.lead.docs.sign.attachment'].create({'name': _("Multi L3 With Lodger"), 'code': 'm3_with', 'lead_id': self.id, 'initial_doc_ids': [(4, generated_docs.id)], 'initial_doc_id': generated_docs.id, 'version': 1})
            else:
                generated_docs = self.with_context(dia_street=dia_street, dia_street2=dia_street2, dia_zip=dia_zip, dia_city=dia_city).generate_report_l3_multi_no_lodger()
                if 'm3_no' in available_docs_by_code:
                    self.env['greenloc.crm.lead.docs.sign.attachment'].browse(available_docs_by_code['m3_no']).write({'initial_doc_ids': [(4, generated_docs.id)], 'initial_doc_id': generated_docs.id})
                else:
                    self.env['greenloc.crm.lead.docs.sign.attachment'].create({'name': _("Multi L3 No Lodger"), 'code': 'm3_no', 'lead_id': self.id, 'initial_doc_ids': [(4, generated_docs.id)], 'initial_doc_id': generated_docs.id, 'version': 1})

        # Prepare docs to send to universign, also signers position and index
        signatureFields = []
        for signer_idx in range(len(universign_signers)):
            signatureFields.append({'page': 1, 'x': 80, 'y': 42, 'signerIndex': signer_idx})
        universign_docs.append({'name': generated_docs.name, 'content': generated_docs.datas, 'signatureFields': signatureFields})
        # Send to Universign
        #self.send_rdvvt_to_universign(universign_docs=universign_docs, universign_signers=universign_signers, main_partner=True)
        return True

    @api.multi
    def generate_report_multi_with_lodger(self):
        self.ensure_one()
        report = self.env['ir.actions.report.xml'].with_context(self._context).search([('report_name', '=', 'greenloc_crm_ext.report_multi_with_lodger')])
        if report:
            document = self.env['report'].with_context(self._context).get_pdf([self.id], report.report_name)
            available_docs_by_code = {docs.code: docs.id for docs in self.fal_document_signature_ids}
            if 'm_with' in available_docs_by_code:
                current_version = self.env['greenloc.crm.lead.docs.sign.attachment'].browse(available_docs_by_code['m_with']).version
                self.env['greenloc.crm.lead.docs.sign.attachment'].browse(available_docs_by_code['m_with']).version = current_version+1
                return self.env['ir.attachment'].create({
                    'name': self.name + ' - MWL -' + ' V' + str(current_version),
                    'datas_fname': self.name + ' - MWL -' + ' V' + str(current_version) + '.pdf',
                    'datas': base64.b64encode(document),
                    'type': 'binary',
                    'res_model': 'crm.lead',
                    'res_id': self.id,
                    'res_name': self.name,
                    'fal_lead_id': self.id,
                })
            else:
                return self.env['ir.attachment'].create({
                    'name': self.name + ' - MWL -' + ' V0',
                    'datas_fname': self.name + ' - MWL -' + ' V0.pdf',
                    'datas': base64.b64encode(document),
                    'type': 'binary',
                    'res_model': 'crm.lead',
                    'res_id': self.id,
                    'res_name': self.name,
                    'fal_lead_id': self.id,
                })

    @api.multi
    def generate_report_multi_no_lodger(self):
        self.ensure_one()
        report = self.env['ir.actions.report.xml'].with_context(self._context).search([('report_name', '=', 'greenloc_crm_ext.report_multi_no_lodger')])
        if report:
            document = self.env['report'].with_context(self._context).get_pdf([self.id], report.report_name)
            available_docs_by_code = {docs.code: docs.id for docs in self.fal_document_signature_ids}
            if 'm_no' in available_docs_by_code:
                current_version = self.env['greenloc.crm.lead.docs.sign.attachment'].browse(available_docs_by_code['m_no']).version
                self.env['greenloc.crm.lead.docs.sign.attachment'].browse(available_docs_by_code['m_no']).version = current_version+1
                return self.env['ir.attachment'].create({
                    'name': self.name + ' - MNL -' + ' V' + str(current_version),
                    'datas_fname': self.name + ' - MNL -' + ' V' + str(current_version) + '.pdf',
                    'datas': base64.b64encode(document),
                    'type': 'binary',
                    'res_model': 'crm.lead',
                    'res_id': self.id,
                    'res_name': self.name,
                    'fal_lead_id': self.id,
                })
            else:
                return self.env['ir.attachment'].create({
                    'name': self.name + ' - MNL -' + ' V0',
                    'datas_fname': self.name + ' - MNL -' + ' V0.pdf',
                    'datas': base64.b64encode(document),
                    'type': 'binary',
                    'res_model': 'crm.lead',
                    'res_id': self.id,
                    'res_name': self.name,
                    'fal_lead_id': self.id,
                })

    @api.multi
    def generate_report_single_with_lodger(self):
        self.ensure_one()
        report = self.env['ir.actions.report.xml'].with_context(self._context).search([('report_name', '=', 'greenloc_crm_ext.report_single_with_lodger')])
        if report:
            document = self.env['report'].with_context(self._context).get_pdf([self.id], report.report_name)
            available_docs_by_code = {docs.code: docs.id for docs in self.fal_document_signature_ids}
            if 's_with' in available_docs_by_code:
                current_version = self.env['greenloc.crm.lead.docs.sign.attachment'].browse(available_docs_by_code['s_with']).version
                self.env['greenloc.crm.lead.docs.sign.attachment'].browse(available_docs_by_code['s_with']).version = current_version+1
                return self.env['ir.attachment'].create({
                    'name': self.name + ' - SWL -' + ' V' + str(current_version),
                    'datas_fname': self.name + ' - SWL -' + ' V' + str(current_version) + '.pdf',
                    'datas': base64.b64encode(document),
                    'type': 'binary',
                    'res_model': 'crm.lead',
                    'res_id': self.id,
                    'res_name': self.name,
                    'fal_lead_id': self.id,
                })
            else:
                return self.env['ir.attachment'].create({
                    'name': self.name + ' - SWL -' + ' V0',
                    'datas_fname': self.name + ' - SWL -' + ' V0.pdf',
                    'datas': base64.b64encode(document),
                    'type': 'binary',
                    'res_model': 'crm.lead',
                    'res_id': self.id,
                    'res_name': self.name,
                    'fal_lead_id': self.id,
                })

    @api.multi
    def generate_report_single_no_lodger(self):
        self.ensure_one()
        report = self.env['ir.actions.report.xml'].with_context(self._context).search([('report_name', '=', 'greenloc_crm_ext.report_single_no_lodger')])
        if report:
            document = self.env['report'].with_context(self._context).get_pdf([self.id], report.report_name)
            available_docs_by_code = {docs.code: docs.id for docs in self.fal_document_signature_ids}
            if 's_no' in available_docs_by_code:
                current_version = self.env['greenloc.crm.lead.docs.sign.attachment'].browse(available_docs_by_code['s_no']).version
                self.env['greenloc.crm.lead.docs.sign.attachment'].browse(available_docs_by_code['s_no']).version = current_version+1
                return self.env['ir.attachment'].create({
                    'name': self.name + ' - SNL -' + ' V' + str(current_version),
                    'datas_fname': self.name + ' - SNL -' + ' V' + str(current_version) + '.pdf',
                    'datas': base64.b64encode(document),
                    'type': 'binary',
                    'res_model': 'crm.lead',
                    'res_id': self.id,
                    'res_name': self.name,
                    'fal_lead_id': self.id,
                })
            else:
                return self.env['ir.attachment'].create({
                    'name': self.name + ' - SNL -' + ' V0',
                    'datas_fname': self.name + ' - SNL -' + ' V0.pdf',
                    'datas': base64.b64encode(document),
                    'type': 'binary',
                    'res_model': 'crm.lead',
                    'res_id': self.id,
                    'res_name': self.name,
                    'fal_lead_id': self.id,
                })

    @api.multi
    def generate_report_l3_multi_with_lodger(self):
        self.ensure_one()
        report = self.env['ir.actions.report.xml'].with_context(self._context).search([('report_name', '=', 'greenloc_crm_ext.report_l3_multi_with_lodger')])
        if report:
            document = self.env['report'].with_context(self._context).get_pdf([self.id], report.report_name)
            available_docs_by_code = {docs.code: docs.id for docs in self.fal_document_signature_ids}
            if 'm3_with' in available_docs_by_code:
                current_version = self.env['greenloc.crm.lead.docs.sign.attachment'].browse(available_docs_by_code['m3_with']).version
                self.env['greenloc.crm.lead.docs.sign.attachment'].browse(available_docs_by_code['m3_with']).version = current_version+1
                return self.env['ir.attachment'].create({
                    'name': self.name + ' - MWL L3 -' + ' V' + str(current_version),
                    'datas_fname': self.name + ' - MWL L3 -' + ' V' + str(current_version) + '.pdf',
                    'datas': base64.b64encode(document),
                    'type': 'binary',
                    'res_model': 'crm.lead',
                    'res_id': self.id,
                    'res_name': self.name,
                    'fal_lead_id': self.id,
                })
            else:
                return self.env['ir.attachment'].create({
                    'name': self.name + ' - MWL L3 -' + ' V0',
                    'datas_fname': self.name + ' - MWL L3 -' + ' V0.pdf',
                    'datas': base64.b64encode(document),
                    'type': 'binary',
                    'res_model': 'crm.lead',
                    'res_id': self.id,
                    'res_name': self.name,
                    'fal_lead_id': self.id,
                })

    @api.multi
    def generate_report_l3_multi_no_lodger(self):
        self.ensure_one()
        report = self.env['ir.actions.report.xml'].with_context(self._context).search([('report_name', '=', 'greenloc_crm_ext.report_l3_multi_no_lodger')])
        if report:
            document = self.env['report'].with_context(self._context).get_pdf([self.id], report.report_name)
            available_docs_by_code = {docs.code: docs.id for docs in self.fal_document_signature_ids}
            if 'm3_no' in available_docs_by_code:
                current_version = self.env['greenloc.crm.lead.docs.sign.attachment'].browse(available_docs_by_code['m3_no']).version
                self.env['greenloc.crm.lead.docs.sign.attachment'].browse(available_docs_by_code['m3_no']).version = current_version+1
                return self.env['ir.attachment'].create({
                    'name': self.name + ' - MNL L3 -' + ' V' + str(current_version),
                    'datas_fname': self.name + ' - MNL L3 -' + ' V' + str(current_version) + '.pdf',
                    'datas': base64.b64encode(document),
                    'type': 'binary',
                    'res_model': 'crm.lead',
                    'res_id': self.id,
                    'res_name': self.name,
                    'fal_lead_id': self.id,
                })
            else:
                return self.env['ir.attachment'].create({
                    'name': self.name + ' - MNL L3 -' + ' V0',
                    'datas_fname': self.name + ' - MNL L3 -' + ' V0.pdf',
                    'datas': base64.b64encode(document),
                    'type': 'binary',
                    'res_model': 'crm.lead',
                    'res_id': self.id,
                    'res_name': self.name,
                    'fal_lead_id': self.id,
                })

    @api.multi
    def generate_report_l3_single_with_lodger(self):
        self.ensure_one()
        report = self.env['ir.actions.report.xml'].with_context(self._context).search([('report_name', '=', 'greenloc_crm_ext.report_l3_single_with_lodger')])
        if report:
            document = self.env['report'].with_context(self._context).get_pdf([self.id], report.report_name)
            available_docs_by_code = {docs.code: docs.id for docs in self.fal_document_signature_ids}
            if 's3_with' in available_docs_by_code:
                current_version = self.env['greenloc.crm.lead.docs.sign.attachment'].browse(available_docs_by_code['s3_with']).version
                self.env['greenloc.crm.lead.docs.sign.attachment'].browse(available_docs_by_code['s3_with']).version = current_version+1
                return self.env['ir.attachment'].create({
                    'name': self.name + ' - SWL L3 -' + ' V' + str(current_version),
                    'datas_fname': self.name + ' - SWL L3-' + ' V' + str(current_version) + '.pdf',
                    'datas': base64.b64encode(document),
                    'type': 'binary',
                    'res_model': 'crm.lead',
                    'res_id': self.id,
                    'res_name': self.name,
                    'fal_lead_id': self.id,
                })
            else:
                return self.env['ir.attachment'].create({
                    'name': self.name + ' - SWL L3 -' + ' V0',
                    'datas_fname': self.name + ' - SWL L3 -' + ' V0.pdf',
                    'datas': base64.b64encode(document),
                    'type': 'binary',
                    'res_model': 'crm.lead',
                    'res_id': self.id,
                    'res_name': self.name,
                    'fal_lead_id': self.id,
                })

    @api.multi
    def generate_report_l3_single_no_lodger(self):
        self.ensure_one()
        report = self.env['ir.actions.report.xml'].with_context(self._context).search([('report_name', '=', 'greenloc_crm_ext.report_l3_single_no_lodger')])
        if report:
            document = self.env['report'].with_context(self._context).get_pdf([self.id], report.report_name)
            available_docs_by_code = {docs.code: docs.id for docs in self.fal_document_signature_ids}
            if 's3_no' in available_docs_by_code:
                current_version = self.env['greenloc.crm.lead.docs.sign.attachment'].browse(available_docs_by_code['s3_no']).version
                self.env['greenloc.crm.lead.docs.sign.attachment'].browse(available_docs_by_code['s3_no']).version = current_version+1
                return self.env['ir.attachment'].create({
                    'name': self.name + ' - SNL L3 -' + ' V' + str(current_version),
                    'datas_fname': self.name + ' - SNL L3 -' + ' V' + str(current_version) + '.pdf',
                    'datas': base64.b64encode(document),
                    'type': 'binary',
                    'res_model': 'crm.lead',
                    'res_id': self.id,
                    'res_name': self.name,
                    'fal_lead_id': self.id,
                })
            else:
                return self.env['ir.attachment'].create({
                    'name': self.name + ' - SNL L3 -' + ' V0',
                    'datas_fname': self.name + ' - SNL L3 -' + ' V0.pdf',
                    'datas': base64.b64encode(document),
                    'type': 'binary',
                    'res_model': 'crm.lead',
                    'res_id': self.id,
                    'res_name': self.name,
                    'fal_lead_id': self.id,
                })
