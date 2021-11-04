from odoo import api, fields, models


class ResPartnerConditionsPayment(models.Model):
    _inherit = 'res.partner'

    trading_conditions = fields.Html(string='Trading Conditions')
    payment_ids = fields.One2many(comodel_name='res.supplier.payment.plan', inverse_name='name', string=' Supplier Payment Plan')