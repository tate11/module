# -*- coding: utf-8 -*-
from odoo import api, fields, models


class account_analytic_chart(models.TransientModel):
    _name = 'account.analytic.chart'
    _description = 'Account Analytic Chart'

    from_date = fields.Date(string='From')
    to_date = fields.Date(string='To')

    @api.multi
    def analytic_account_chart_open_window(self):
        mod_obj = self.env['ir.model.data']
        act_obj = self.env['ir.actions.act_window']
        result_context = {}
        result = mod_obj.get_object_reference('fal_parent_account', 'action_account_analytic_account_tree2')
        id = result and result[1] or False
        result = act_obj.browse(id).read()[0]
        data = self.read()[0]
        if data['from_date']:
            result_context.update({'from_date': data['from_date']})
        if data['to_date']:
            result_context.update({'to_date': data['to_date']})
        result['context'] = str(result_context)
        return result

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
