from odoo import api, fields, models


class ApprovalsCategoryConciliationExtend(models.Model):
    _inherit = 'approval.category'

    has_conciliation = fields.Selection(string='Conciliation', selection=[('required', 'Required'), ('optional', 'Optional'), ('no', 'None')], default='no')


class ApprovalsRequestConciliationExtend(models.Model):
    _inherit = 'approval.request'

    conciliation_id = fields.Many2one(comodel_name='account.payment', string='Payment')
    has_conciliation = fields.Selection(related="category_id.has_conciliation")

    def action_approve(self):
        #res = super(ApprovalsRequestConciliationExtend, self).action_approve()
        for ap in self:
            if ap.conciliation_id.id:
                order_obj = ap.env['account.payment'].search([('id', '=', ap.conciliation_id.id)])
                order_obj.write({'is_approved': True})
        return super(ApprovalsRequestConciliationExtend, self).action_approve()

    def action_refuse(self):
        for ap in self:
            if ap.conciliation_id.id:
                order_obj = ap.env['account.payment'].search([('id', '=', ap.conciliation_id.id)])
                order_obj.write({'is_approved': False, 'is_rejected': True})
        return super(ApprovalsRequestConciliationExtend, self).action_refuse()

    def action_cancel(self):
        for ap in self:
            if ap.conciliation_id.id:
                order_obj = ap.env['account.payment'].search([('id', '=', ap.conciliation_id.id)])
                order_obj.write({'is_approved': False, 'is_rejected': True})
        return super(ApprovalsRequestConciliationExtend, self).action_refuse()
