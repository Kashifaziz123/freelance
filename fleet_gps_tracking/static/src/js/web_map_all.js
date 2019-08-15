odoo.define('fleet_gps_tracking.mapall', function(require) {
"use strict";
var core = require('web.core');
var form_common = require('web.form_common');
var map;
var Widget = require("web.Widget");
var Model = require("web.Model");
var _t = core._t;
var QWeb = core.qweb;
var count=0;
var count_mapfit;
var FieldMap = Widget.extend({
    template: 'mapall',
    init: function(parent, args) {
        this._super(parent, args);
        this.options = {};
    }
 ,
    start: function() {

    var self = this;
    count_mapfit=0;
},
});
 core.action_registry.add('mapall', FieldMap);
});