# -*- coding: utf-8 -*-
from openerp import api, fields, models, _


class Partner(models.Model):
    _inherit = 'res.partner'

    # Adding some required field

    lead_id = fields.Many2one('crm.lead', 'Lead')
    fal_marital_status = fields.Selection([('married', 'Married'),
                                          ('single', 'Single'),
                                          ('widower', 'Widower',),
                                          ('pacs', 'Pacs'),
                                          ('concubinage', 'Concubinage')],
                                          string="Marital Status")
    fal_wedding_contract = fields.Char(string="Wedding Contract")
    fal_birthday = fields.Date(string="Birthday")
    fal_parent_id_relation_type = fields.Selection([('child', 'Child'),
                                                    ('spouse', 'Spouse'),
                                                    ('wife', 'Wife'),
                                                    ('husband', 'Husband'),
                                                    ('lodger', 'Lodger'),
                                                    ('sci', 'SCI'),
                                                    ('moral', 'Moral'),
                                                    ('other', 'Other')],
                                                   string="Relation")
    fal_is_owner = fields.Boolean(string="Is Owner")
    fal_is_lodger = fields.Boolean(string="Is Lodger")
    fal_birth_place = fields.Char(string="Birthplace")
    fal_birth_department = fields.Char(string="Birth Department")
    fal_birth_nationality = fields.Many2one('res.country', string="Birth Nationality")
    # Add on field for company
    fal_siret = fields.Char(string="Siret")
    fal_reg_city = fields.Char(string="Registered City")
    fal_capital = fields.Char(string="Capital")
    fal_manager_firstname = fields.Char(string="Manager First Name")
    fal_manager_lastname = fields.Char(string="Manager Last Name")
    fal_depart_no = fields.Char(string="Department N°", compute='_compute_department_no', store=True)

    # Department Number auto generate
    @api.one
    @api.depends('zip')
    def _compute_department_no(self):
        if self.zip:
            self.fal_depart_no = self.zip[0:2]

    def _onchange_partner_id_values(self, partner_id):
        """ returns the new values when partner_id has changed """
        if partner_id:
            partner = self.env['res.partner'].browse(partner_id)

            partner_name = partner.parent_id.name
            if not partner_name and partner.is_company:
                partner_name = partner.name

            return {
                'partner_name': partner_name,
                'contact_name': partner.name if not partner.is_company else False,
                'title': partner.title.id,
                'street': partner.street,
                'street2': partner.street2,
                'city': partner.city,
                'state_id': partner.state_id.id,
                'country_id': partner.country_id.id,
                'email_from': partner.email,
                'phone': partner.phone,
                'mobile': partner.mobile,
                'fax': partner.fax,
                'zip': partner.zip,
                'function': partner.function,
                'fal_marital_status': partner.fal_marital_status,
                'fal_wedding_contract': partner.fal_wedding_contract,
            }
        return {}
