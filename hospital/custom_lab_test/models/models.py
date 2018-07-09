# -*- coding: utf-8 -*-

from odoo import models, fields, api,_


class InheritProduct(models.Model):
    _inherit = 'product.template'

    is_labtest = fields.Boolean('Is Lab Test')


class InheritLabTestType(models.Model):
    _inherit = 'oeh.medical.labtest.types'

    product_id = fields.Many2one('product.product', 'Product')


class InheritLabTest(models.Model):
    _inherit = 'oeh.medical.lab.test'

    patient = fields.Many2one('oeh.medical.patient', string='Patient', help="Patient Name", required=False,
                              readonly=True, states={'Draft': [('readonly', False)]})
    pathologist = fields.Many2one('oeh.medical.physician', string='Pathologist', help="Pathologist", required=False,
                                  readonly=True, states={'Draft': [('readonly', False)]})
    c_patient = fields.Char(string='Patient Name', help="Enter Patient Name", required=False, readonly=True,
                            states={'Draft': [('readonly', False)]})



class InheritInvoice(models.Model):
    _inherit = 'account.invoice'

    is_labtest_invoice = fields.Boolean('Is Lab Test Invoice')
    is_created = fields.Boolean('Is Created',compute="action_create_labtests",store=True)

    @api.multi
    def action_create_labtests(self):
        for record in self.invoice_line_ids:
            search_labtest_category = self.env['oeh.medical.labtest.types'].search(
                [('product_id', '=', record.product_id.id)])
            if self.op_name:
                p_name = self.op_name
            if self.patient:
                p_name = self.patien
            if search_labtest_category:
                obj = self.env['oeh.medical.lab.test']
                obj.create({'test_type': search_labtest_category.id,
                            'c_patient': p_name})
                self.is_created = True
                test_type_id = obj.create({'test_type': search_labtest_category.id,
                                           'c_patient': p_name})
                test_id = test_type_id.id
                if test_id:
                    self.is_created =True
                    labtest_ids = []
                    criteria_obj = self.env['oeh.medical.labtest.criteria']
                    criteria_obj2 = self.env['oeh.medical.lab.resultcriteria']
                    res = {'value': {
                        'lab_test_criteria': [],
                    }
                    }
                    # Create Invoice line
                    test_type_ids1 = criteria_obj.search([('medical_type_id', '=', search_labtest_category.id)])
                    query = _(
                        "select name, sequence, normal_range, units from oeh_medical_labtest_criteria where medical_type_id=%s") % (
                                str(search_labtest_category.id))
                    self.env.cr.execute(query)
                    vals = self.env.cr.fetchall()
                    if vals:
                        for va in vals:
                            specs = {
                                'name': va[0],
                                'sequence': va[1],
                                'normal_range': va[2],
                                'units': va[3],
                                'medical_lab_test_id': test_id,
                            }
                            labtest_ids += [specs]
                            inv_line_ids = criteria_obj2.create(specs)



class InheritInvoiceLine(models.Model):
    _inherit = 'account.invoice.line'

    @api.onchange('product_id')
    def _onchange_product_id(self):
        if self.invoice_id.is_labtest_invoice:
            search_product_templates = self.env['product.product'].search([('product_tmpl_id.is_labtest', '=', True)])
            mlist = []
            for val in search_product_templates:
                mlist.append(val.id)
            return {'domain': {'product_id': [('id', 'in', mlist)]}}
        else:
            return {'domain': {'product_id': [('id', '>', 0)]}}
