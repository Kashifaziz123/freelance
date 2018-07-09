# -*- coding: utf-8 -*-


from odoo import api, fields, models, tools, _

class OutpatientWizard(models.TransientModel):
    _name = 'outpatient.wizard'
    
    partner_id = fields.Many2one('res.partner' , 'Customer')
    
