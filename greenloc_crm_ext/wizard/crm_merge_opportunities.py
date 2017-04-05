# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models


class MergeOpportunity(models.TransientModel):
    """
        Merge opportunities together.
        If we're talking about opportunities, it's just because it makes more sense
        to merge opps than leads, because the leads are more ephemeral objects.
        But since opportunities are leads, it's also possible to merge leads
        together (resulting in a new lead), or leads and opps together (resulting
        in a new opp).
    """

    _inherit = 'crm.merge.opportunity'

    head_opportunity_id = fields.Many2one('crm.lead', string='Head Leads/Opportunities')

    @api.multi
    @api.onchange('opportunity_ids')
    def onchange_opportunity_ids(self):
        for merge in self:
            domain = [('id', 'in', self.opportunity_ids.ids)]
            return {'domain': {'head_opportunity_id': domain}}

    @api.multi
    def action_merge(self):
        self.ensure_one()
        merge_opportunity = self.opportunity_ids.with_context(head_selected=self.head_opportunity_id).merge_opportunity(self.user_id.id, self.team_id.id)

        # The newly created lead might be a lead or an opp: redirect toward the right view
        if merge_opportunity.type == 'opportunity':
            return merge_opportunity.redirect_opportunity_view()
        else:
            return merge_opportunity.redirect_lead_view()
