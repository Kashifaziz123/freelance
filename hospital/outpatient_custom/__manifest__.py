

{
    'name': 'Outpatient Management',
    'version': '1.0',
    'author': "Habib Awan, Megaline",
    'category': 'Generic Modules/Medical',
    'summary': 'Odoo Hospital Management Solutions',
    'depends': ['base','account','oehealth'],
    
    "data": [
           'view/outpatient.xml',
           'view/oeh_invoice_report.xml',
           'view/report_oeh_invoice.xml',
		   'view/report_oeh_invoice_corporate.xml',
		   'view/report_oeh_invoice_mri.xml',
        ],
}