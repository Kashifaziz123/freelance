from odoo import api, SUPERUSER_ID, fields, models, _
import time
from dateutil import relativedelta
import dateutil.relativedelta
import datetime
from datetime import date
from datetime import datetime , timedelta
from odoo.exceptions import ValidationError

class OeHealthPatient(models.Model):
    
    _inherit = 'oeh.medical.patient'
    attendent_name=fields.Char(string="Attendent Name")
    inpatient_realtionship= fields.Selection([('m', 'Mother'),('F', 'Father'),('s','Son'),('d','Daughter'),('u','Uncle'),('etc','Others')],string="Relationship")
    


class OeHealthInpatient(models.Model):
    _inherit = 'oeh.medical.inpatient'
     
#     admission_reason2 = fields.Many2one('oeh.medical.pathology', string='Reason for Admission2', help="Reason for Admission", required=True, readonly=True, states={'Draft': [('readonly', False)]})
 
    admission_date = fields.Datetime(string='Hospitalization Date', readonly=True, default=fields.Datetime.now )
    discharge_date = fields.Datetime(string='Discharge Date', readonly=False, states={'Discharged': [('readonly', True)]})
     
    @api.model
    def create(self, vals):
        res = super(OeHealthInpatient,self).create(vals)
         
        inpatients = self.env['oeh.medical.inpatient'].search([('patient.id','=',res.patient.id),('state','not in',['Discharged','Cancelled'])])
         
        count=0
        for inpatient in inpatients:
            count +=1
             
        if count >1:
         
            raise ValidationError("Patient Already Admitted")
             
        return res
     


class OeHealthPathology(models.Model):
    _name = "oeh.medical.pathology"
    _description = "Diseases"
#     admission_reason2 = fields.Many2one('oeh.medical.pathology', string='Reason for Admission2', help="Reason for Admission", required=True, readonly=True, states={'Draft': [('readonly', False)]})

#     admission_date = fields.Datetime(string='Hospitalization Date', readonly=True, default=fields.Datetime.now )
#     discharge_date = fields.Datetime(string='Discharge Date', readonly=False, states={'Discharged': [('readonly', True)]})
#     
#   

    name = fields.Char(string='Disease Name', size=128, help="Disease name", required=True)
    code = fields.Char(string='Code', size=32, help="Specific Code for the Disease (eg, ICD-10, SNOMED...)")
    category = fields.Many2one('oeh.medical.pathology.category', string='Disease Category')
    chromosome = fields.Char(string='Affected Chromosome', size=128, help="chromosome number")
    protein = fields.Char(string='Protein involved', size=128, help="Name of the protein(s) affected")
    gene = fields.Char(string='Gene', size=128, help="Name of the gene(s) affected")
    info = fields.Text(string='Extra Info')

    _sql_constraints = [
        ('code_uniq', 'unique (code)', 'The disease code must be unique')]

    
