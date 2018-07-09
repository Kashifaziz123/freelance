
# from odoo import models, fields, api

from dateutil import relativedelta
import dateutil.relativedelta
import datetime
from datetime import date
from datetime import datetime , timedelta
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT
from odoo import api, fields, models, _
from odoo.osv import expression
from odoo.tools import float_is_zero
from odoo.tools import float_compare, float_round, float_repr
from odoo.tools.misc import formatLang
from odoo.exceptions import UserError, ValidationError

import time
import math

class ParticularReport(models.AbstractModel):
    _name = 'report.daily_invoice_report.report_dailyinvoice_report'
    
    @api.model
    def render_html(self, docids, data=None):
#         unit_prices = {}
        group_by_user = {}
        department = []
        lines =[]
        
        report_obj = self.env['report']
        
        
        report = report_obj._get_report_from_name('daily_invoice_report.report_dailyinvoice_report')
        if data['form']['user_id']:
            users_objs=self.env['res.users'].search([('id','in',data['form']['user_id'])])
        else:
            users_objs=self.env['res.users'].search([])
            
        sorted_user_ids= sorted(users_objs,key=lambda x:(x.name))
        if data['form']['category']:
            depart_objs =self.env['product.category'].search([('id','in',data['form']['category'])])
        
        else:
            depart_objs =self.env['product.category'].search([])
        sorted_depart_ids= sorted(depart_objs,key=lambda x:(x.name))
        
        #for doctor
        date_from = datetime.strptime(data['form']['date_from'], '%Y-%m-%d %H:%M:%S')+ timedelta(hours=5)
        date_to = datetime.strptime(data['form']['date_to'], '%Y-%m-%d %H:%M:%S')+ timedelta(hours=5)
        
        
        s_date_to = date_to.strftime('%d/%m/%y %H:%M:%S'),

        s_date_from =date_from.strftime('%d/%m/%y %H:%M:%S'),
        for sorted_user_id in sorted_user_ids:
            for sorted_depart_id in sorted_depart_ids:
                invoice_obj= self.env['account.invoice.line']
                invoice_ids = invoice_obj.search([
                                                   
                                                   ('invoice_id.date_invoice','>=',s_date_from),
                                                   ('invoice_id.date_invoice','<=',s_date_to),
                                                   ('invoice_id.user_id','=',sorted_user_id.id),
                                                    ('product_id.categ_id','=',sorted_depart_id.id)])

                 
                depart_due_sum=0
                depart_total_sum=0
                for invoice_line_id in invoice_ids:
#                     date = time.strptime(invoice_id.date,'%d/%m/%Y')
                    
                    
                    inv_date=datetime.strptime(invoice_line_id.invoice_id.date_invoice, '%Y-%m-%d %H:%M:%S')- timedelta(hours=7) 
#                     datetime.strptime(invoice_line_id.invoice_id.date_invoice, '%Y-%m-%d').strftime('%d/%m/%y'),
                    if  invoice_line_id.invoice_id.type == 'out_refund':
                        discount_amount = -invoice_line_id.invoice_id.amount_discount or 0.0
                        total_amount = -invoice_line_id.invoice_id.amount_total or 0.0
                    else:
                        discount_amount = invoice_line_id.invoice_id.amount_discount or 0.0
                        total_amount = invoice_line_id.invoice_id.amount_total
                        
                    vals = {
                            'shift':data['form']['shift'] or '',
#                             'date_from':data['form']['date_from'],
#                             'date_to':data['form']['date_to'],
                            'inv':invoice_line_id.invoice_id.number,
                            'date':inv_date.strftime('%d/%m/%y %I:%M:%S %P'),
                            'pat_name': invoice_line_id.invoice_id.op_name,
                            'inpat_name': invoice_line_id.invoice_id.patient.name,
                            'referral_dr':invoice_line_id.invoice_id.ref_by.name,
#                             'product_id':invoice_line_id.invoice_id.invoice_line_ids[0].product_id.name,
                            'product_id':invoice_line_id.product_id.name,
#                             'total_amount': invoice_line_id.invoice_id.amount_total,
#                             invoice_id.amount_discount or
                            'discount_amount': discount_amount,
                            'due_amount': invoice_line_id.invoice_id.residual,
                            'total_amount': total_amount,
                            'department':invoice_line_id.product_id.categ_id.name or '',
#                             'department':invoice_id.reporting_department.name,
                        }
                    depart_due_sum +=invoice_line_id.invoice_id.residual
                    depart_total_sum +=invoice_line_id.invoice_id.amount_total
                    lines.append(vals)
            
                if invoice_ids:
                    department.append({sorted_depart_id.name: lines})
#                                        'depart_due_sum':depart_due_sum,
#                                        'depart_total_sum':depart_total_sum
                    lines =[]
                
            group_by_user.update({sorted_user_id.name : department,
                                  })
#             'date_to':data['form']['date_to'],
#                                  'date_from':data['form']['date_from']
            department = []
            
         
        docargs = {
            'data' : group_by_user,
#             'unit_prices' : unit_prices,
#             'date_to':datetime.strptime(data['form']['date_to'], '%Y-%m-%d %H:%M:%S').strftime('%d/%m/%y %H:%M:%S'),
            'date_to':date_to.strftime('%d/%m/%y %I:%M:%S %P'),

            'date_from':date_from.strftime('%d/%m/%y %I:%M:%S %P'),
            'shift':data['form']['shift'],
            'doc_ids': docids,
            'doc_model': report.model,
            'docs': self,
        }
        return report_obj.render('daily_invoice_report.report_dailyinvoice_report', docargs)
        
#         for stock_picking in stock_pickings:
#             product_price = self.get_product_price(stock_picking)
#             if product_price:
#                 unit_prices.update({stock_picking.id : product_price})
#             else:
#                 unit_prices.update({stock_picking.id : False})
#         docargs = {
#             'data' : stock_pickings,
#             'unit_prices' : unit_prices,
#             'doc_ids': docids,
#             'doc_model': report.model,
#             'docs': self,
#         }

    
    def get_product_price(self, stock_picking):
        unit_prices = {}
        order_lines = self.env['sale.order'].search([('name','=',stock_picking.origin)]).order_line
        if order_lines:
            for order_line in order_lines:
                if order_line.price_unit:
                    unit_prices.update({order_line.product_id.id : {'price':order_line.price_unit,'tax':order_line.tax_id.amount,'discount':order_line.discount,}})
        else:
            unit_prices.update({stock_picking.id : False})
        return unit_prices
            