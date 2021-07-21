from odoo import api, fields, models


class ApprovalsCategoryAccountExtend(models.Model):
    _inherit = 'approval.category'

    has_account_move = fields.Selection(string='Invoice', selection=[('required', 'Required'), ('optional', 'Optional'), ('no', 'None')], default='no')

class ApprovalsRequestAccountExtend(models.Model):
    _inherit = 'approval.request'

    account_move_id = fields.Many2one(comodel_name='account.move', string='Invoice')
    has_account_move = fields.Selection(related="category_id.has_account_move")
