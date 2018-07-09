odoo.define('account_invoice_indent.patient_template', function (require) {
"use strict";

var popup = require('point_of_sale.popups');
var gui = require('point_of_sale.gui');
var screens = require('point_of_sale.screens');
var core = require('web.core');
var Model = require('web.DataModel');
var models = require('point_of_sale.models');

var QWeb = core.qweb;
var _t = core._t;

models.load_fields('res.partner', ['is_patient']);

	screens.ClientListScreenWidget.include({
		show: function(){
			var self = this;
			this._super();

			this.renderElement();
			this.details_visible = false;
			this.old_client = this.pos.get_order().get_client();

			this.$('.back').click(function(){
				self.gui.back();
			});

			this.$('.next').click(function(){   
				self.save_changes();
				var client = false;
				if ((self.new_client) && (self.new_client.is_patient)){
					client = self.new_client
				}
				else{
					client = this.old_client 
				}
				if ((client) && (client.is_patient)){
					var domain = [['partner_id', '=', client.id]]
					new Model('oeh.medical.patient')
					.query(['id','name','identification_code'])
					.filter(domain)
					.all({'timeout': 1000, 'shadow': true})
					.then(function( j ){
						if (j[0]){
							new Model('oeh.medical.inpatient')
							.query(['id','name','state'])
							.filter([['patient', '=', j[0].id],['state', '=','Hospitalized']])
							.all({'timeout': 1000, 'shadow': true})
							.then(function(inpatient){
								if (inpatient.length > 0){
									self.gui.show_popup('patient-template',{'title': core._t('Inpatient Admissions')});
									self.pos.number = name
									_.each(inpatient, function(i){
										$("<option></option>", 
											{value: i.id, text: i.name }).appendTo('#inpatient_id');
									});
								}
								else{
									self.gui.back();
									self.pos.inpatient_id = false;
									self.pos.indent_no = false;
									self.pos.number = false;
									self.pos.patient_name = false;
									self.pos.identification_code = false;
								}
							});
						}
						else{
							self.gui.back();
							self.pos.inpatient_id = false;
							self.pos.indent_no = false;
							self.pos.number = false;
							self.pos.patient_name = false;
							self.pos.identification_code = false;
						}
					});
				}	
				else{
					self.gui.back();    // FIXME HUH ?
					self.pos.inpatient_id = false;
					self.pos.indent_no = false;
					self.pos.number = false;
					self.pos.patient_name = false;
					self.pos.identification_code = false;
				}
			});

			this.$('.new-customer').click(function(){
				self.display_client_details('edit',{
					'country_id': self.pos.company.country_id,
				});
			});

			var partners = this.pos.db.get_partners_sorted(1000);
			this.render_list(partners);

			this.reload_partners();

			if( this.old_client ){
				this.display_client_details('show',this.old_client,0);
			}

			this.$('.client-list-contents').delegate('.client-line','click',function(event){
				self.line_select(event,$(this),parseInt($(this).data('id')));
			});

			var search_timeout = null;

			if(this.pos.config.iface_vkeyboard && this.chrome.widget.keyboard){
				this.chrome.widget.keyboard.connect(this.$('.searchbox input'));
			}

			this.$('.searchbox input').on('keypress',function(event){
				clearTimeout(search_timeout);

				var query = this.value;

				search_timeout = setTimeout(function(){
					self.perform_search(query,event.which === 13);
				},70);
			});

			this.$('.searchbox .search-clear').click(function(){
				self.clear_search();
			});
		},
	});
	
	var PatientTemplate = popup.extend({
		template: 'PatientTemplate',
		show: function(options){
			options = options || {};
			this._super(options);
		},
		click_confirm: function(){
			
			var self = this;
			var inpatient_id = this.$('#inpatient_id').val();
			var indent_no = this.$('#indent_no').val();
			var cont = this;
			self.pos.inpatient_id = this.$('#inpatient_id').val();
			self.pos.indent_no = this.$('#indent_no').val();
			new Model('oeh.medical.inpatient')
			.query(['id','name','state','patient'])
			.filter([['id', '=', inpatient_id]])
			.all({'timeout': 1000, 'shadow': true})
			.then(function(inpatient){
				if (inpatient.length > 0){
					self.pos.number = inpatient[0].name;
					if (inpatient[0].patient){
						new Model('oeh.medical.patient')
						.query(['id','name','identification_code'])
						.filter([['id','=',inpatient[0].patient[0]]])
						.all({'timeout': 1000, 'shadow': true})
						.then(function(patient){
							if (patient.length > 0){
								self.pos.patient_name = patient[0].name;
								self.pos.identification_code = patient[0].identification_code;
							}
						});
					}
				}
			});
			if(this.$('#indent_no').val().length > 4) {
				// ---------------- Check Pos Order  Indent No ---------------------------
				new Model('pos.order')
				.query(['id','name','indent_no'])
				.filter([['indent_no','ilike',indent_no]])
				.all({'timeout': 1000, 'shadow': true})
				.then(function(pos){
					if (pos.length > 0){
						self.$('#msg-indent').text('Indent Number must be unique!');
					}
					else{
						self.gui.back();
//						self.pos.inpatient_id = false;
//						self.pos.indent_no = false;
//						self.pos.number = false;
//						self.pos.patient_name = false;
//						self.pos.identification_code = false;
					}
				})
				// ---------------- Check Pos Order Indent No ---------------------------
			}
			else{
				this.$('#msg-indent').text('Indent number length must be five(5) digits.')
			}
		},
		
	});
	
	var _super_order = models.Order.prototype;
		
	models.Order = models.Order.extend({
		export_as_JSON: function() {
			var orderLines, paymentLines;
			orderLines = [];
			this.orderlines.each(_.bind( function(item) {
				return orderLines.push([0, 0, item.export_as_JSON()]);
			}, this));
			paymentLines = [];
			this.paymentlines.each(_.bind( function(item) {
				return paymentLines.push([0, 0, item.export_as_JSON()]);
			}, this));
			return {
				indent_no:this.pos.indent_no,
				inpatient_id:this.pos.inpatient_id,
				name: this.get_name(),
				amount_paid: this.get_total_paid(),
				amount_total: this.get_total_with_tax(),
				amount_tax: this.get_total_tax(),
				amount_return: this.get_change(),
				lines: orderLines,
				statement_ids: paymentLines,
				pos_session_id: this.pos_session_id,
				partner_id: this.get_client() ? this.get_client().id : false,
				user_id: this.pos.cashier ? this.pos.cashier.id : this.pos.user.id,
				uid: this.uid,
				sequence_number: this.sequence_number,
				creation_date: this.validation_date || this.creation_date, // todo: rename creation_date in master
				fiscal_position_id: this.fiscal_position ? this.fiscal_position.id : false
			};
		},
	});
	
	gui.define_popup({name:'patient-template', widget: PatientTemplate});
	
});