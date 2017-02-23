# -*- coding: utf-8 -*-
from odoo import fields, models, api, _


class AccountAssetDepreciationLine(models.Model):
    _inherit = 'account.asset.depreciation.line'

    @api.multi
    def create_move(self, post_move=True):
        created_moves = self.env['account.move']
        res = super(AccountAssetDepreciationLine, self).create_move(post_move)
        if res:
            for move in created_moves.browse(res):
                move.line_ids.write({
                    'analytic_account_id': move.asset_id.category_id.account_analytic_id.id,
                })
        return res

# end of AccountAssetDepreciationLine
