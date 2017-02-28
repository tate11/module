# -*- encoding: utf-8 -*-
##############################################################################
#
#    Web Easy Switch Company module for OpenERP
#    Copyright (C) 2014 GRAP (http://www.grap.coop)
#    @author Sylvain LE GAL (https://twitter.com/legalsylvain)
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from odoo import fields, models, api, _
from odoo.tools import image_resize_image


class res_company(models.Model):
    _inherit = 'res.company'

    # Custom Section
    @api.multi
    def _switch_company_get_companies_from_partner(self, ids):
        return self.pool['res.company'].search([('partner_id', 'in', ids)])

    # Fields function Section
    @api.multi
    def _get_logo_topbar(self, ids, _field_name, _args):
        result = dict.fromkeys(ids, False)
        for record in self.browse(ids):
            size = (48, 48)
            result[record.id] = image_resize_image(
                record.partner_id.image, size)
        return result

    logo_topbar = fields.Binary(
        compute='_get_logo_topbar',
        string="Logo displayed in the switch company menu",
        store=True
    )
