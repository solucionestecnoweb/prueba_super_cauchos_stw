from operator import index
from odoo import api, fields, models, _
from datetime import datetime, date, timedelta
import base64
from odoo.exceptions import UserError, ValidationError, Warning
from odoo.tools.float_utils import float_round

class ProrrateoIva(models.Model):
    _name = "prorrateo.iva"

    name = fields.Char(string='Código', default='Borrador')
    desde = fields.Date(string='Desde')
    hasta = fields.Date(string='Hasta')
    deducible = fields.Float(string='% Deducible')
    no_deducible = fields.Float(string='% No Deducible')
    invoice_ids = fields.Many2many(comodel_name='account.move', string='Facturas')
    move_ids = fields.Many2many(comodel_name='account.move.line', string='Asientos Contables')
    state = fields.Selection(string='Estado', selection=[('draft', 'Borrador'), ('posted', 'Publicado')], default='draft')
    company_id = fields.Many2one('res.company','Compañía',default=lambda self: self.env.company.id)
    
    @api.constrains('state')
    def constraint_name(self):
        if self.state == 'posted':
            self.name = self.env['ir.sequence'].next_by_code('prorrateo.iva.seq')

    def post(self):
        self.state = 'posted'
    
    def draft(self):
        self.state = 'draft'

    def find_lines(self):
        xfind = self.env['account.move'].search([
            ('date', '>=', self.desde),
            ('date', '<=', self.hasta),
            ('state', '=', 'posted'),
            ('type', '!=', 'entry'),
            ('company_id', '=', self.company_id.id),
        ])
        self.invoice_ids = xfind

    def float_format(self,valor):
        if valor:
            result = '{:,.2f}'.format(valor)
            result = result.replace(',','*')
            result = result.replace('.',',')
            result = result.replace('*','.')
        else:
            result="0,00"
        return result