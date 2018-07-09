{
    'name': 'daily Invoice Report',
    'summary': 'PDF report template for valued invoicing notes',
    'description': 'Print Invoice Report on Specific Dates filter',
    'author': 'Habaib Awan',
    'depends' : ['stock','account','oehealth'],
    'data' : [
            'security/ir.model.access.csv',
            'reports/stock_picking_report.xml',
            'reports/stock_picking_template.xml',
            'wizard/wizard_view.xml',
              ]
}