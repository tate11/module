# -*- coding: utf-8 -*-
from odoo import fields, models, api, _


class project(models.Model):
    _name = "project.project"
    _inherit = "project.project"

    project_todo_list = fields.Boolean('To do list')
    classic_project = fields.Boolean('Classic Project')

    def _get_type_common(self):
        ids = super(project, self)._get_type_common()
        if context.get('default_project_todo_list', False):
            ids = self.pool.get('project.task.type').search([('todolist_default', '=', 1)])
        return ids

    _defaults = {
        'type_ids': _get_type_common,
    }
# end of project()


class project_task_type(models.Model):
    _name = 'project.task.type'
    _inherit = 'project.task.type'

    todolist_default = fields.Boolean('Default for New To do List',
                        help="If you check this field, this stage will be proposed by default on each new To do List. It will not assign this stage to existing To do List."),

# end of project_task_type()
