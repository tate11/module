from odoo import fields, models, api, _

import openerp.addons.decimal_precision as dp
import time


class account_voucher(models.Model):
    _name = "account.voucher"
    _inherit = "account.voucher"

    @api.multi
    def onchange_contract_condition_id(self, contract_condition_id):
        if not contract_condition_id:
            return {}
        return {'value': {'comment': self.env['contract.condition'].browse(contract_condition_id).content}}

    contract_condition_id = fields.Many2one(
        'contract.condition',
        string='Contract Condition'
    )

# end of account_voucher()
