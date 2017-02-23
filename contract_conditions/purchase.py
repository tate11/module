# -*- coding: utf-8 -*-
from odoo import fields, models, api, _

import openerp.addons.decimal_precision as dp
import time


class purchase_order(models.Model):
    _name = "purchase.order"
    _inherit = "purchase.order"

    @api.multi
    def onchange_contract_condition_id(self, contract_condition_id):
        if not contract_condition_id:
            return {}
        return {'value': {'comment': self.env['contract.condition'].browse(contract_condition_id).content}}

    contract_condition_id = fields.Many2one(
        'contract.condition',
        string='Contract Condition'
    )

# end of purchase_order()
