import json
from datetime import datetime, timedelta
import base64
from io import StringIO
from odoo import api, fields, models, _
from datetime import date
from odoo.tools.float_utils import float_round
from odoo.exceptions import Warning
import time

class Internal(models.Model):
    _inherit ='account.payment'

    transfer_to_id = fields.Many2one ('res.company', string='Company to transfer')
    destination_journal_id = fields.Many2one('account.journal', domain="[('company_id','=',transfer_to_id)]")
    