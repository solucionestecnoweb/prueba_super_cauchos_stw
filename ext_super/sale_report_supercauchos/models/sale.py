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

class SaleOrderExtend(models.Model):
	_inherit = "sale.order"

	arrive_date = fields.Date(string='Arrive Date')
	payment_condition = fields.Selection(string='Payment Condition', selection=[('cash', 'Cash'), ('credit', 'Credit')])

	def _date_now_purchase(self):
		xdate = datetime.now() - timedelta(hours=4)
		return xdate
