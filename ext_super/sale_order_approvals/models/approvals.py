from odoo import api, fields, models


class ApprovalsCategorySaleExtend(models.Model):
    _inherit = 'approval.category'

    has_sale_order = fields.Selection(string='Sale Order', selection=[('required', 'Required'), ('optional', 'Optional'), ('no', 'None')], default='no')

class ApprovalsRequestSaleExtend(models.Model):
    _inherit = 'approval.request'

    sale_order_id = fields.Many2one(comodel_name='sale.order', string='Sale Order')
    has_sale_order = fields.Selection(related="category_id.has_sale_order")

    # @api.depends('approver_ids.status')
    # def _compute_request_status(self):
    #     res = super(ApprovalsRequestSaleExtend, self)._compute_request_status()
    #     for ap in self:
    #         if ap.request_status == 'approved':
    #             order_obj = ap.env['sale.order'].search([('id', '=', ap.sale_order_id)])
    #             if order_obj:
    #                 order_obj.write({'is_approved', True})
    #     return res

    def action_approve(self):
        res = super(ApprovalsRequestSaleExtend, self).action_approve()
        for ap in self:
            if ap.sale_order_id.id:
                order_obj = ap.env['sale.order'].search([('id', '=', ap.sale_order_id.id)])
                order_obj.write({'is_approved': True})
        return res

    def action_refuse(self):
        res = super(ApprovalsRequestSaleExtend, self).action_refuse()
        for ap in self:
            if ap.sale_order_id.id:
                order_obj = ap.env['sale.order'].search([('id', '=', ap.sale_order_id.id)])
                order_obj.write({'is_approved': False, 'is_rejected': True})
        return res

    def action_cancel(self):
        res = super(ApprovalsRequestSaleExtend, self).action_cancel()
        for ap in self:
            if ap.sale_order_id.id:
                order_obj = ap.env['sale.order'].search([('id', '=', ap.sale_order_id.id)])
                order_obj.write({'is_approved': False, 'is_rejected': True})
        return res