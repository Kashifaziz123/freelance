# -*- coding: utf-8 -*-


from odoo import api, fields, models, tools, _
from odoo.exceptions import UserError

OUTPATIENT_STATES = [
            ('Draft', 'Draft'),
            ('Invoiced', 'Invoiced'),
        ]

class ResPartner(models.Model):
    _inherit = 'res.partner'
    
    father_name = fields.Char('Father Name')
    age = fields.Char('Age')
  
class PosOrderLine(models.Model):
    _inherit = 'pos.order.line'
    
    admissions_id = fields.Many2one('outpatient.admissions', string='Admissions')

    @api.onchange('product_id')
    def _onchange_product_id(self):
        if self.product_id:
            pricelist_id = False
            if self.order_id and self.order_id.pricelist_id:
                pricelist_id = self.order_id.pricelist_id
                price = self.order_id.pricelist_id.get_product_price(
                    self.product_id, self.qty or 1.0, self.order_id.partner_id)
                self._onchange_qty()
                self.tax_ids = self.product_id.taxes_id.filtered(lambda r: not self.company_id or r.company_id == self.company_id)
                fpos = self.order_id.fiscal_position_id
                ax_ids_after_fiscal_position = fpos.map_tax(self.tax_ids, self.product_id, self.order_id.partner_id) if fpos else self.tax_ids
                self.price_unit = self.env['account.tax']._fix_tax_included_price_company(price, self.product_id.taxes_id, tax_ids_after_fiscal_position, self.company_id)
            else:
                pricelist_id = self.admissions_id.pricelist_id
                if not pricelist_id:
                    raise UserError(_('Select Pricelist First'))
                price = self.admissions_id.pricelist_id.get_product_price(
                    self.product_id, self.qty or 1.0, self.admissions_id.partner_id)
                self._onchange_qty()
                self.tax_ids = self.product_id.taxes_id.filtered(lambda r: not self.company_id or r.company_id == self.company_id)
                fpos = self.admissions_id.fiscal_position_id
                tax_ids_after_fiscal_position = fpos.map_tax(self.tax_ids, self.product_id, self.admissions_id.partner_id) if fpos else self.tax_ids
                self.price_unit = self.product_id.lst_price
            if not pricelist_id:
                raise UserError(
                    _('You have to select a pricelist in the sale form !\n'
                      'Please set one before choosing a product.'))
                
                
    @api.onchange('qty', 'discount', 'price_unit', 'tax_ids')
    def _onchange_qty(self):
        if self.product_id:
            pricelist_id = False
            if self.order_id and self.order_id.pricelist_id:
                pricelist_id = self.order_id.pricelist_id
            else:
                pricelist_id = self.admissions_id.pricelist_id
            if not pricelist_id:
                raise UserError(_('You have to select a pricelist in the sale form !'))
            price = self.price_unit * (1 - (self.discount or 0.0) / 100.0)
            self.price_subtotal = self.price_subtotal_incl = price * self.qty
            if (self.product_id.taxes_id):
                taxes = self.product_id.taxes_id.compute_all(price, pricelist_id.currency_id, self.qty, product=self.product_id, partner=False)
                self.price_subtotal = taxes['total_excluded']
                self.price_subtotal_incl = taxes['total_included']

class Outpatient_Admissions(models.Model):
    _name = 'outpatient.admissions'
    
    name = fields.Char('Name')
    father_name = fields.Char('Father Name')
    age = fields.Char('Age')
    ph_no = fields.Char('Mobile No')
    street = fields.Char()
    street2 = fields.Char()
    zip = fields.Char(change_default=True)
    city = fields.Char()
    state_id = fields.Many2one("res.country.state", string='State')
    country_id = fields.Many2one('res.country', string='Country')
    cnic = fields.Char('CNIC')
    state = fields.Selection(OUTPATIENT_STATES, string='State')
    notice = fields.Char(string='Discount Notice')
    product_id = fields.Many2one('product.product', string='Product')
    price_unit = fields.Float(string='Unit Price')
    qty = fields.Float('Quantity')
    price_subtotal = fields.Float(string='Subtotal w/o Tax')
    price_subtotal_incl = fields.Float(string='Subtotal')
    discount = fields.Float(string='Discount (%)')
    tax_ids_after_fiscal_position = fields.Many2many('account.tax' , string='Taxes')
    lines = fields.One2many('pos.order.line', 'admissions_id', string='Order Lines')
    pricelist_id = fields.Many2one('product.pricelist', string='Pricelist', required=True)
    partner_id = fields.Many2one('res.partner', string='Customer')
    fiscal_position_id = fields.Many2one('account.fiscal.position', string='Fiscal Position')
    invo_id = fields.Many2one('account.invoice', 'Account Invoices')
    
    
    @api.multi
    @api.onchange('partner_id')
    def onchange_part_id(self):
        for rec in self:
            print "eeeeeeeeee", rec.lines.product_id.name
            rec.name = rec.partner_id.name or ' '
            rec.father_name = rec.partner_id.father_name or ''
            rec.age = rec.partner_id.age or ''
            rec.ph_no = rec.partner_id.mobile or ''
            
    
    @api.multi
    def outpatient_invoiced(self):
        invoice_obj = self.env["account.invoice"]
        invoice_line_obj = self.env["account.invoice.line"]
        res = {}
        curr_invoice = {
                    'partner_id': self.partner_id.id,
                    'fiscal_position_id' : self.fiscal_position_id.id,
                }
                 
        invo_id = invoice_obj.create(curr_invoice)
        for outpatient in self.lines:
             curr_invoice_line = {
                 'name': outpatient.product_id.name,
                'product_id': outpatient.product_id.id,
                'price_unit': outpatient.price_unit,
                'account_id': invo_id.account_id.id,
                'invoice_id': invo_id.id,
            }
            
             vals = invoice_line_obj.create(curr_invoice_line)
             res = self.write({'state': 'Invoiced'})
        self.invo_id = invo_id.id
             
             
             
    @api.multi
    def check_invoiced(self):
        return {
            'name': _('Paid Invoices'),
            'view_type': 'form',
            'view_mode': 'tree,form',
            'res_model': 'account.invoice',
            'view_id': False,
            'type': 'ir.actions.act_window',
            'domain': [('id', '=', self.invo_id.id)],
        }
        
        
    
    
             
   

    
    
    