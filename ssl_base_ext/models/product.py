from odoo import fields, models, api
import logging
_logger = logging.getLogger(__name__)


class productTemplate(models.Model):
    _inherit = 'product.template'

    fal_internal_name = fields.Char(string='Internal Name')
    # Compute and inverse commented to not change product template ref
    default_code = fields.Char(
        'Internal Reference', compute='',
        inverse='', store=True)

    # Add the fields Length / Width / Height
    fal_length_uom_id = fields.Many2one(
        'product.uom', string='Length UoM',
        default=lambda self: self.env.ref(
            'fal_product_size_detail.fal_uom_milimeter'
        ).id
    )
    fal_width_uom_id = fields.Many2one(
        'product.uom', string='Width UoM',
        default=lambda self: self.env.ref(
            'fal_product_size_detail.fal_uom_milimeter'
        ).id
    )
    fal_height_uom_id = fields.Many2one(
        'product.uom', string='Height UoM',
        default=lambda self: self.env.ref(
            'fal_product_size_detail.fal_uom_milimeter'
        ).id
    )

    @api.multi
    def name_get(self):
        res = super(productTemplate, self).name_get()
        res_dict = {}
        new_res = []
        for item in res:
            res_dict[item[0]] = item[1]
            product = self.browse(item[0])
            if product.fal_old_ref:
                if product.default_code and product.default_code in item[1]:
                    parts = item[1].split('[' + product.default_code + ']')
                    name = '[' + product.default_code + '] ' +\
                        product.fal_old_ref + ' -' + parts[1]
                    new_res.append((product.id, name))
                else:
                    name = product.fal_old_ref + ' - ' + item[1]
                    new_res.append((product.id, name))
            else:
                new_res.append((product.id, item[1]))
        return new_res


class ProductProduct(models.Model):
    _inherit = 'product.product'

    fal_client_ref = fields.Char(string='Client Reference')

    # Add the fields Length / Width / Height
    fal_length_uom_id = fields.Many2one(
        'product.uom', string='Length UoM',
        default=lambda self: self.env.ref(
            'fal_product_size_detail.fal_uom_milimeter'
        ).id
    )
    fal_width_uom_id = fields.Many2one(
        'product.uom', string='Width UoM',
        default=lambda self: self.env.ref(
            'fal_product_size_detail.fal_uom_milimeter'
        ).id
    )
    fal_height_uom_id = fields.Many2one(
        'product.uom', string='Height UoM',
        default=lambda self: self.env.ref(
            'fal_product_size_detail.fal_uom_milimeter'
        ).id
    )

    @api.multi
    def name_get(self):
        res = super(ProductProduct, self).name_get()
        res_dict = {}
        new_res = []
        for item in res:
            res_dict[item[0]] = item[1]
            product = self.browse(item[0])
            if product.fal_old_ref:
                if product.default_code and product.default_code in item[1]:
                    parts = item[1].split('[' + product.default_code + ']')
                    name = '[' + product.default_code + '] ' +\
                        product.fal_old_ref + ' -' + parts[1]
                    new_res.append((product.id, name))
                else:
                    name = product.fal_old_ref + ' - ' + item[1]
                    new_res.append((product.id, name))
            else:
                new_res.append((product.id, item[1]))
        return new_res

    @api.depends(
        'product_tmpl_id',
        'product_tmpl_id.default_code')
    def get_fal_internal_ref(self):
        for prod in self:
            new_code = ''
            first = prod.product_tmpl_id.default_code or False
            new_code = str(prod.id)
            if first:
                new_code = first + ' | ' + new_code
            prod.default_code = new_code
