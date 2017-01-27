from odoo import fields, models, api
from openerp.tools.translate import _


class account_account(models.Model):
    _name = "account.account"
    _inherit = "account.account"

    fal_multicompany_consolidation_account_id = fields.Many2one(
        'account.account',
        'Consolidated Ledger Account',
        domain="[('company_id.child_ids','=',company_id)]"
    )

# end of account_account()
