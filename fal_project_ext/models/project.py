# -*- coding:utf-8 -*-
from odoo import fields, models, api, _


class project(models.Model):
    _name = "project.project"
    _inherit = "project.project"

    program_name = fields.Char('Program Name', size=128)
    mold_serial_number = fields.Char('Total Mold Qty', size=128)
    project_opportunities = fields.Boolean('Opportunities')
    classic_project = fields.Boolean('Classic Project')

    def _get_type_common(self):
        ids = self.env['project.task.type'].search([('case_default', '=', 1)])
        if self.get('default_project_opportunities', False):
            ids = self.env['project.task.type'].\
                search([('project_opportunities_default', '=', 1)])
        return ids

# end of project()


class project_task_type(models.Model):
    _name = 'project.task.type'
    _inherit = 'project.task.type'

    project_opportunities_default = fields.Boolean(
        'Default for Project Opportunities',
        help="If you check this field, this stage will be proposed by \
        default on each new Project Opportunities. \
        It will not assign this stage to existing Project Opportunities.")
    case_default = fields.Boolean(
        'Default for New Projects',
        help="If you check this field, this stage will be proposed by default on each \
        new project. It will not assign this stage to existing projects.")

# end of project_task_type()


class task(models.Model):
    _name = "project.task"
    _inherit = "project.task"

    partner_id = fields.Many2one('res.partner', 'Customer', default=False)
    project_id_partner_id = fields.Many2one(
        'res.partner',
        related='project_id.partner_id',
        string='Final Customer',
        readonly=True,
        store=True)

    def onchange_project(self, id, project_id):
        res = super(task, self).onchange_project(id, project_id)
        return {}

    @api.multi
    def write(self, vals):
        if isinstance(self.ids, (int, long)):
            ids = [self.ids]
        if vals and not 'kanban_state' in vals and 'stage_id' in vals:
            for t in self.browse(self.ids):
                vals['kanban_state'] = t.kanban_state
                super(task, self).write(vals)
        else:
            result = super(task, self).write(vals)
        return True

# end of task()


class account_analytic_account(models.Model):
    _name = 'account.analytic.account'
    _inherit = 'account.analytic.account'

    def _get_one_full_name(self, elmt, level=6):
        res = super(account_analytic_account, self)._get_one_full_name(elmt, level)
        if elmt.partner_id:
            res += ' / ' + elmt.partner_id.name
        return res

# end of account_analytic_account()
