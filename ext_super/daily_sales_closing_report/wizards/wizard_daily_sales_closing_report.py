from datetime import datetime, timedelta
from operator import mod
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

class DailySales(models.Model):
    _name = 'daily.sales'

    name = fields.Date(string='Invoice Date')
    invoice_num = fields.Char(string='Invoice Number')
    partner_id = fields.Many2one(comodel_name='res.partner', string='Customer')
    currency_rate = fields.Float(string='Rate')
    total_bs = fields.Float(string='Total Bs. Operation')
    total_usd = fields.Float(string='Total $ Operation')
    payment_condition_id = fields.Many2one(comodel_name='account.condition.payment', string='Payment Condition')
    amount = fields.Float(string='Amount')
    currency_id = fields.Many2one(comodel_name='res.currency', string='Currency')

class DailySalesReport(models.Model):
    _name = 'daily.sales.report'

    date_from = fields.Date(string='Date From', default=lambda *a:datetime.now().strftime('%Y-%m-%d'))
    date_to = fields.Date('Date To', default=lambda *a:(datetime.now() + timedelta(days=(1))).strftime('%Y-%m-%d'))
    date_now = fields.Datetime(string='Date Now', default=lambda *a:datetime.now())

    state = fields.Selection([('choose', 'choose'), ('get', 'get')],default='choose')
    report = fields.Binary('Prepared file', filters='.xls', readonly=True)
    name = fields.Char('File Name', size=50)
    company_id = fields.Many2one('res.company','Company',default=lambda self: self.env.user.company_id.id)

    def print_report(self):
        self.env['daily.sales'].search([]).unlink()
        self.get_invoice()
        return {
            'type': 'ir.actions.report',
            'report_name': 'daily_sales_closing_report.daily_sales_closing_report',
            'report_type':"qweb-pdf"
            }

    def get_invoice(self):
        xfind = self.env['account.move'].search([
            ('invoice_date', '>=', self.date_from),
            ('invoice_date', '<=', self.date_to),
            ('type', '=', 'out_invoice'),
        ])
        
        for item in xfind:
            rate = 0.00
            if item.currency_id.name == 'Bs.':
                rates = item.env['res.currency.rate'].search([
                    ('name', '=', item.invoice_date)
                ], limit=1).sell_rate
                if rates > 0:
                    rate = rates
                else:
                    rate = 1
            else:
                if item.os_currency_rate > 0:
                    rate = item.os_currency_rate
                else:
                    rate = 1

            if item.currency_id.name == 'Bs.':
                total_bs = item.amount_total
                total_usd = round(item.amount_total / rate, 2)
            else:
                total_bs =round (item.amount_total * item.os_currency_rate, 2)
                total_usd = item.amount_total

            if item.payment_condition_id:
                payment_condition = item.payment_condition_id.id
            else:
                payment_condition = False

            values = {
                'name': item.invoice_date,
                'invoice_num': item.invoice_number_cli,
                'partner_id': item.partner_id.id,
                'currency_rate': rate,
                'total_bs': total_bs,
                'total_usd': total_usd,
                'payment_condition_id': payment_condition,
                'amount': item.amount_total,
                'currency_id': item.currency_id.id,
            }
            self.env['daily.sales'].create(values)

    def get_lines(self):
        xfind = self.env['daily.sales'].search([])
        return xfind

    def show_daily_sales(self):
        self.env['daily.sales'].search([]).unlink()
        self.get_invoice()
        self.ensure_one()
        res = self.env.ref('daily_sales_closing_report.daily_sales_action').read()[0]
        return res

    # *******************  REPORTE EN EXCEL ****************************

    def generate_xls_report(self):
        self.env['daily.sales'].search([]).unlink()
        self.get_invoice()

        wb1 = xlwt.Workbook(encoding='utf-8')
        ws1 = wb1.add_sheet(_('Daily Sales Closing Report'))
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
        ws1.write_merge(row,row, 3, 5, _("Daily Sales Closing Report"), header_content_style)
        xdate = self.date_now.strftime('%d/%m/%Y %I:%M:%S %p')
        xdate = datetime.strptime(xdate,'%d/%m/%Y %I:%M:%S %p') - timedelta(hours=4)
        ws1.write_merge(row,row, 6, 8, xdate.strftime('%d/%m/%Y %I:%M:%S %p'), header_content_style)
        row += 2

        #CABECERA DE LA TABLA 
        ws1.write(row,col+0, _("Date"),sub_header_style_c)
        ws1.col(col+0).width = int((len('xx/xx/xxxx')+2)*256)
        ws1.write(row,col+1, _("Invoice Num"),sub_header_style_c)
        ws1.col(col+1).width = int((len('Invoice Num')+5)*256)
        ws1.write(row,col+2, _("Customer"),sub_header_style_c)
        ws1.col(col+2).width = int((len('Customer')+26)*256)
        ws1.write(row,col+3, _("Rate"),sub_header_style_c)
        ws1.col(col+3).width = int((len('Rate')+15)*256)
        ws1.write(row,col+4,_("Total Bs. Operation"),sub_header_style_c)
        ws1.col(col+4).width = int((len('Total Bs. Operation')+2)*256)
        ws1.write(row,col+5, _("Total $ Operation"),sub_header_style_c)
        ws1.col(col+5).width = int((len('Total $ Operation')+2)*256)
        ws1.write(row,col+6, _("Payment Condition"),sub_header_style_c)
        ws1.col(col+6).width = int((len('Payment Condition')+5)*256)
        ws1.write(row,col+7, _("Amount"),sub_header_style_c)
        ws1.col(col+7).width = int((len('Amount')+10)*256)
        ws1.write(row,col+8, _("Currency"),sub_header_style_c)
        ws1.col(col+8).width = int((len('Currency')+2)*256)

        center = xlwt.easyxf("align: horiz center")
        right = xlwt.easyxf("align: horiz right")

        #Totales
        total_bs = 0
        total_usd = 0
        total_amount = 0
        #####
        total_credit_bs = 0
        total_credit_usd = 0
        total_cash_bs = 0
        total_cash_usd = 0

        for item in self.get_lines():
            row += 1
            # Date
            if item.name:
                ws1.write(row,col+0, item.name.strftime('%d/%m/%Y'),center)
            else:
                ws1.write(row,col+0, '',center)
            # Invoice Number
            if item.invoice_num:
                ws1.write(row,col+1, item.invoice_num,center)
            else:
                ws1.write(row,col+1, '',center)
            # Customer
            if item.partner_id.name:
                ws1.write(row,col+2, item.partner_id.name,center)
            else:
                ws1.write(row,col+2, item.name,center)
            # Rate
            if item.currency_rate:
                ws1.write(row,col+3, item.currency_rate,right)
            else:
                ws1.write(row,col+3, '',right)
            # Total Bs. Operation
            if item.total_bs:
                ws1.write(row,col+4, round(item.total_bs, 2),right)
            else:
                ws1.write(row,col+4, '',right)
            # Total $ Operation
            if item.total_usd:
                ws1.write(row,col+5, round(item.total_usd, 2),right)
            else :
                ws1.write(row,col+5,'',right)
            # Payment Condition
            if item.payment_condition_id:
                ws1.write(row,col+6, item.payment_condition_id.name,center)
            else :
                ws1.write(row,col+6, '',center)
            # Amount
            if item.amount:
                ws1.write(row,col+7,item.amount,right)
            else :
                ws1.write(row,col+7,'',right)
            # Currency
            if item.currency_id:
                ws1.write(row,col+8,item.currency_id.name,center)
            else :
                ws1.write(row,col+8,'',center)
            
            if item.payment_condition_id.name in ('contado', 'Contado', 'CONTADO'):
                total_cash_bs += item.total_bs
                total_cash_usd += item.total_usd
            elif item.payment_condition_id.name in ('credito', 'Credito', 'CREDITO', 'crédito', 'Crédito', 'CRÉDITO'):
                total_credit_bs += item.total_bs
                total_credit_usd += item.total_usd

            total_bs += item.total_bs
            total_usd += item.total_usd
            total_amount += item.amount
                
        row += 1
        ws1.write(row,col+4, total_bs,center)
        ws1.write(row,col+5, total_usd,center)
        ws1.write(row,col+7, total_amount,center)

        row += 2
        ws1.write(row,col+3, '',sub_header_style_c)
        ws1.write(row,col+4, _('$ Amount'),sub_header_style_c)
        ws1.write(row,col+5, _('Bs. Amount'),sub_header_style_c)
        row += 1
        ws1.write(row,col+3, _('Credit Bs./$'),sub_header_style_c)
        ws1.write(row,col+4, total_credit_usd,right)
        ws1.write(row,col+5, total_credit_bs,right)
        row += 1
        ws1.write(row,col+3, _('Cash Bs./$'),sub_header_style_c)
        ws1.write(row,col+4, total_cash_usd,right)
        ws1.write(row,col+5, total_cash_bs,right)
        row += 1
        ws1.write_merge(row,row,col+3,col+4, _('Total Bs.'),sub_header_style_c)
        ws1.write(row,col+5, total_cash_bs + total_credit_bs,right)

        wb1.save(fp)
        out = base64.encodestring(fp.getvalue())
        fecha  = datetime.now().strftime('%d/%m/%Y') 
        self.write({'state': 'get', 'report': out, 'name': _('Daily Sales Closing Report ')+ fecha +'.xls'})
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'daily.sales.report',
            'view_mode': 'form',
            'view_type': 'form',
            'res_id': self.id,
            'views': [(False, 'form')],
            'target': 'new',
        }