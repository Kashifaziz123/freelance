odoo.define('ga_saatchi_bidding.tree_view_button', function (require){
"use strict";


var core = require('web.core');
var ListView = require('web.ListView');
var QWeb = core.qweb;
var KanbanView = require('web_kanban.KanbanView');

KanbanView.include({

        render_buttons: function($node) {
                var self = this;
                this._super($node);

                    try{
                    this.$buttons.find('.kanbanmap').click(this.proxy('kanban_view_action'));
}
catch(err)
{

}
        },

        kanban_view_action: function () {
        this.do_action({
                type: "ir.actions.client",
                tag: "mapall"
        });

         return { 'type': 'ir.actions.client','tag': 'reload', } }

});

});