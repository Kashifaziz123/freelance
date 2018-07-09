# -*- coding: utf-8 -*-
##########################################################################
#
#	Copyright (c) 2015-Present Webkul Software Pvt. Ltd. (<https://webkul.com/>)
#   See LICENSE file for full copyright and licensing details.
#   "License URL : <https://store.webkul.com/license.html/>"
#
##########################################################################

from odoo import api, fields, models, _

class SaleConfigSettings(models.TransientModel):
    _inherit = 'sale.config.settings'

    group_order_global_discount = fields.Boolean("A global discount on sale order",
        implied_group='discount_sale_order.group_order_global_discount',
        help="""Allows to give a global discount on sale order. """)
    global_discount_tax = fields.Selection([
        (0, 'Apply global discount on untaxed amount'),
        (1, 'Apply global discount on tax added amount'),
        ], "Global Discount Calculation",
        help='Global disount calculation will be (0 : Global discount will be applied before applying tax, \
            1 : Global disount will be applied after applying tax)')
    group_discount_sale_line = fields.Boolean("Apply discount on sale order line",
        implied_group='discount_sale_order.group_discount_sale_line',
        help="""Allows to give discount on sale order line. """)

    @api.multi
    def set_default_fields(self):
        ir_values_obj = self.env['ir.values']
        ir_values_obj.sudo().set_default('sale.config.settings', 'global_discount_tax',
                                         self.global_discount_tax or 0)

    @api.model
    def get_default_fields(self, fields):
        ir_values_obj = self.env['ir.values']
        global_discount_tax = ir_values_obj.sudo().get_default(
            'sale.config.settings', 'global_discount_tax')

        return {
            'global_discount_tax': global_discount_tax,
        }
