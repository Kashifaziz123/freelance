from odoo import models, fields, api
import time
from dateutil import relativedelta
import dateutil.relativedelta
import datetime
from datetime import date
from datetime import datetime , timedelta
from odoo.tools import float_is_zero, float_compare, DEFAULT_SERVER_DATETIME_FORMAT
from odoo.tools.misc import formatLang


# class account_invoice(models.Model):
#     _inherit = 'account.invoice'
#     
#     date_invoice = fields.Datetime(string='Invoice Date',
#         readonly=True, states={'draft': [('readonly', False)]}, index=True,
#         help="Keep empty to use the current date", copy=False,default=datetime.today())
#     
#     date_ref_by= fields.Datetime('Reporting Date 2', default=datetime.today())


class StockReport(models.TransientModel):
    _name = "wizard.invoice.history"
    _description = "Current Stock History"
#     date_to= fields.Date("Date To",default=datetime.today())
    date_to=fields.Datetime("Date To",default=fields.Datetime.now)
    date_from= fields.Datetime("Date From", default=fields.Datetime.now)
    category = fields.Many2many('product.category', string='Department')
    shift =fields.Selection([('A', 'A'),('B', 'B'),('C','C')],string="Shift")
#     ref_by_ids = fields.Many2many('oeh.medical.physician', string='Referral Dr')
    user_id = fields.Many2many('res.users',  string='Staff',default=lambda self: self.env.user)
#     @api.model
#     def get_user(self):
#         return self.env['my.tax.tax'].search([('type', 'in', ['income', 'value', 'excise'])]).ids
# 
#     

    @api.multi
    def print_report(self):
        
        data={}
        data['form']= self.read()[0]
        return self.env['report'].get_action(self,'daily_invoice_report.report_dailyinvoice_report',data)