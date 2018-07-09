from odoo import api, models

class ParticularReport(models.AbstractModel):
    _name = 'report.abbex_valued_stock_move.report_deliveryslip_custom'
    
    @api.model
    def render_html(self, docids, data=None):
        unit_prices = {}
        report_obj = self.env['report']
        report = report_obj._get_report_from_name('abbex_valued_stock_move.report_deliveryslip_custom')
        stock_pickings = self.env['stock.picking'].browse(docids)
        for stock_picking in stock_pickings:
            product_price = self.get_product_price(stock_picking)
            if product_price:
                unit_prices.update({stock_picking.id : product_price})
            else:
                unit_prices.update({stock_picking.id : False})
        docargs = {
            'data' : stock_pickings,
            'unit_prices' : unit_prices,
            'doc_ids': docids,
            'doc_model': report.model,
            'docs': self,
        }
        return report_obj.render('abbex_valued_stock_move.report_deliveryslip_custom', docargs)
    
    def get_product_price(self, stock_picking):
        unit_prices = {}
        order_lines = self.env['sale.order'].search([('name','=',stock_picking.origin)]).order_line
        if order_lines:
            for order_line in order_lines:
                if order_line.price_unit:
                    unit_prices.update({order_line.product_id.id : {'price':order_line.price_unit,'tax':order_line.tax_id.amount,'discount':order_line.discount,}})
        else:
            unit_prices.update({stock_picking.id : False})
        return unit_prices
            