# -*- coding: utf-8 -*-
##########################################################################
#
#	Copyright (c) 2015-Present Webkul Software Pvt. Ltd. (<https://webkul.com/>)
#   See LICENSE file for full copyright and licensing details.
#   "License URL : <https://store.webkul.com/license.html/>"
#
##########################################################################

from odoo import api, fields, models, _
import odoo.addons.decimal_precision as dp

class SaleOrder(models.Model):
	_inherit = "sale.order"

	@api.model
	def _wk_discount_po_settings(self):
		configModel = self.env['sale.config.settings']
		discntSettingObj = configModel.create({'group_discount_sale_line':True})
		discntSettingObj.execute()
		globalDiscountSettingObj = configModel.create({'group_order_global_discount':True})
		globalDiscountSettingObj.execute()
		return True

	@api.depends('order_line.price_total', 'global_order_discount', 'global_discount_type')
	def _amount_all(self):
		super(SaleOrder, self)._amount_all()
		for order in self:
			amount_untaxed = amount_tax = 0.0
			total_discount = 0.0
			for line in order.order_line:
				amount_untaxed += line.price_subtotal
				if line.discount_type == 'fixed':
					total_discount += line.discount
				else:
					total_discount += line.product_qty*(line.price_unit - line.price_reduce)
				if order.company_id.tax_calculation_rounding_method == 'round_globally':
					quantity = 1.0
					if line.discount_type == 'fixed':
						price = line.price_unit * line.product_qty - (line.discount or 0.0)
					else:
						price = line.price_unit * (1 - (line.discount or 0.0) / 100.0)
						quantity = line.product_qty
					taxes = line.tax_id.compute_all(
						price, line.order_id.currency_id, quantity, product=line.product_id, partner=line.order_id.partner_id)
					amount_tax += sum(t.get('amount', 0.0) for t in taxes.get('taxes', []))
				else:
					amount_tax += line.price_tax
			ir_values_obj = self.env['ir.values']
			discTax = ir_values_obj.sudo().get_default(
				'sale.config.settings', 'global_discount_tax')
			if discTax == 0:
				total_amount = amount_untaxed
			else:
				total_amount = amount_untaxed + amount_tax
			if order.global_discount_type == 'percent':
				beforeGlobal = total_amount
				total_amount = total_amount * (1 - (order.global_order_discount or 0.0)/100)
				total_discount += beforeGlobal - total_amount
			else:
				total_amount = total_amount - (order.global_order_discount or 0.0)
				total_discount += order.global_order_discount
			if discTax == 0:
				total_amount = total_amount + amount_tax
			order.update({
				'amount_untaxed': order.currency_id.round(amount_untaxed),
				'amount_tax': order.currency_id.round(amount_tax),
				'amount_total': total_amount,
				'total_discount': total_discount,
			})

	total_discount = fields.Monetary(string='Total Discount', store=True, readonly=True, compute='_amount_all', track_visibility='always')
	global_discount_type = fields.Selection([
		('fixed', 'Fixed'),
		('percent', 'Percent')
		], string="Discount Type",)
	global_order_discount = fields.Float(string='Global Discount', store=True,  track_visibility='always')

class SaleOrderLine(models.Model):
	_inherit = "sale.order.line"

	@api.depends('price_unit', 'discount_type', 'discount')
	def _get_price_reduce(self):
		for line in self:
			if line.discount_type == 'fixed':
				price_reduce = line.price_unit * line.product_qty - line.discount
				line.price_reduce = price_reduce/line.product_qty
			else:
				line.price_reduce = line.price_unit * (1.0 - line.discount / 100.0)


	price_reduce = fields.Monetary(compute='_get_price_reduce', string='Price Reduce', readonly=True, store=True)
	discount = fields.Float(string='Discount', digits=dp.get_precision('Discount'), default=0.0)
	discount_type = fields.Selection([
		('fixed', 'Fixed'),
		('percent', 'Percent')
		], string="Discount Type",)

	@api.depends('product_qty', 'price_unit', 'taxes_id', 'discount', 'discount_type')
	def _compute_amount(self):
		super(SaleOrderLine, self)._compute_amount()
		for line in self:
			quantity = 1.0
			if line.discount_type == 'fixed':
				price = line.price_unit * line.product_qty - (line.discount or 0.0)
			else:
				price = line.price_unit * (1 - (line.discount or 0.0) / 100.0)
				quantity = line.product_qty
			taxes = line.taxes_id.compute_all(
				price, line.order_id.currency_id, quantity, product=line.product_id, partner=line.order_id.partner_id)
			line.update({
				'price_tax': taxes['total_included'] - taxes['total_excluded'],
				'price_total': taxes['total_included'],
				'price_subtotal': taxes['total_excluded'],
			})
