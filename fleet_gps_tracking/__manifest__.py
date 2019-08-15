# -*- coding: utf-8 -*-
{
    'name' : 'Fleet GPS Tracking',
    'version' : '10.2018.06.12.0',
    'author' : 'smttraders',
    'depends' : ['fleet','base'],
    'data' : [
            'views/res_config.xml',
            'views/web_map_templates.xml',
            'views/fleet_view.xml',
            'views/fleet_engine.xml',
            'data/gps_crons.xml',
            'security/ir.model.access.csv',
        ],
'qweb': [
        'static/src/xml/*.xml',
    ],
    'installable' : True,
}