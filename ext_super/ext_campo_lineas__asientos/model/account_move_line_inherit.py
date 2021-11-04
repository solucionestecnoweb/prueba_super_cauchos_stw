# -*- coding: utf-8 -*-


import logging
from datetime import datetime
from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError




class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    def _nro_doc(self):
    	var=self.move_id.invoice_number
    	return var

    nro_doc=fields.Char(string="Nro Documento", default=_nro_doc)
   

   
    #uni_neg_id = fields.Many2one('stock.unidad.negocio')