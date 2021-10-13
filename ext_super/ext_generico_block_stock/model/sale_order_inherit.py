# -*- coding: utf-8 -*-
# Copyright (C) Softhealer Technologies.

from odoo import fields,models,api,_
import datetime
from odoo.exceptions import UserError, ValidationError

class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    stock=fields.Float(compute='_compute_stock_mano')

    def _compute_stock_mano(self):
        for selff in self:
            selff.stock=selff.product_id.qty_available

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    def action_confirm(self):
        super().action_confirm()
        for det in self.order_line:
            if det.product_id.qty_available>0:
                if det.product_id.qty_available>=det.product_uom_qty:
                    pass
                else:
                    raise UserError(_("La cantidad a vender del producto %s no puede ser mayor al stock actual")%det.product_id.name)
            else:
                raise UserError(_("el producto %s no puede ser vendido con stock cero")%det.product_id.name)
