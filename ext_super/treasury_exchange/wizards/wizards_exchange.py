from datetime import datetime, timedelta
from odoo.tools.misc import DEFAULT_SERVER_DATE_FORMAT

from odoo import models, fields, api, _, tools
from odoo.exceptions import UserError
import logging

import io
from io import BytesIO

import xlsxwriter
import shutil
import base64
import csv
import xlwt

_logger = logging.getLogger(__name__)

class Exchange(models.TransientModel):
    _name = "transaction.exchange"

    date_from = fields.Date(string='Date From', default=lambda *a:datetime.now().strftime('%Y-%m-%d'))
    date_to = fields.Date('Date To', default=lambda *a:(datetime.now() + timedelta(days=(1))).strftime('%Y-%m-%d'))
    date_now = fields.Datetime(string='Date Now', default=lambda *a:datetime.now())

    state = fields.Selection([('choose', 'choose'), ('get', 'get')],default='choose')
    report = fields.Binary('Prepared file', filters='.xls', readonly=True)
    name = fields.Char('File Name', size=50)
    company_id = fields.Many2one('res.company','Company',default=lambda self: self.env.user.company_id.id)

    def get_lines(self):
        xfind = self.env['account.exchange'].search([('state', 'in', ('confirmed', 'done'))('request', '>=', self.date_from), ('request', '<=', self.date_to)])
        return xfind

    def generate_xls_report(self):

        wb1 = xlwt.Workbook(encoding='utf-8')
        ws1 = wb1.add_sheet(_('Exchange Transactions'))
        fp = BytesIO()

        header_content_style = xlwt.easyxf("font: name Helvetica size 20 px, bold 1, height 170; align: horiz center;")
        sub_header_style = xlwt.easyxf("font: name Helvetica size 10 px, bold 1, height 170")
        sub_header_style_c = xlwt.easyxf("font: name Helvetica size 10 px, bold 1, height 170; borders: left thin, right thin, top thin, bottom thin; align: horiz center")
        sub_header_style_r = xlwt.easyxf("font: name Helvetica size 10 px, bold 1, height 170; borders: left thin, right thin, top thin, bottom thin; align: horiz right")
        sub_header_content_style = xlwt.easyxf("font: name Helvetica size 10 px, height 170;")
        line_content_style = xlwt.easyxf("font: name Helvetica, height 170;")

        row = 0
        col = 0
        ws1.row(row).height = 500
        ws1.write_merge(row,row, 4, 5, _("Exchange Transactions"), header_content_style)
        xdate = self.date_now.strftime('%d/%m/%Y %I:%M:%S %p')
        xdate = datetime.strptime(xdate,'%d/%m/%Y %I:%M:%S %p') - timedelta(hours=4)
        xname = self.company_id.name
        xvat = self.company_id.vat
        ws1.write_merge(row,row, 0, 1, xname, header_content_style)
        ws1.write_merge(row,row, 2, 3, xvat, header_content_style)
        ws1.write_merge(row,row, 6, 7, xdate.strftime('%d/%m/%Y %I:%M:%S %p'), header_content_style)
        row += 2

        #CABECERA DE LA TABLA 
        ws1.col(col).width = 250
        ws1.write(row,col+0, _("Date of Request"),sub_header_style_c)
        ws1.col(col+0).width = int((len('xx/xx/xxxx')+10)*256)
        ws1.write(row,col+1, _("Amount"),sub_header_style_c)
        ws1.col(col+1).width = int((len('Amount')+10)*256)
        ws1.write(row,col+2, _("Origin Currency"),sub_header_style_c)
        ws1.col(col+2).width = int((len('Origin Currency')+10)*256)
        ws1.write(row,col+3, _("Transaction"),sub_header_style_c)
        ws1.col(col+3).width = int((len('Transaction')+10)*256)
        ws1.write(row,col+4, _("Rate"),sub_header_style_c)
        ws1.col(col+4).width = int((len('Rate')+20)*256)
        ws1.write(row,col+5, _("Converted Amount"),sub_header_style_c)
        ws1.col(col+5).width = int((len('Converted Amount')+20)*256)
        ws1.write(row,col+6, _("Final Currency"),sub_header_style_c)
        ws1.col(col+6).width = int((len('Final Currency')+26)*256)
        ws1.write(row,col+7, _("Reference"),sub_header_style_c)
        ws1.col(col+7).width = int((len('Reference')+10)*256)

        center = xlwt.easyxf("align: horiz center")
        right = xlwt.easyxf("align: horiz right")

        for item in self.get_lines():
            row += 1
            # Date of Request
            if item.request:
                ws1.write(row,col+0, item.request.strftime('%d/%m/%Y'),center)
            else:
                ws1.write(row,col+0, '',center)
            # Amount
            if item.amount:
                ws1.write(row,col+1, item.amount,right)
            else:
                ws1.write(row,col+1, '0',right)
            # Origin Currency
            if item.origin_currency_id:
                ws1.write(row,col+2, item.origin_currency_id.name,center)
            else:
                ws1.write(row,col+2, '0',center)
            # Transaction
            if item.transaction:
                ws1.write(row,col+3, item.transaction,center)
            else:
                ws1.write(row,col+3, '0',center)
            # Rate
            if item.rate:
                ws1.write(row,col+4, item.rate,right)
            else:
                ws1.write(row,col+4, '',right)
            # Converted Amount
            if item.final_amount:
                ws1.write(row,col+5, item.final_amount,right)
            else:
                ws1.write(row,col+5, '',center)
            # Final Currency
            if item.final_currency_id:
                ws1.write(row,col+6, item.final_currency_id.name,center)
            else:
                ws1.write(row,col+6, '',center)
            # Reference
            if item.reference:
                ws1.write(row,col+7, item.reference,center)
            else:
                ws1.write(row,col+7, '',center)

        wb1.save(fp)
        out = base64.encodestring(fp.getvalue())
        fecha  = datetime.now().strftime('%d/%m/%Y') 
        self.write({'state': 'get', 'report': out, 'name': _('Exchange Transactions')+ fecha +'.xls'})
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'transaction.exchange',
            'view_mode': 'form',
            'view_type': 'form',
            'res_id': self.id,
            'views': [(False, 'form')],
            'target': 'new',
        }