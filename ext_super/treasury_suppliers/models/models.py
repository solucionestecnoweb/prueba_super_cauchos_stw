import json
from datetime import datetime, timedelta
import base64
from io import StringIO
from odoo import api, fields, models, _
from datetime import date
from odoo.tools.float_utils import float_round
from odoo.exceptions import Warning
import time
from base64 import encodestring

class Suppliers(models.Model):
    _inherit ='account.payment'

    invoice_ids = fields.Many2many('account.move', 'account_invoice_payment_rel', 'payment_id', 'invoice_id', string="Invoices", copy=False, readonly=True,
                                   help="""Technical field containing the invoice for which the payment has been generated.
                                   This does not especially correspond to the invoices reconciled with the payment,
                                   as it can have been generated first, and reconciled later""")

    def send_email_recipt(self):
        company = self.env.user.company_id
        if self.partner_id.email:
            template = self.env.ref('treasury_suppliers.email_template_oasis_send_email', False)
            attachment_ids = []
            attach = {}

            result_pdf, type = self.env['ir.actions.report']._get_report_from_name('account.action_report_payment_receipt')._render_qweb_pdf(self.id)
            attach['name'] = 'Recibo de Pago.pdf' 
            attach['type'] = 'binary'
            attach['datas'] = encodestring(result_pdf)
           # attach['datas_fname'] = 'Recibo de Pago.pdf' 
            attach['res_model'] = 'mail.compose.message'
            attachment_id = self.env['ir.attachment'].create(attach)
            attachment_ids.append(attachment_id.id)

            mail = template.send_mail(self.id, force_send=True,email_values={'attachment_ids': attachment_ids}) #envia mail
            if mail:
                self.message_post(body=_("Enviado email al Cliente: %s"%self.partner_id.name))
                self.state_dte_partner = 'sent'
                print('Correo Enviado a '+ str(self.partner_id.email))

class InvoicesDisplayName(models.Model):
    _inherit ='account.move'

    def name_get(self):
        result = []
        for record in self:
            if record.type in ('in_invoice', 'in_refund', 'in_receipt'):
                # Only goes in when invoice is suppliers
                result.append((record.id, record.invoice_number_pro))
            elif record.type in ('out_invoice', 'out_refund', 'out_receipt'):
                # Only goes in when invoice is customer
                result.append((record.id, record.invoice_number_cli))
            else:
                result.append((record.id, record.name))
        return result