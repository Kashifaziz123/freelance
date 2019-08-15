odoo.define('fleet_gps_tracking.FieldMap', function(require) {
"use strict";
var core = require('web.core');
var form_common = require('web.form_common');
var map;
var Widget = require("web.Widget");
var Model = require("web.Model");
var form_common = require('web.form_common');
var _t = core._t;
var QWeb = core.qweb;
var load_count;
var FieldMap =form_common.AbstractField.extend({
    template: 'FieldMap',
    start: function() {
    var self = this;
    load_count=0;
    self.initmap();
},
initmap:function(){
var self = this;
var data = this.field_manager.get_field_value('imei');
if (data){
 try{
var myOptions = {
        zoom: 9,
        mapTypeId: google.maps.MapTypeId.ROADMAP
}
  var marker;
  var xmlHttp = new XMLHttpRequest();
    xmlHttp.open("GET", 'https://api.afaqy.in/?r=userTrackers/lastUpdate&data=%7b%22apiKey%22:%2213ade3d216c5eb5383e4cf9508165899%22,%22imei%22:%22'+data+'%22,%22serverId%22:2%7d', false ); // false for synchronous request
    xmlHttp.send( null );
  var parsedData = JSON.parse(xmlHttp.responseText);
  var uluru = {lat: parseFloat(parsedData['data']['lastUpdate']['onLocation']['lat']), lng: parseFloat(parsedData['data']['lastUpdate']['onLocation']['lng'])};
  var map= new google.maps.Map(this.el,  {
  center: uluru,
  zoom: 9
});
  // The marker, positioned at Uluru

  setInterval(function(){
  if (load_count>0){
 xmlHttp = new XMLHttpRequest();
    xmlHttp.open("GET", 'https://api.afaqy.in/?r=userTrackers/lastUpdate&data=%7b%22apiKey%22:%2213ade3d216c5eb5383e4cf9508165899%22,%22imei%22:%22'+data+'%22,%22serverId%22:2%7d', false ); // false for synchronous request
    xmlHttp.send( null );
 parsedData = JSON.parse(xmlHttp.responseText);
 uluru = {lat: parseFloat(parsedData['data']['lastUpdate']['onLocation']['lat']), lng: parseFloat(parsedData['data']['lastUpdate']['onLocation']['lng'])};
 }
 var contentString = '<p>'+parsedData['data']['name']+'</p><p>'+parsedData['data']['lastUpdate']['onSpeed']+'</p>';
 // The location of Uluru
 var infowindow;
 if (marker!=null){
   marker.setPosition(uluru);
 if (parsedData['data']['lastUpdate']['onSpeed']>0)
 {
 marker.setIcon('http://maps.google.com/mapfiles/ms/icons/green-dot.png');
 }
 else{
 marker.setIcon('http://maps.google.com/mapfiles/ms/icons/red-dot.png');
 }
 }
  else{
 console.log('not exist...............',parsedData['data']['lastUpdate']['onSpeed']);
 if (parsedData['data']['lastUpdate']['onSpeed']>0)
 {
  marker = new google.maps.Marker({position: uluru, map: map,icon: {
      url: "http://maps.google.com/mapfiles/ms/icons/green-dot.png"
}});
 }
 else{
  marker = new google.maps.Marker({position: uluru, map: map,icon: {
      url: "http://maps.google.com/mapfiles/ms/icons/red-dot.png"
 }
});
 }
 }
  marker.infowindow = new google.maps.InfoWindow({
          content: contentString
        });
         marker.addListener('click', function() {
         marker.infowindow.open(map, marker);
        });
    load_count+=1;
    }
    ,5000);
}
catch(err){
  alert ("Internet Issue or Issue with APIKEY");
     return 1;
}
}
}
});
 core.form_widget_registry.add('map', FieldMap);
return {
    FieldMap: FieldMap,
};
});