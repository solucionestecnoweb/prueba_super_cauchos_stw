from odoo import api, fields, models


class SaleOrderLogicExtend(models.Model):
    _inherit = 'sale.order'

    seller_id = fields.Many2one(comodel_name='res.partner', string='Seller Name')
    date_start = fields.Date(string='Date Start')
    date_end = fields.Date(string='Date End')
    estimated_date = fields.Date(string='Estimated Date')

    @api.onchange('user_id')
    def _onchange_user_id(self):
        self.seller_id = self.user_id.partner_id.id

