from odoo import api, fields, models


class PurchaseAccountMove(models.Model):
    _inherit = 'account.move'

    pay_order_id = fields.Many2one(comodel_name='purchase.pay.order', string='Pay Order')