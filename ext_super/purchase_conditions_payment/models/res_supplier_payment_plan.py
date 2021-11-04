from odoo import api, fields, models


class SupplierPaymentPla(models.Model):
    _name = 'res.supplier.payment.plan'

    name = fields.Many2one(comodel_name='res.partner', string='Supplier')
    date_start = fields.Date(string='Date', default=fields.Date.today())
    qty = fields.Float(string='Qty')
    description = fields.Text(string='Description')
    group = fields.Char(string='Group')
    filler = fields.Float(string='Filler')
    currency_id = fields.Many2one(comodel_name='res.currency', string='Currency',
                                  default=lambda self: self.env.user.company_id.currency_id)
    cost = fields.Float(string='Cost')
    amount = fields.Float(string='Amount')
    crossing = fields.Char(string='Crossing')
    purchase_id = fields.Many2one(comodel_name='purchase.order', string='Purchase order')
    amount_payable = fields.Monetary(string='Amount Payable', related='purchase_id.amount_total')
    payment = fields.Float(string='Payment')
    status_cxp = fields.Selection(string='Status CXP',
                                  selection=[('to_pay', 'To Pay'), ('paid', 'Paid'), ('paid_crossing', 'Paid Crossing'),
                                             ('crossing', 'Crossing'), ('payment', 'Payment'),
                                             ('crossing_payable', 'Crossing Payable')], default='to_pay')
    end_date = fields.Date(string='End Date')
