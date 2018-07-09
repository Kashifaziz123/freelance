#addition of fields such as sales tax no. and national tax no.

from odoo import fields, models, api
from docutils.nodes import field


class Partner(models.Model):
    _inherit = "res.partner"
    
    sales_tax_no = fields.Char('Sales Tax No.')
    nat_tax_no = fields.Char('National Tax No.')