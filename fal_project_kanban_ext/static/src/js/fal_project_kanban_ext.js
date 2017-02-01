odoo.define('fal_project_kanban_ext.KanbanView', function(require) {
    var core = require('web.core');
    var Model = require('web.DataModel');
    var data = require('web.data');
    var utils = require('web.utils');
    var KanbanRecord = require('web_kanban.Record');
    var KanbanView = require('web_kanban.KanbanView');
    var kanban_widgets = require('web_kanban.widgets');
    var KanbanColumn = require('web_kanban.Column');
    var fields_registry = kanban_widgets.registry;
    var QWeb = core.qweb;
    var _t = core._t;

    KanbanView.include({

        /*
         *  postprocessing of fields type many2many
         *  make the rpc request for all ids/model and insert value inside .oe_tags fields
         */
        postprocess_m2m_tags: function(records) {
            var self = this;
            if (!this.many2manys.length) {
                return;
            }
            var relations = {};
            records = records ? (records instanceof Array ? records : [records]) :
                      this.grouped ? Array.prototype.concat.apply([], _.pluck(this.widgets, 'records')) :
                      this.widgets;

            records.forEach(function(record) {
                self.many2manys.forEach(function(name) {
                    var field = record.record[name];
                    var $el = record.$('.oe_form_field.o_form_field_many2manytags[name=' + name + ']');
                    if (self.model == "project.task" || self.model == "project.issue"){
                        if (record.record.tag_ids.raw_value.length == 0){
                            $el = record.$('.oe_form_field.o_form_field_many2manytags[name=' + name + ']')
                            .css("padding-left","3px");
                        }else if (record.record.tag_ids.raw_value.length > 0 && record.record.tag_ids.raw_value.length < 4){
                            $el = record.$('.oe_form_field.o_form_field_many2manytags[name=' + name + ']')
                            .css("padding-left","3px")
                            .css("min-height","17px");
                        }else{
                            $el = record.$('.oe_form_field.o_form_field_many2manytags[name=' + name + ']')
                            .css("overflow","auto")
                            .css("padding-left","3px")
                            .css("min-height","36px");
                        };
                    };
                    // fields declared in the kanban view may not be used directly
                    // in the template declaration, for example fields for which the
                    // raw value is used -> $el[0] is undefined, leading to errors
                    // in the following process. Preventing to add push the id here
                    // prevents to make unnecessary calls to name_get
                    if (! $el[0]) {
                        return;
                    }
                    if (!relations[field.relation]) {
                        relations[field.relation] = { ids: [], elements: {}, context: self.m2m_context[name]};
                    }
                    var rel = relations[field.relation];
                    field.raw_value.forEach(function(id) {
                        rel.ids.push(id);
                        if (!rel.elements[id]) {
                            rel.elements[id] = [];
                        }
                        rel.elements[id].push($el[0]);
                    });
                });
            });
           _.each(relations, function(rel, rel_name) {
                var dataset = new data.DataSetSearch(self, rel_name, self.dataset.get_context(rel.context));
                var call = false
                dataset.read_ids(_.uniq(rel.ids), ['name', 'color']).done(function(result) {
                    if(!call){
                        result.forEach(function(record) {
                            // Does not display the tag if color = 0
                            if (record['color']){
                                if (self.model == "project.task" || self.model == "project.issue"){
                                    var $tag = $('<span>')
                                        .addClass('o_tag o_tag_color_' + record['color'])
                                        .text(_.str.escapeHTML(record.name))
                                        .css("width", "auto")
                                        .css("height", "auto")
                                        .css("font-size", "75%")
                                        .css("font-weight", "bold")
                                        .css("color", "white")
                                        .css("padding-top", "1px")
                                        .css("padding-bottom", "1px")
                                        .css("padding-left", "5px")
                                        .css("padding-right", "5px")
                                        .css("border-radius", "15px")
                                        .css("margin-right", "2px")
                                        .attr('title', _.str.escapeHTML(record['name']));
                                    $(rel.elements[record['id']]).append($tag);
                                }
                                else{
                                    var $tag = $('<span>')
                                        .addClass('o_tag o_tag_color_' + record['color'])
                                        .attr('title', _.str.escapeHTML(record['name']));
                                    $(rel.elements[record['id']]).append($tag);
                                }
                            }
                        });
                    }
                    // we use boostrap tooltips for better and faster display
                    self.$('span.o_tag').tooltip({delay: {'show': 50}});
                });
            });
        },
    });

});