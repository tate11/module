# -*- coding:utf-8 -*-
from odoo import fields, models, api, _
from dateutil.relativedelta import relativedelta
from datetime import datetime
from datetime import date


class hr_employee(models.Model):
    _name = "hr.employee"
    _inherit = "hr.employee"

    fal_reference = fields.Char('Reference')
    address_home_id = fields.Many2one('res.partner', 'Related Partner')
    driving_license_number = fields.Char('Driving License Number', size=128)
    parents_address = fields.Text('Parents Address')
    parents_phone = fields.Char('Parents Phone', size=64)
    contact = fields.Char('Contact in Case of Accident', size=64)
    relation_contact = fields.Char('Relation of the Contact', size=64)
    phone_contact = fields.Char('Phone of the Contact', size=64)
    hukou_place = fields.Char('Hukou Place', size=128)
    fal_child_ids = fields.One2many(
        'hr.employee.child',
        'employee_id',
        string='Children'
    )
    age = fields.Char(string='Age')

# end of hr_employee()

    @api.onchange('birthday')
    def set_age(self):
        for rec in self:
            if rec.birthday:
                dt = rec.birthday
                d1 = datetime.strptime(dt, "%Y-%m-%d").date()
                d2 = date.today()
                rd = relativedelta(d2, d1)
                rec.age = str(rd.years) + ' years ' + str(rd.months) + ' months'


class hr_employee_child(models.Model):
    _name = "hr.employee.child"

    employee_id = fields.Many2one('hr.employee', string="Employee")
    name = fields.Char('Name', size=128, required=True, select=True)


# end of hr_employee_child()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
