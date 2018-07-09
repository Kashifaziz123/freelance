###############################################################################
#
#   Copyright (C) 2004-today OpenERP SA (<http://www.openerp.com>)
#   Copyright (C) 2016-today Geminate Consultancy Services (<http://geminatecs.com>).
#
#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU Affero General Public License as
#   published by the Free Software Foundation, either version 3 of the
#   License, or (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#   GNU Affero General Public License for more details.
#
#   You should have received a copy of the GNU Affero General Public License
#   along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
###############################################################################

from odoo import api, models, fields, _
from odoo.exceptions import Warning


class PackOperationLot(models.Model):
    _inherit = 'stock.pack.operation.lot'

    expiry_date = fields.Datetime(string="Expiry Date")
    alert_date = fields.Datetime(string="Alert Date")
    
    @api.onchange('lot_id')
    def onchange_lot_id(self):
        for record in self:
            record.expiry_date = record.lot_id.life_date
            record.alert_date = record.lot_id.alert_date
            
    @api.model
    def create(self, vals):
        res = super(PackOperationLot, self).create(vals)
        lot_id = self.env['stock.production.lot'].create({'product_id':res.operation_id.product_id.id})
        res.lot_id = lot_id.id
        lot_id.write({'life_date':res.expiry_date,
        'alert_date':res.alert_date})
        return res
    
    @api.multi
    def write(self, vals):
        if vals.get('expiry_date'):
            self.lot_id.update({'life_date':vals.get('expiry_date')})
        if vals.get('alert_date'):
            self.lot_id.update({'alert_date':vals.get('alert_date')})
        return super(PackOperationLot, self).write(vals)

