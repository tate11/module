from odoo import _, api, exceptions, fields, models, tools


class MailThread(models.AbstractModel):
    _inherit = 'mail.thread'

    @api.multi
    def _message_auto_subscribe_notify(self, partner_ids):
        """ Notify newly subscribed followers of the last posted message.
            :param partner_ids : the list of partner to add as needaction partner of the last message
                                 (This excludes the current partner)
        """
        if not partner_ids:
            return
        for record in self:
            # If record are from greenloc website, do not send email
            if not record.fal_website_form_result:
                record.message_post_with_view(
                    'mail.message_user_assigned',
                    composition_mode='mass_mail',
                    partner_ids=[(4, pid) for pid in partner_ids],
                    auto_delete=True,
                    auto_delete_message=True,
                    subtype_id=self.env.ref('mail.mt_note').id)
