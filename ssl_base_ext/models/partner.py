from odoo import fields, models, api


class resPartner(models.Model):
    _inherit = 'res.partner'

    fal_related_company_ids = fields.One2many(
        'res.company',
        'partner_id',
        string='Related Company'
    )
    fal_ssl_company = fields.Boolean(
        string='Is SSL Company Partner',
        compute='fal_get_company_partner'
    )
    fal_ef_company = fields.Boolean(
        string='Is EF Company Partner',
        compute='fal_get_company_partner'
    )
    fal_aixalp_company = fields.Boolean(
        string='Is Aixalp Company Partner',
        compute='fal_get_company_partner'
    )

    @api.depends(
        'fal_related_company_ids', 'fal_related_company_ids.fal_code')
    def fal_get_company_partner(self):
        for item in self:
            for company in item.fal_related_company_ids:
                if company.fal_code == 'X':
                    item.fal_aixalp_company = True
                elif company.fal_code == 'S':
                    item.fal_ssl_company = True
                elif company.fal_code == 'E':
                    item.fal_ef_company = True
