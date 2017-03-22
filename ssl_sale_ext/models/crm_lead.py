from odoo import models, fields, api


class CrmLead(models.Model):
    _inherit = 'crm.lead'

    display_name = fields.Char(compute='fal_compute_display_name')

    @api.depends('name', 'partner_id', 'partner_id.ref')
    def fal_compute_display_name(self):
        for item in self:
            if item.partner_id.is_company:
                ref = item.partner_id.ref
            else:
                ref = item.partner_id.parent_id and \
                    item.partner_id.parent_id.ref
                if not item.partner_id.parent_id:
                    ref = item.partner_id.ref
            if ref:
                item.display_name = ref + ' - ' +\
                    item.name
            else:
                item.display_name = item.name

    @api.multi
    def name_get(self):
        res = super(CrmLead, self).name_get()
        new_res = []
        for item in res:
            lead = self.browse(item[0])
            if lead.partner_id.is_company:
                ref = lead.partner_id.ref
            else:
                ref = lead.partner_id.parent_id and \
                    lead.partner_id.parent_id.ref
                if not lead.partner_id.parent_id:
                    ref = lead.partner_id.ref
            if ref:
                new_res.append((
                    lead.id, ref + ' - ' + item[1]
                ))
            else:
                new_res.append(item)
        return new_res
