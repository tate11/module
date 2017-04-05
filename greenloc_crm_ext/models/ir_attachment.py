from odoo import api, fields, models, tools, SUPERUSER_ID, _
from odoo.exceptions import UserError


class IrAttachment(models.Model):
    _inherit = 'ir.attachment'

    fal_lead_id = fields.Many2one("crm.lead", "Lead")
    fal_greenloc_crm_lead_docs_initial_attachment = fields.Many2one("greenloc.crm.lead.docs.sign.attachment", "Greenloc_lead_docs_sign")
    fal_greenloc_crm_lead_docs_sign_attachment = fields.Many2one("greenloc.crm.lead.docs.sign.attachment", "Greenloc_lead_docs_sign")
    fal_protected = fields.Boolean("Protected", help="Protected Document cannot be deleted")

    # Prevent Deleting a protected attachment
    @api.multi
    def unlink(self):
        for attachment in self:
            if attachment.fal_protected:
                raise UserError(_("Cannot delete protected attachment."))
        super(IrAttachment, self).unlink()
