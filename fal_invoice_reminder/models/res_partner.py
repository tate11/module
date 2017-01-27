# -*- coding: utf-8 -*-

from odoo import fields, models, api
from openerp.tools.translate import _
import openerp.addons.decimal_precision as dp
import time


class res_partner(models.Model):
    _name = "res.partner"
    _inherit = "res.partner"

    invoice_reminder = fields.Boolean('Invoice Reminder', default=1)


# end of res_partner()
