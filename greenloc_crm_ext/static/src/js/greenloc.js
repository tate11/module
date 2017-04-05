odoo.define('greenloc.greenloc_crm_ext', function (require) {
"use strict";
var core = require('web.core');
var SalesTeamDashboardView = require('sales_team.dashboard');
var KanbanColumn = require('web_kanban.Column');
var Model = require('web.Model');
var KanbanView = require('web_kanban.KanbanView');
var QWeb = core.qweb;
var quick_create = require('web_kanban.quick_create');
var UserMenu = require('web.UserMenu');
var session = require('web.session');
var ColumnQuickCreate = quick_create.ColumnQuickCreate;

KanbanColumn.include({
    start: function() {
        if (this.record_options.model === "crm.lead"){
            this.draggable = false;
        }
        this._super.apply(this, arguments);
    },
});

KanbanView.include({
    render_grouped: function (fragment) {
        // This method is override version of original
        var self = this;

        // FORWARDPORT UP TO SAAS-10, NOT IN MASTER!
        // Drag'n'drop activation/deactivation
        var group_by_field_attrs = this.fields_view.fields[this.group_by_field];

        // Group_by field might not be in the Kanban view, so we need to get it somewhere else...
        // This somewhere else is on the search view.
        if (group_by_field_attrs === undefined) {
            if (this.ViewManager.searchview.groupby_menu && this.ViewManager.searchview.groupby_menu.groupable_fields) {
                group_by_field_attrs = _.find(this.ViewManager.searchview.groupby_menu.groupable_fields, function(field) {
                    return field.name === self.group_by_field;
                })
            }
        }
        // Deactivate the drag'n'drop if:
        // - field is a date or datetime since we group by month
        // - field is readonly
        var draggable = true;
        if (group_by_field_attrs) {
            if (group_by_field_attrs.type === "date" || group_by_field_attrs.type === "datetime") {
                var draggable = false;
            }
            else if (group_by_field_attrs.readonly !== undefined) {
                var draggable = !(group_by_field_attrs.readonly);
            }
        }
        var record_options = _.extend(this.record_options, {
            draggable: draggable,
        });

        var column_options = this.get_column_options();

        _.each(this.data.groups, function (group) {
            var column = new KanbanColumn(self, group, column_options, record_options);
            column.appendTo(fragment);
            self.widgets.push(column);
        });
        //change falinwa in here
        if (this.model != 'crm.lead') {
            this.$el.sortable({
                axis: 'x',
                items: '> .o_kanban_group',
                handle: '.o_kanban_header',
                cursor: 'move',
                revert: 150,
                delay: 100,
                tolerance: 'pointer',
                forcePlaceholderSize: true,
                stop: function () {
                    var ids = [];
                    self.$('.o_kanban_group').each(function (index, u) {
                        ids.push($(u).data('id'));
                    });
                    self.resequence(ids);
                },
            });
        }
        if (this.is_action_enabled('group_create') && this.grouped_by_m2o) {
            this.column_quick_create = new ColumnQuickCreate(this);
            this.column_quick_create.appendTo(fragment);
        }
        this.postprocess_m2m_tags();
    },
});

});