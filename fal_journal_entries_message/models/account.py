from odoo import fields, models, api, _


class account_move(models.Model):
    _name = "account.move"
    _inherit = ['account.move', 'mail.thread', 'ir.needaction_mixin']

# end of account_move()
