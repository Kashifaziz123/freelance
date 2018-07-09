# -*- coding: utf-8 -*-
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

{
    'name': 'Account Invoice And POS Indent No',
    'version': '1.0',
    'category': 'Accounting',
    "license": "AGPL-3", 
    'description': """
       Account Invoice Indent
    """,
    'author': 'Geminate Consultancy Services',
    'website': 'www.geminatecs.com',
    'sequence': 1,
    'depends': ['account','point_of_sale','stock'],
    'qweb': ['static/src/xml/pos_template.xml'],
    'data': [
             'views/account_invoice.xml',
             'views/pos_order_view.xml',
             'views/stock_pack_operation_views.xml',
             'views/point_of_sale_template.xml',
    ],
    'installable': True,
    'auto_install': False,
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: -*-
