odoo.define('fal_project_ext.fal_project_ext', function(require) {

var core = require('web.core');
var KanbanRecord = require('web_kanban.Record');
    KanbanRecord.include({
        on_card_clicked: function() {
            if(this.$('.oe_fal_not_in')[0]){
                if(this.$el.find('.oe_kanban_global_click_edit').size()>0)
                    this.trigger_up('kanban_record_edit', {id: this.id});
                else
                    this.trigger_up('kanban_record_open', {id: this.id});
            } else {
                this._super.apply(this, arguments);
            }
        },
    });
});