# -*- coding: utf-8 -*-
from openerp import api, fields, models, _


class Users(models.Model):
    _inherit = 'res.users'

    # Adding some required field

    fal_universign_login = fields.Char("Universign Login")
    fal_universign_password = fields.Char("Universign Password")
