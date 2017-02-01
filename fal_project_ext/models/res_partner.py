
from odoo import fields, models, api, _


class res_partner(models.Model):
    _name = "res.partner"
    _inherit = "res.partner"

    is_final_customer = fields.Boolean('Final Customer')

# end of res_partner()
