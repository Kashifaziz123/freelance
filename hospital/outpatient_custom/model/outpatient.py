from odoo import api, SUPERUSER_ID, fields, models, _
import time
from dateutil import relativedelta
import dateutil.relativedelta
import datetime
from datetime import date
from datetime import datetime , timedelta

class account_invoice(models.Model):
    _inherit = 'account.invoice'
    
    
    
    out_patient=fields.Boolean(string='Out Patient')
    date_invoice = fields.Datetime(string='Invoice Date',
        readonly=True, states={'draft': [('readonly', False)]}, index=True,
        help="Keep empty to use the current date", copy=False,default=fields.Datetime.now)
    
#     patient information
    op_id=fields.Char(string="Outpatient ID")
    op_name=fields.Char(string="Outpatient Name")
    relation_name=fields.Char(string="Attendent Name")
    realtionship= fields.Selection([('m', 'Mother'),('F', 'Father'),('s','Son'),('d','Daughter'),('u','Uncle'),('etc','Others')])
    o_age=fields.Char('Age')
    o_cnic= fields.Char('CNIC No')
    o_mobile= fields.Char('Mobile No')
    o_sex =fields.Selection([('male', 'Male'),('Female', 'Female'),('other','Not Disclosed')],string="Gender")
    o_patient_address=fields.Char('Address')
    
#     panel information
    approved_by=fields.Many2one('oeh.medical.physician')
    internal_no = fields.Char(string="NCCI Approval No.")
    date_inter_appr= fields.Datetime('Approval Date',default=fields.Datetime.now)
    panel_ref_no= fields.Char(string="Panel's Ref. No.")
    
#  physician ref

    ref_by=fields.Many2one('oeh.medical.physician')
    ref_no = fields.Char(string="Referral No.")
    remark= fields.Char(string="Dr.'s Remarks")
    date_ref_by= fields.Datetime('Reporting Date',default=fields.Datetime.now)
    reporting_department= fields.Many2one('product.category')


    indent_no= fields.Char(string="Dr Indent No.")
#    for capitalize the Outpatient Name
#     @api.onchange('op_name')
#    def set_caps(self):
#         val = str(self.op_name)
#         self.op_name = val.upper()		 
 
#     invoc attr
#     staff = fields.Char(string="Staff")
#     department= fields.Char(string="Department")
#     due_date= fields.Date('Dur Date',default=time.strftime('%Y-%m-01'))
    inv_remark= fields.Char(string="Staff's Remarks")
    
    _sql_constraints = [('op_id', 'unique(op_id)', 'The Outpatient ID must be unique')]



    



    
