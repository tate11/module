from odoo import fields, models, api, _

import openerp.addons.decimal_precision as dp
import time


class contract_condition_falinwa(models.Model):
    _name = "contract.condition"

    name = fields.Char(string='Name', size=64, select=True, required=True)
    content = fields.Text(string='Content', select=True, required=True)

# end of contract_condition_falinwa()
