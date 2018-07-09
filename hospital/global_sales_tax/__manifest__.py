
{
    'name' : 'Invoices Tax Print',
    'description' : "Company's fields has been added such as sales tax invoices etc ",
    'author' : 'Itech resources',
    'wesbite' : 'www.itechresources.com',
    'depends' : [
                    'account','base','product'
                ],
    'data' :[
                'views/account_invoice_views_custom.xml',
                'views/res_company_custom.xml',
                'views/res_partner_custom.xml',
                'reports/global_sales_tax_menu.xml',
                'reports/report.xml',
            ],
    'installable' : True,
}