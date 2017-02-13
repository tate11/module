# -*- coding: utf-8 -*-
from odoo import api, fields, models, _


class ir_exports_line(models.Model):
    _name = 'ir.exports.line'
    _inherit = 'ir.exports.line'
    _order = 'sequence, id'

    sequence = fields.Integer('Sequence', help="Used to order the sequences.")

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
