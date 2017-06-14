from odoo import models, fields, api


class ProjectTask(models.Model):
    _inherit = 'project.task'

    fal_number = fields.Char(
        string='Number',
    )
    fal_display_number = fields.Char(string='Display Number', compute='_get_display_name')
    fal_version = fields.Selection([
        ('10', '10'),
        ('9', '9'),
        ('8', '8'),
        ('7', '7'),
    ], string='Odoo Version')
    fal_url = fields.Char(string='Technical Location')
    fal_cust_deadline = fields.Date(string='Customer Deadline')
    fal_tech_deadline = fields.Date(string='Technical Deadline')
    fal_apps_category_id = fields.Many2one(
        'fal.apps.category',
        string='Apps Category'
    )
    fal_next_action_user_id = fields.Many2one(
        'res.users',
        string='Next Action by'
    )
    fal_responsible_user_id = fields.Many2one(
        'res.users',
        string='Responsible'
    )
    fal_change_ids = fields.One2many(
        'fal.history.change',
        'task_id',
        string='Change History'
    )

    @api.depends('fal_number', 'stage_id')
    def _get_display_name(self):
        for rule in self:
            name = '%s-%s' % (rule.fal_number, rule.stage_id.name)
            rule.fal_display_number = name
