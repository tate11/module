from odoo import models, fields, api


class StockMove(models.Model):
    _inherit = 'stock.move'

    fal_old_ref = fields.Char(
        string='Old Ref.',
        compute='get_old_ref',
    )

    @api.depends(
        'product_id', 'product_id.product_tmpl_id',
        'product_id.product_tmpl_id.fal_old_ref')
    def get_old_ref(self):
        for line in self:
            line.fal_old_ref = line.product_id.product_tmpl_id.fal_old_ref

    @api.multi
    def show_bom_structure(self):
        for line in self:
            return line.product_id.product_tmpl_id.get_bom_structure()


class StockPackOperation(models.Model):
    _inherit = 'stock.pack.operation'

    fal_old_ref = fields.Char(
        string='Old Ref.',
        compute='get_old_ref',
    )

    @api.depends(
        'product_id', 'product_id.product_tmpl_id',
        'product_id.product_tmpl_id.fal_old_ref')
    def get_old_ref(self):
        for line in self:
            line.fal_old_ref = line.product_id.product_tmpl_id.fal_old_ref

    @api.multi
    def show_bom_structure(self):
        for line in self:
            return line.product_id.product_tmpl_id.get_bom_structure()
