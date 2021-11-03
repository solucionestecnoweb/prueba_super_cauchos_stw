# -*- coding: utf-8 -*-


import logging
from datetime import datetime
from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError




class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    nro_comprobante=fields.Char(string="Nro Comprobante")
   
    #uni_neg_id = fields.Many2one('stock.unidad.negocio')