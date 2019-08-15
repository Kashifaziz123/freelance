# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from datetime import datetime, timedelta
from odoo import http
import requests
import logging
_logger = logging.getLogger(__name__)


class map_transient(models.TransientModel):
    _name = 'map.transient'

    location =fields.Char('location')
    imei = fields.Char('imei')

    @api.model
    def default_get(self, fields):
        print('............',fields)
        context = self.env.context.get('default_veh_id')
        record_vehcle= self.env['fleet.vehicle'].search([('id','=',context)])
        res = super(map_transient, self).default_get(fields)
        writeoff_lines = []
        print('............r',record_vehcle.imei)
        res.update({'imei': record_vehcle.imei,

                    })

        return res

class FleetVehicle(models.Model):
    _inherit = 'fleet.vehicle'
    
    imei = fields.Char(string="IMEI")
    is_tracking = fields.Boolean(string="Is Tracking")
    total_engine_hours = fields.Float(compute='_compute_total_engine_hour_counts', string='Total Engine Hours')
    engine_hour_counts = fields.Integer(compute='_compute_engine_hour_counts')
    
    vehicle_latitude = fields.Float('Latitude', digits=(16, 5), compute="_get_vehicle_position")
    vehcile_longitude = fields.Float('Longitude', digits=(16, 5), compute="_get_vehicle_position")
    vehcile_speed = fields.Float('Speed',  digits=(16, 5), compute="_get_vehicle_position")
    location =fields.Char('Location')

    def _get_vehicle_position(self):
        for res in self:
            if res.is_tracking == True:
                first_url = "https://api.afaqy.in/?r=userTrackers/lastUpdate&data=%7b%22apiKey%22:%2213ade3d216c5eb5383e4cf9508165899%22,%22imei%22:%22"
                if res.imei:
                    imei = res.imei
                    data = requests.get(first_url+imei+"%22,%22serverId%22:2%7d").json()
                    if data['message'] == 'error':
                        pass
                    else:
                        location_data = data['data']['lastUpdate']['onLocation']
                        speed_data = data['data']['lastUpdate']
                        res.vehicle_latitude = location_data['lat']
                        res.vehcile_longitude = location_data['lng']
                        res.vehcile_speed = speed_data['onSpeed']

    @api.multi
    def vehicle_location_on_map(self):
        ir_model_data = self.env['ir.model.data']
        try:
           view_id = ir_model_data.get_object_reference('fleet_gps_tracking', 'view_fleet_vehicle_map')[1]
        except ValueError:
            view_id = False
        return {
            'name': _('Map'),
            'type': 'ir.actions.act_window',
            'domain': [('id', 'in', [self.id])],
            'view_type': 'form',
            'view_mode': 'map',
            'res_model': 'fleet.vehicle',
            'view_id': False,
            'views': [(view_id, 'map')],
            'target': 'current',
            'context': self._context,
        }



    def _get_odometer(self):
        res = super(FleetVehicle, self)._get_odometer()
        FleetVehicalOdometer = self.env['fleet.vehicle.odometer']
        for record in self:
            odoometers = 0.0
            vehicle_odometer = FleetVehicalOdometer.search([('vehicle_id', '=', record.id)])
            if vehicle_odometer:
                for rec in vehicle_odometer:
                    odoometers += rec.value
            record.odometer = odoometers
        return res

    @api.one
    def _compute_total_engine_hour_counts(self):
        hours = 0.0
        tot_engine_hours = self.env["fleet.vehicle.engine"].search([('vehicle_id', '=', self.id)])
        if tot_engine_hours:
            for rec in tot_engine_hours:
                hours += rec.engine_hours
        self.total_engine_hours = hours

    @api.one
    def _compute_engine_hour_counts(self):
        tot_engine_hours = self.env["fleet.vehicle.engine"].search_count([('vehicle_id', '=', self.id)])
        self.engine_hour_counts = tot_engine_hours

    @api.multi
    def total_engine_hours_afqy(self):
        documents_obj = self.env["fleet.vehicle.engine"].search([('vehicle_id', '=', self.id)])
        hours_ids_list = [hour.id for hour in documents_obj]
        ir_model_data = self.env['ir.model.data']
        try:
           tree_id = ir_model_data.get_object_reference('fleet_gps_tracking', 'view_fleet_gps_engine_hours')[1]
        except ValueError:
            view_id = False
        return {
            'name': _('Engine Hours'),
            'type': 'ir.actions.act_window',
            'domain': [('id', 'in', hours_ids_list)],
            'view_type': 'form',
            'view_mode': 'tree',
            'res_model': 'fleet.vehicle.engine',
            'view_id': False,
            'views': [(tree_id, 'tree')],
            'target': 'current',
            'context': self._context,
        }

    @api.model
    def action_to_get_odometer_engine_afaqy(self):
        fleets = self.search([])
        for res in fleets:
            today = datetime.now() - timedelta(hours = 24)
            last_time = today.strftime('%Y-%m-%d %H:%M:%S')
            today_now = datetime.now()
            now_date = today_now.strftime('%Y-%m-%d %H:%M:%S')
            if res.is_tracking == True:
                first_url = "https://api.afaqy.in/?r=userTrackers/lastUpdate&data=%7b%22apiKey%22:%2213ade3d216c5eb5383e4cf9508165899%22,%22imei%22:%22"
                if res.imei:
                    imei = res.imei
                    get_dates = "%22dateFrom%22:%22"+last_time+"%22,%22dateTo%22:%22"+now_date+"%22,"
                    data = requests.get(first_url+imei+"%22,"+str(get_dates)+"%22serverId%22:2%7d").json()
                    if data['message'] == 'error':
                        pass
                    else:
                        odometer_data = data['data']
                        if odometer_data['odometer'] > 0:
                            self.env['fleet.vehicle.odometer'].create({
                                    'vehicle_id': res.id,
                                    'value': odometer_data['odometer'],
                                    'unit': 'kilometers',
                                })
                        if odometer_data['engineHours'] > 0:
                            self.env['fleet.vehicle.engine'].create({
                                    'vehicle_id': res.id,
                                    'engine_hours': odometer_data['engineHours'],
                                    'unit': 'h',
                                })
    
class FleetVehicleEngine(models.Model):
    _name = 'fleet.vehicle.engine'
    _order = 'date'
    _description = 'Engine Hours History'
    
    vehicle_id = fields.Many2one('fleet.vehicle', 'Vehicle')
    date = fields.Date(default=datetime.today())
    engine_hours = fields.Float('Engine Hours')
    unit = fields.Selection([('h','H')], default='h')

