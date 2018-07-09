#This code contains addition of some fields
from odoo import fields, models, api

class AccountInvoice(models.Model):
    _inherit = "account.invoice"
    
    sal_tax_inv = fields.Char('Sale Tax Invoice')


