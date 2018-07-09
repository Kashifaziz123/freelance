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

class PosOrder(models.Model):
    _inherit = 'pos.order'

    indent_no = fields.Char('Indent No')
    inpatient_id = fields.Many2one('oeh.medical.inpatient', 'Inpatient Admissions')

    @api.model
    def _order_fields(self, ui_order):
        res = super(PosOrder, self)._order_fields(ui_order=ui_order)
        res.update({'indent_no':ui_order.get('indent_no', False),
                    'inpatient_id':ui_order.get('inpatient_id', False),
                    })
        return res

    @api.model
    def create(self, vals):
        if vals.get('indent_no') and len(str(vals.get('indent_no'))) < 4:
            raise Warning(_('Indent number length must be five digits.'))
        return super(PosOrder, self).create(vals)

    @api.multi
    def write(self, vals):
        if vals.get('indent_no') and len(str(vals.get('indent_no'))) < 4:
            raise Warning(_('Indent number length must be five digits.'))
        return super(PosOrder, self).write(vals)

#     _sql_constraints = [
#             ('pos_indent_no_unique','unique(indent_no)','Indent Number must be unique!'),
#       ]

    def _prepare_invoice(self):
        res = super(PosOrder, self)._prepare_invoice()
        if res:
            res.update({'cust_indent_no':self.indent_no,
                        'inpatient_id':self.inpatient_id.id,
                        'patient':self.inpatient_id.patient.id})
        return res