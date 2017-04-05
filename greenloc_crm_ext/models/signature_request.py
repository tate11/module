from odoo import api, fields, models, _


class SignatureRequest(models.Model):
    _inherit = "signature.request"

    fal_lead_id = fields.Many2one('crm.lead', "Lead")

	# Add lead id in mail that sended from send signature button
    @api.one
    def send_follower_accesses(self, followers, subject=None, message=None):
        base_context = self.env.context
        template_id = self.env.ref('website_sign.website_sign_mail_template').id
        mail_template = self.env['mail.template'].browse(template_id)

        email_from_usr = self.create_uid.partner_id.name
        email_from_mail = self.create_uid.partner_id.email
        email_from = "%(email_from_usr)s <%(email_from_mail)s>" % {'email_from_usr': email_from_usr, 'email_from_mail': email_from_mail}

        for follower in followers:
            template = mail_template.sudo().with_context(base_context,
                lang = follower.lang,
                template_type = "follower",
                email_from_usr = email_from_usr,
                email_from_mail = email_from_mail,
                email_from = email_from,
                email_to = follower.email,
                link = "sign/document/%(request_id)s/%(access_token)s" % {'request_id': self.id, 'access_token': self.access_token},
                subject = subject or ("Signature request - " + self.reference),
                msgbody = (message or "").replace("\n", "<br/>")
            )
            mail = template.send_mail(self.id, force_send=True)

            # if self._context['fal_lead_id']:
            #         self.env['mail.mail'].browse(mail).fal_lead_id = self._context['fal_lead_id']

        return True

    @api.multi
    def send_completed_document(self):
        self.ensure_one()
        if len(self.request_item_ids) <= 0 or self.state != 'signed':
            return False

        if not self.completed_document:
            self.generate_completed_document()

        base_context = self.env.context
        template_id = self.env.ref('website_sign.website_sign_mail_template').id
        mail_template = self.env['mail.template'].browse(template_id)

        email_from_usr = self.create_uid.partner_id.name
        email_from_mail = self.create_uid.partner_id.email
        email_from = "%(email_from_usr)s <%(email_from_mail)s>" % {'email_from_usr': email_from_usr, 'email_from_mail': email_from_mail}

        mail_template = mail_template.sudo().with_context(base_context,
            template_type = "completed",
            email_from_usr = email_from_usr,
            email_from_mail = email_from_mail,
            email_from = email_from,
            subject = "Signed Document - " + self.reference
        )

        for signer in self.request_item_ids:
            if not signer.partner_id:
                continue
            template = mail_template.with_context(
                lang = signer.partner_id.lang,
                email_to = signer.partner_id.email,
                link = "sign/document/%(request_id)s/%(access_token)s" % {'request_id': self.id, 'access_token': signer.access_token}
            )
            template.send_mail(self.id, force_send=True)

        for follower in self.follower_ids:
            template = mail_template.with_context(
                lang = follower.lang,
                email_to = follower.email,
                link = "sign/document/%(request_id)s/%(access_token)s" % {'request_id': self.id, 'access_token': self.access_token}
            )
            template.send_mail(self.id, force_send=True)

        mail = mail_template.with_context( # Send copy to request creator
            email_to = email_from_mail,
            link = "sign/document/%(request_id)s/%(access_token)s" % {'request_id': self.id, 'access_token': self.access_token}
        ).send_mail(self.id, force_send=True)

        # if self._context['fal_lead_id']:
        #     self.env['mail.mail'].browse(mail).fal_lead_id = self._context['fal_lead_id']

        return True


class SignatureRequestItem(models.Model):
    _inherit = "signature.request.item"

    @api.multi
    def send_signature_accesses(self, subject=None, message=None):
        base_context = self.env.context
        template_id = self.env.ref('website_sign.website_sign_mail_template').id
        mail_template = self.env['mail.template'].browse(template_id)

        email_from_usr = self[0].create_uid.partner_id.name
        email_from_mail = self[0].create_uid.partner_id.email
        email_from = "%(email_from_usr)s <%(email_from_mail)s>" % {'email_from_usr': email_from_usr, 'email_from_mail': email_from_mail}

        for signer in self:
            if not signer.partner_id:
                continue
            template = mail_template.sudo().with_context(base_context,
                lang = signer.partner_id.lang,
                template_type = "request",
                email_from_usr = email_from_usr,
                email_from_mail = email_from_mail,
                email_from = email_from,
                email_to = signer.partner_id.email,
                link = "sign/document/%(request_id)s/%(access_token)s" % {'request_id': signer.signature_request_id.id, 'access_token': signer.access_token},
                subject = subject or ("Signature request - " + signer.signature_request_id.reference),
                msgbody = (message or "").replace("\n", "<br/>")
            )
            mail = template.send_mail(signer.signature_request_id.id, force_send=True)
            # if self._context['fal_lead_id']:
            #     self.env['mail.mail'].browse(mail).fal_lead_id = self._context['fal_lead_id']
