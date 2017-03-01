# -*- encoding: utf-8 -*-

from datetime import datetime

from odoo import fields, models, api, _


class account_asset_category(models.Model):
    _name = 'account.asset.category'
    _inherit = 'account.asset.category'

    simple_prorata = fields.Boolean('Simple Prorata')

# end of account_asset_category()


class account_asset_asset(models.Model):
    _name = 'account.asset.asset'
    _inherit = 'account.asset.asset'

    def _compute_board_amount(
        self,
        i,
        residual_amount,
        amount_to_depr,
        undone_dotation_number,
        posted_depreciation_line_ids,
        total_days,
        depreciation_date
    ):
        res = super(account_asset_asset, self)._compute_board_amount(
            i,
            residual_amount,
            amount_to_depr,
            undone_dotation_number,
            posted_depreciation_line_ids,
            total_days,
            depreciation_date
        )
        if self.prorata and self.simple_prorata:
            res = 0
            if i == undone_dotation_number:
                res = residual_amount
            else:
                if self.method == 'linear':
                    res = amount_to_depr / (undone_dotation_number - len(posted_depreciation_line_ids))
                elif self.method == 'degressive':
                    res = residual_amount * self.method_progress_factor
        return res

    @api.multi
    @api.depends('depreciation_line_ids')
    def _fal_closing_date(self):
        for record in self:
            temp_last_date = False
            for line in record.depreciation_line_ids:
                if temp_last_date < line.depreciation_date:
                    temp_last_date = line.depreciation_date
            record.fal_closing_date = temp_last_date

    simple_prorata = fields.Boolean('Simple Prorata')
    fal_closing_date = fields.Date(
        string='Closing Date',
        help="The Closing Date",
        compute='_fal_closing_date',
        store=True
    )

    @api.onchange('category_id')
    def onchange_category_id(self):
        res = super(account_asset_asset, self).onchange_category_id()
        asset_categ_obj = self.env['account.asset.category']
        if self.category_id:
            category_obj = asset_categ_obj.browse(self.category_id.id)
            self.simple_prorata = category_obj.simple_prorata

# end of account_asset_asset()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
