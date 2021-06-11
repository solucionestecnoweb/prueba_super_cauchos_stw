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

class PurchaseOrderExtend(models.Model):
	_inherit = "purchase.order"

	assigned_to_id = fields.Many2one(comodel_name='res.partner', string='Assigned to')
	approve_by_id = fields.Many2one(comodel_name='res.partner', string='Approve by')
	date_end = fields.Date(string='End Date')
	department_id = fields.Many2one(comodel_name='hr.department', string='Department')
	priority = fields.Selection(string='Priority', selection=[('very_low', 'Very Low'), ('low', 'Low'), ('meddium', 'Meddium'), ('high', 'High')], default="low")
	
	def _date_now_purchase(self):
		xdate = datetime.now() - timedelta(hours=4)
		return xdate
