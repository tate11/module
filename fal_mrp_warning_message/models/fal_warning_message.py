from openerp import models, fields


class MrpWorkCenter(models.Model):
    _inherit = 'mrp.workcenter'

    fal_warning_message_ids = fields.Many2many(
        'fal.warning.message',
        'fal_warning_message_workcenter_rel',
        'workcenter_id',
        'warning_id',
        string='Warning Messages for Workcenter'
    )


class MrpRouting(models.Model):
    _inherit = 'mrp.routing'

    fal_warning_message_ids = fields.Many2many(
        'fal.warning.message',
        'fal_warning_message_routing_rel',
        'routing_id',
        'warning_id',
        string='Warning Messages for Routing'
    )
