from odoo import _, api, fields, models


class MailMail(models.Model):
    _inherit = 'mail.mail'

    fal_lead_id = fields.Many2one("crm.lead", "Lead")
