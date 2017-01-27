from odoo import models, fields


class res_company(models.Model):
    _name = "res.company"
    _inherit = "res.company"
    _rec_name = "code"

    code = fields.Char('Code', Size="7", required=True, default=id)

    _sql_constraints = [
        ('code_uniq', 'unique(code)', 'Code must be unique!'),
    ]


"""
class res_currency(orm.Model):
    _name = "res.currency"
    _inherit = "res.currency"

    def name_get(self, cr, uid, ids, context=None):
        if not len(ids):
            return []
        company_obj = self.pool.get('res.company')
        reads = self.read(cr, uid, ids, ['name','symbol','company_id'],
        context=context, load='_classic_write')
        res = []
        for record in reads:
            name = record['name']
            company_code = 'GLB'
            if record['company_id']:
                company_code = company_obj.read(cr, SUPERUSER_ID,
                record['company_id'], ['code'],
                context=context, load='_classic_write')['code'] or ''
            res.append((record['id'], name+'('+ company_code +')'))
        return res

#end of res_currency()
"""
