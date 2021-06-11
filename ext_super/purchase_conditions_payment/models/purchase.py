from odoo import api, fields, models
from datetime import datetime, date, timedelta
import base64
from odoo.exceptions import UserError, ValidationError
from odoo.tools.float_utils import float_round
from odoo.exceptions import Warning

class PurchaseConditionsPayment(models.Model):
    _inherit = 'purchase.order'

    pay_order_id = fields.Many2one(comodel_name='purchase.pay.order', string='Pay Order')

class PurchaseAccountMove(models.Model):
    _inherit = 'account.move'

    pay_order_id = fields.Many2one(comodel_name='purchase.pay.order', string='Pay Order')

class ResPartnerConditionsPayment(models.Model):
    _inherit = 'res.partner'

    trading_conditions = fields.Html(string='Trading Conditions')
