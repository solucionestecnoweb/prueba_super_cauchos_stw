# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.
import json
from datetime import datetime, timedelta
import base64
from io import StringIO
from odoo import api, fields, models
from datetime import date
from odoo.tools.float_utils import float_round
from odoo.exceptions import Warning

import time

class PurchaseOrderImports(models.Model):
	_inherit = "purchase.order"

	cycle_brand = fields.Char(string='Brand')
	invoice_number = fields.Char(string='Proforma')
	cycle_type = fields.Char(string='Type')
	prof_date = fields.Date(string='Proforma Date')
	invoice_id = fields.Many2one(comodel_name='account.move', string='Invoice')
	cont = fields.Char(string='CONT')
	bl_date = fields.Date(string='BL Date')
	transc = fields.Char(string='Transc')
	acumulated = fields.Float(string='Acumulated')
	eta = fields.Char(string='ETA')
	traffic = fields.Float(string='Traffic')
	nac = fields.Float(string='NAC')
	total = fields.Float(string='Total')

	load_plan = fields.Binary(string='Load Plan')
	package_list = fields.Binary(string='Package List')
	landed_date = fields.Date(string='Landed Date')
	merchandise_available_load = fields.Binary(string='Merchandise Available for Load')

	aduana_agency_id = fields.Many2one(comodel_name='purchase.order.imports.aduana', string='Aduana Agency')
	aduana_costs = fields.Float(string='Aduana Estimated Costs')
	aduana_date = fields.Date(string='Aduana Estimated Date')
	aduana_doc = fields.Binary(string='Attach Document')

	aduana_payment_ids = fields.One2many(comodel_name='purchase.order.imports.aduana.payment', inverse_name='purchase_order_id', string=' Aduana Payment')
	
class PurchaseOrderLineImports(models.Model):
	_inherit = "purchase.order.line"

	pr = fields.Char(string='PR')
	pronto_pago = fields.Char(string='Pronto Pago Promotion')
	super_promo = fields.Char(string='Super Promo Promotion')
	apart_to_seller = fields.Integer(string='Set Apart to Seller')
	apart_qty_available = fields.Integer(string='Set Apart Quantity Available')

class PurchaseOrderImportsAduana(models.Model):
	_name = "purchase.order.imports.aduana"
	
	name = fields.Char(string='Aduana name')
	
class PurchaseOrderImportsAduanaPayment(models.Model):
	_name = "purchase.order.imports.aduana.payment"
	
	payment_date = fields.Date(string='Payment Date')
	payment_concept = fields.Char(string='Payment Concept')
	payment_amount = fields.Float(string='Payment Amount')
	payment_approve = fields.Boolean(string='Approve?')
	payment_doc = fields.Binary(string='Attach Document')
	payment_observation = fields.Text(string='Observation')
	purchase_order_id = fields.Many2one(comodel_name='purchase.order', string='Purchase Order')
	currency_id = fields.Many2one(comodel_name='res.currency', string='Currency', default=lambda self: self.env.user.company_id.currency_id)

class PurchaseOrderImportsShippingInformation(models.Model):
	_name = "purchase.order.imports.shipping"

	policy = fields.Char(string='Policy')
	price_type = fields.Char(string='Price Type')
	freight_type = fields.Char(string='Freight Type')
	expedient_import_number = fields.Char(string='Expedient Import Number')
	
	arrival_date = fields.Date(string='Arrival Date')
	harbor = fields.Char(string='Harbor')
	proforma_number = fields.Char(string='Proforma Number')
	reference = fields.Char(string='Reference')
	doc_reception = fields.Char(string='Document Reception')
	cus_hou_remitance = fields.Char(string='Custom House Remitance')
	dua = fields.Char(string='DUA')
	currency_id = fields.Many2one(comodel_name='res.currency', string='Currency Rate', default=lambda self: self.env.user.company_id.currency_id)
	
	shipping_number = fields.Char(string='Shipping Number')
	shipping_date = fields.Date(string='Shipping Date')
	arrival_shipping_date = fields.Date(string='Estimated Shipping Arrival Date')
	country_id = fields.Many2one(comodel_name='res.country', string='Country')
	shipping_city = fields.Char(string='Shipping City')
	
	vessel_name = fields.Char(string='Name')
	vessel_containers = fields.Integer(string='Containers')
	origin_vessel = fields.Char(string='Origin Vessel')
	transfer_vessel = fields.Char(string='Transfer Vessel')

# class PurchaseOrderImports(models.Model):
# 	_name = "purchase.order.imports"

# 	partner_id = fields.Many2one(comodel_name='res.partner', string='Supplier')
# 	import_model = fields.Char(string='Model')
# 	import_brand = fields.Char(string='Brand')
# 	invoice_number = fields.Char(string='Invoice Number / Proforma')
# 	import_qty = fields.Integer(string='Quantity')
# 	percent_30 = fields.Float(string='30%')
# 	percent_70 = fields.Float(string='70%')
# 	percent_100 = fields.Float(string='100%')
# 	import_amount = fields.Float(string='Amount')
# 	payment_date = fields.Date(string='Payment Date')
# 	etd = fields.Char(string='ETD')
# 	eta = fields.Char(string='ETA')
# 	status = fields.Char(string='Status')
	
# class PurchaseOrderImportsContainers(models.Model):
# 	_name = "purchase.order.imports.containers"

# 	nbl_container = fields.Char(string='N BL / Container')
# 	invoice_number = fields.Char(string='Invoice Number')
# 	container_type = fields.Char(string='Type')
# 	container_brand = fields.Char(string='Brand')
# 	cont = fields.Char(string='CONT')
# 	tires = fields.Char(string='Tires')
# 	agency = fields.Char(string='Agency')
# 	shipping_company = fields.Char(string='Shipping Company')
# 	eta_ven = fields.Char(string='ETA/VEN')
# 	harbor = fields.Char(string='Harbor')
# 	warehouse = fields.Char(string='Warehouse')
# 	status_w = fields.Char(string='Status')
# 	vessel = fields.Char(string='Vessel')
# 	status_v = fields.Char(string='Status')
