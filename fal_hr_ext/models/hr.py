# -*- coding:utf-8 -*-
from odoo import fields, models, _


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

# end of hr_employee()


class hr_employee_child(models.Model):
    _name = "hr.employee.child"

    employee_id = fields.Many2one('hr.employee', string="Employee")
    name = fields.Char('Name', size=128, required=True, select=True)


# end of hr_employee_child()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
