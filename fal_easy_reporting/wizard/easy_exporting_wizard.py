# -*- coding: utf-8 -*-

from odoo import api, fields, models, _


class easy_exporting_wizard(models.TransientModel):
    _name = "easy.exporting.wizard"
    _description = "Easy Exporting Wizard"

    model_id = fields.Many2one(
        'ir.model',
        'Object',
        required=True,
        ondelete='cascade',
        help="Select the object on which want to be download."
    )
    resource = fields.Char('Resource', size=128)
    template_id = fields.Many2one(
        'ir.exports',
        string='Template',
        required=True,
        help="Select the template on which want to be download."
    )
    filter_ids = fields.Many2many(
        'ir.filters',
        'easy_export_filter_rel',
        'easy_export_id',
        'filter_id',
        string='Filter',
        help="Select the filter on which want to be download."
    )
    from_date = fields.Date('From')
    to_date = fields.Date('To')
    temp = fields.Text('temp')
    temp_domain = fields.Text('Domain')
    temp_file = fields.Binary('File')
    temp_file_name = fields.Char('name', size=64)
    file_format = fields.Selection([
        ('Excel', 'Excel'),
        ('CSV', 'CSV')],
        string='File Format',
        required=True,
        default='Excel'
    )

    @api.multi
    def onchange_model_id(self, model_id):
        res = {}
        model_obj = self.env['ir.model']
        res['value'] = {'resource': False, 'template_id': False, 'temp': '', 'filter_ids': [], 'temp_filter_ids': ''}
        if model_id:
            model = model_obj.browse(model_id)
            res['value'] = {'resource': model.model, 'template_id': False, 'temp': '', 'filter_ids': [], 'temp_filter_ids': ''}
        return res

    @api.multi
    def onchange_template_id(self, template_id):
        res = {}
        export_obj = self.env['ir.exports']
        if template_id:
            export = export_obj.browse(template_id)
            temp_field = []
            for field in export.export_fields:
                temp_field.append(field.name)
            out = ','.join(temp_field)
            res['value'] = {'temp': out}
        return res

    @api.multi
    def onchange_filter_ids(self, filter_ids, from_date, to_date, resource):
        res = {}
        filter_obj = self.env['ir.filters']
        res['value'] = {'temp_domain': ''}
        out = ''
        temp_domain = []
        if not filter_ids:
            for filter in filter_obj.browse(filter_ids[0][2]):
                for dom in eval(filter.domain):
                    temp_domain.append(dom)
        if from_date and to_date:
            resource_obj = self.env[resource]
            resource_fields = resource_obj.fields_get()
            if 'date' in resource_fields:
                temp_domain.append(['date', '>=', from_date])
                temp_domain.append(['date', '<=', to_date])
            else:
                temp_domain.append(['create_date', '>=', from_date])
                temp_domain.append(['create_date', '<=', to_date])
        out += str(temp_domain)
        res['value'] = {'temp_domain': out}
        return res

    """
    def action_next(self, cr, uid, ids, context=None):
        if context is None:
            context = {}
        data_wizard = self.browse(cr, uid, ids, context)[0]
        object_obj = self.pool.get(data_wizard.model_id.model)
        obj_ids = object_obj.search(cr, uid, [], context=context)
        temp_field = []
        for field in data_wizard.template_id.export_fields:
            temp_field.append(field.name)
        export = object_obj.read(cr, uid, obj_ids, temp_field, context=context)
        out=base64.encodestring(str(export))
        #print export

        #modif start
        fp = StringIO()
        writer = csv.writer(fp, quoting=csv.QUOTE_ALL)
        writer.writerow([name.encode('utf-8') for name in temp_field])
        for data in export:
            row = []
            for l,d in data.items():
                if isinstance(d, basestring):
                    d = d.replace('\n',' ').replace('\t',' ')
                    try:
                        d = d.encode('utf-8')
                    except UnicodeError:
                        pass
                if d is False: d = None
                row.append(d)
            writer.writerow(row)
        fp.seek(0)
        data = fp.read()
        fp.close()
        #print data
        self.write(cr, uid, ids, {'state': 'done', 'temp_file':data, 'temp_file_name': data_wizard.model_id.model + '.csv'})
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'easy.exporting.wizard',
            'view_mode': 'form',
            'view_type': 'form',
            'res_id': ids[0],
            'views': [(False, 'form')],
            'target': 'new',
             }
    """
# end of easy_exporting_wizard()
