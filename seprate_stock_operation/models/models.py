# -*- coding: utf-8 -*-

from odoo import models, fields, api


class Inherit_Picking(models.Model):
    _inherit = "stock.picking"

    brand = fields.Many2one('brand.brand')

    @api.onchange('picking_type_id')
    def _picking_type_id(self):
        operation_type = self.env.context.get('operation_type')
        picking_type = self.env['stock.picking.type'].search([('name', 'ilike', operation_type)])
        mlist = []
        for val in picking_type:
            mlist.append(val.id)
        return {'domain': {'picking_type_id': [('id', 'in', mlist)]}}


class brand(models.Model):
    _name = 'brand.brand'

    name = fields.Char('brand')


class InheritProductTemplate(models.Model):
    _inherit = "product.template"

    brand = fields.Many2one('brand.brand')


class StockMove(models.Model):
    _inherit = "stock.move"
    
    @api.onchange('product_id')
    def _productlist_brand(self):
        brand = self.env.context.get('default_brand')
        if brand:
            search_product_templates = self.env['product.template'].search([('brand', '=', brand)])
            mlist = []
            for val in search_product_templates:
                products = self.env['product.product'].search([('product_tmpl_id', '=', val.id)])
                stock=self.env['stock.quant'].search([('product_id','=',products.id),('quantity','>',0)])
                if len(stock)>0:
                    for prod in stock:
                        mlist.append(prod.product_id.id)
            return {'domain': {'product_id': [('id', 'in', mlist)]}}
