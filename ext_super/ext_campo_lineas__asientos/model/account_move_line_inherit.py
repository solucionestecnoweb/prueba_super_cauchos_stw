# -*- coding: utf-8 -*-


import logging
from datetime import datetime
from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError




class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    #@api.onchange('state')
    #@api.depent('state')
    #@api.constrains('move_id')
    """def _nro_doc(self):
        var=self.move_id.invoice_number
        self.nro_doc=self.move_id.invoice_number
        return var"""

    nro_doc=fields.Char(string="Nro Documento")
    nro_doc_aux=fields.Char(compute='_compute_nro_doc')

    #@api.depent('parent_state')
    @api.onchange('parent_state')
    def _compute_nro_doc(self):
    	for selff in self:
    		if selff.move_id.invoice_number:
    			if selff.account_id.user_type_id.type in ('receivable','payable'):
		    		selff.nro_doc_aux=selff.move_id.invoice_number
		    		selff.nro_doc=selff.move_id.invoice_number
		    	else:
		    		selff.nro_doc_aux=selff.move_id.invoice_number
	    	else:
	    		selff.nro_doc_aux=selff.move_id.invoice_number