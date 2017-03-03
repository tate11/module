# -*- coding: utf-8 -*-
from odoo import fields, models, api, exceptions, _


class popup_after_login_config(models.TransientModel):
    _name = "popup.after.login.config"
    _description = "After login config"

    company_id = fields.Many2one(
        'res.company',
        string='Company',
        required=True,
        help='The company this user is currently working for.',
        default='_get_company'
    )

    @api.model
    def _get_company(self):
        user_obj = self.env['res.users']
        user = user_obj.read(['company_id'])
        company_id = user.get('company_id', False)
        return company_id and company_id[0] or False

    def onchange_company_id(self):
        user_obj = self.env['res.users']
        if self:
            write_temp = {
                'company_id': self,
            }
            user_obj.write(write_temp)
        return True

    @api.multi
    def execute(self):
        # """
        # user_obj = self.pool.get('res.users')
        # for config_id in self.browse(cr,uid,ids):
        #     write_temp = {
        #         'company_id' : config_id.company_id.id,
        #     }
        #     user_obj.write(cr,uid,uid,write_temp)
        # """
        return {
            'type': 'ir.actions.client',
            'tag': 'reload',
        }

# end of popup_after_login_config()
