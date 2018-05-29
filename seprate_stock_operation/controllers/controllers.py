# -*- coding: utf-8 -*-
from odoo import http

# class SeprateStockOperation(http.Controller):
#     @http.route('/seprate_stock_operation/seprate_stock_operation/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/seprate_stock_operation/seprate_stock_operation/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('seprate_stock_operation.listing', {
#             'root': '/seprate_stock_operation/seprate_stock_operation',
#             'objects': http.request.env['seprate_stock_operation.seprate_stock_operation'].search([]),
#         })

#     @http.route('/seprate_stock_operation/seprate_stock_operation/objects/<model("seprate_stock_operation.seprate_stock_operation"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('seprate_stock_operation.object', {
#             'object': obj
#         })