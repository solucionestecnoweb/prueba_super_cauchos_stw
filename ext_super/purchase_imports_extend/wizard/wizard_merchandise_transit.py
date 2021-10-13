from datetime import datetime, timedelta
from itertools import product
from odoo.tools.misc import DEFAULT_SERVER_DATE_FORMAT

from odoo import models, fields, api, _, tools
from odoo.exceptions import UserError
import openerp.addons.decimal_precision as dp
import logging

import io
from io import BytesIO

import xlsxwriter
import shutil
import base64
import csv
import xlwt

_logger = logging.getLogger(__name__)

class MerchandiseTransitTemp(models.Model):
    _name = 'temp.merchandise.transit'

    compra_id = fields.Many2one(comodel_name='purchase.order')
    cantidad = fields.Float()
    unidades_id = fields.Many2one(comodel_name='uom.uom')
    pr = fields.Char()
    producto_id = fields.Many2one(comodel_name='product.product')
    modelo = fields.Char()
    precio = fields.Float()
    pronto_pago = fields.Char()
    super_promo = fields.Char()
    c_apartada = fields.Float()
    c_disponible = fields.Float()
    moneda_id = fields.Many2one(comodel_name='res.currency')
    fecha_planeada = fields.Datetime()

    @api.constrains('cantidad','unidades_id','pr','producto_id','modelo','precio','pronto_pago','super_promo','fecha_planeada')
    def constrains_factura(self):
        self.actualizar_datos()

    def actualizar_datos(self):
        purchases = self.env['purchase.order.line'].sudo().search([
            ('order_id', '=', self.compra_id.id),
        ])
        purchases.product_qty = self.cantidad
        purchases.product_uom = self.unidades_id.id
        purchases.pr = self.pr
        purchases.product_id = self.producto_id.id
        purchases.modelo = self.modelo
        purchases.price_unit = self.precio
        purchases.pronto_pago = self.pronto_pago
        purchases.super_promo = self.super_promo
        purchases.date_planned = self.fecha_planeada
    
class WizardMerchandiseTransit(models.TransientModel):
    _name = 'wizard.merchandise.transit'

    date_from = fields.Date(string='Date From', default=lambda *a:datetime.now().strftime('%Y-%m-%d'))
    date_to = fields.Date('Date To', default=lambda *a:(datetime.now() + timedelta(days=(1))).strftime('%Y-%m-%d'))
    date_now = fields.Datetime(string='Date Now', default=lambda *a:datetime.now())
    
    state = fields.Selection([('choose', 'choose'), ('get', 'get')],default='choose')
    report = fields.Binary('Prepared file', filters='.xls', readonly=True)
    name = fields.Char('File Name', size=60)
    company_id = fields.Many2one('res.company','Company',default=lambda self: self.env.user.company_id.id)

    
    def get_merchandise(self):
        xfind = self.env['purchase.order.line'].sudo().search([
            ('date_order', '>=', self.date_from),
            ('date_order', '<=', self.date_to),
            ('state', 'in', ('draft', 'sent', 'purchase')),
            ('qty_received', '=', 0),
            ('company_id.imports_company', '=', True)
        ])
        return xfind

    def get_data(self):
        t = self.env['temp.merchandise.transit']
        t.search([]).unlink()
        for item in self.get_merchandise():
            values = {
                'compra_id': item.order_id.id,
                'cantidad': item.product_qty,
                'unidades_id': item.product_uom.id,
                'pr': item.pr,
                'producto_id': item.product_id.id,
                'modelo': item.product_id.modelo,
                'precio': item.price_unit,
                'pronto_pago': item.pronto_pago,
                'super_promo': item.super_promo,
                'c_apartada': item.apart_to_seller,
                'c_disponible': item.apart_qty_available,
                'moneda_id': item.currency_id.id,
                'fecha_planeada': item.date_planned,
            }
            t.create(values)
        self.line_ids = t.search([])
        
    def show_list(self):
        self.get_data()
        return {
            "type": "ir.actions.act_window",
            "res_model": "temp.merchandise.transit",
            "views": [[self.env.ref('purchase_imports_extend.imports_merchandise_transit_view_tree').id, "tree"],[False, "form"]],
            "name": "Mercancía en Tránsito",
        }