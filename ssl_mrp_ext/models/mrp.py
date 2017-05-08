from odoo import models, fields


class MrpWorkcenterProductivity(models.Model):
    _inherit = "mrp.workcenter.productivity"

    fal_production_id = fields.Many2one(
        'mrp.production', related='workorder_id.production_id',
        string='Manufacturing Order'
    )
