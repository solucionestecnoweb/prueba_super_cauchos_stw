# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from datetime import datetime
from odoo.exceptions import UserError, ValidationError, except_orm, Warning


class FleetVehicleLogAssigmentControl(models.Model):
    _inherit = 'fleet.vehicle.log.assignment.control'

    delivery_date = fields.Date('Fecha entrega')

    @api.onchange('vehicle_id','date_ini','date_end')
    def _onchange_date_to(self):
        if self.vehicle_id:
            if self.driver_id:
                assig = self.env['fleet.vehicle.log.assignment.control'].search([])
                a = [a.id for a in assig.vehicle_id]
                if self.vehicle_id.id in a:
                    for item in assig:
                        if item.date_ini and item.date_end and self.date_ini and self.date_end:
                            if item.status != 'done' and self.date_end <= item.date_end:
                                raise Warning(
                                    "El Vehiculo seleccionado '{}' ya está ocupado en ese rango de fechas.\n Seleccione otra fecha o otro vehiculo en la asignación.".format(
                                        ''.join(self.vehicle_id.mapped('name'))))
    def get_user_active(self):
        return self.env['res.users'].browse(self._uid).name