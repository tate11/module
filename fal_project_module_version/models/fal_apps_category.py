from odoo import fields, models, api, _


class AppsCategory(models.Model):
    _name = "fal.apps.category"

    name = fields.Char(string='Name')
    code = fields.Char(string='Code')


class HistoryChange(models.Model):
    _name = "fal.history.change"

    task_id = fields.Many2one("project.task", "Task")
    fal_date = fields.Datetime(string='Date')
    fal_desc = fields.Text(string='Description')
    fal_responsible = fields.Many2one('res.users', string='Responsible')
    fal_stage = fields.Many2one('project.task.type', string='Stage')
    fal_date_deadline = fields.Date(string='Deadline')
    fal_new_deadline = fields.Date(string='New Deadline')
