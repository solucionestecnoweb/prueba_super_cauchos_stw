from odoo import api, fields, models, _
from datetime import datetime, date, timedelta
import base64
from odoo.exceptions import UserError, ValidationError, Warning
from odoo.tools.float_utils import float_round


class AccountPaymentApproval(models.Model):
    _inherit = 'account.payment'

    is_approved = fields.Boolean(default=False, compute='_is_approved')
    state = fields.Selection(selection_add=[('to_approve', 'To be Approved'), ('approved', 'Approved'), ('refused', 'Refused')])
    
    def approved_post(self):
        if self.is_approved:
            self.action_draft()
            self.post()
        else:
            raise ValidationError(_("Cannot confirm until an approval request is approved for this invoice."))

    def _is_approved(self):
        for item in self:
            xfind = item.env['approval.request'].search([('conciliation_id', '=', item.id)])
            is_company =  item.env['res.company'].search([('partner_id', '=', item.partner_id.id)])
            if len(xfind) > 0 and item.state in ('draft'):
                item.state = 'to_approve'

            if item.state in ('to_approve'):
                status = xfind.request_status
                if len(xfind) > 0:
                    if status == 'approved':
                        item.state = 'approved'
                        item.is_approved = True
                    elif status == 'refused':
                        item.state = 'refused'
                        item.is_approved = False
                    else:
                        item.is_approved = False
            elif item.state == 'approved':
                item.is_approved = True
            elif item.state == 'refused':
                item.is_approved = False
            elif len(is_company) > 0:
                item.is_approved = True
            elif len(item.invoice_ids) > 0:
                for line in item.invoice_ids:
                    if line.payment_condition_id.name in ('contado', 'Contado', 'CONTADO'):
                        item.is_approved = True
                    else:
                        item.is_approved = False
            else:
                item.is_approved = False
            
    def approvals_request_conciliation(self):
        xfind = self.env['approval.request'].search([('conciliation_id', '=', self.id), ('request_status', 'not in', ['cancel'])])
        if len(xfind) == 0:
            approval = self.env['approval.category'].search([
                ('has_conciliation', '=', 'required')
            ], limit=1)
            if len(approval) > 0:
                values = {
                    'name': approval.name,
                    'category_id': approval.id,
                    'date': datetime.now(),
                    'request_owner_id': self.env.user.id,
                    'amount': self.amount,
                    'conciliation_id': self.id,
                    'request_status': 'pending'
                }
                t = self.env['approval.request'].create(values)
                for item in approval.user_ids:
                    t.approver_ids += self.env['approval.approver'].new({
                        'user_id': item.id,
                        'request_id': t.id,
                        'status': 'new'
                    })
                t.action_confirm()
                self.state = 'to_approve'
            else:
                raise ValidationError(_("There is no approval category for this type record. Go to Approvals/Config/Approval type."))
        else:
            raise ValidationError(_("There is an approval request ongoing for this invoice."))