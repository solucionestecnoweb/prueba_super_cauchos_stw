from odoo import api, fields, models


class PurchaseConditionsPayment(models.Model):
    _inherit = 'purchase.order'

    pay_order_id = fields.Many2one(comodel_name='purchase.pay.order', string='Pay Order')
