from odoo import api, fields, models, _
from datetime import datetime, date, timedelta
import base64
from odoo.exceptions import UserError, ValidationError, Warning
from odoo.tools.float_utils import float_round

class AccountMoveInvoicePayment(models.Model):
    _inherit = 'account.move.line'

    exp_date_today = fields.Date(string='Exp. Date', compute='_compute_delay')
    delay_1_30 = fields.Float(string='1 - 30')
    delay_31_60 = fields.Float(string='31 - 60')
    delay_61_90 = fields.Float(string='61 - 90')
    delay_91_120 = fields.Float(string='91 - 120')
    delay_older = fields.Float(string='Older')
    delay_total = fields.Float(string='Total')

    ### Compute Functions ###
    def _compute_delay(self):
        for item in self:
            item.exp_date_today = fields.Date.today()
            item.delay_1_30 = 0
            item.delay_31_60 = 0
            item.delay_61_90 = 0
            item.delay_91_120 = 0
            item.delay_older = 0
            item.delay_total = 0

            if item.date and item.exp_date_today:
                days = (item.exp_date_today - item.date)
                if days.days >= 1 and days.days <=30:
                    item.delay_1_30 = item.amount_residual
                elif days.days >= 31 and days.days <=60:
                    item.delay_31_60 = item.amount_residual
                elif days.days >= 61 and days.days <=90:
                    item.delay_61_90 = item.amount_residual
                elif days.days >= 91 and days.days <=120:
                    item.delay_91_120 = item.amount_residual
                elif days.days > 120:
                    item.delay_older = item.amount_residual

                item.delay_total = item.delay_1_30 + item.delay_31_60 + item.delay_61_90 + item.delay_91_120 + item.delay_older
