# -*- coding: utf-8 -*-
from odoo import api, fields, models
from datetime import datetime
from odoo.exceptions import UserError, ValidationError, except_orm, Warning


class PurchaseOrder(models.Model):
    _inherit = "purchase.order"
    
    approvals_ids = fields.One2many('approval.request', 'purchase_id', string='aprobaciones')
    approver_ids = fields.Many2many('res.users', string='Aprobadores')
    is_approval = fields.Boolean(string="Tiene aprobacion")
    
    def approvals_request_purchase(self):
        for purchase in self:
            if purchase.is_approval and not purchase.order_line:
                raise UserError(
                    "No puede enviar una orden de compra sin lineas de pedidos. Por favor agregue lineas a la orden")
            approvers = len(purchase.approver_ids)
            category_obj = self.env['approval.category'].search([('is_purchase', '=', 'required')], limit=1)
            if approvers > len(category_obj.user_ids):
                raise UserError(
                    "No puede agregar mas arpobadores de lo estipulado."
                     "Vaya a Aprobaciones / Configuración / Tipo de aprobación.")
            for aproval in purchase.approvals_ids:
                if aproval.request_status in ['new', 'pending', 'approved']:
                    raise ValidationError("Existe una aprobacion en curso")
                if aproval.request_status == "refused":
                    raise ValidationError("Verifique si no existe una solicitud Rechazada antes de generar una nueva")
            values = {
                'name': category_obj.name,
                'category_id': category_obj.id,
                'date': datetime.now(),
                'request_owner_id': purchase.env.user.id,
                'amount': purchase.amount_total,
                'purchase_id': purchase.id,
                'request_status': 'pending'
            }
            t = self.env['approval.request'].create(values)
            for item in purchase.approver_ids:
                self.env['approval.approver'].create({
                    'user_id': item.id,
                    'request_id': t.id,
                    'status': 'pending'
            })
            if not category_obj:
                raise ValidationError(
                    "No existe una categoría de aprobación para este tipo de registro."
                     "Vaya a Aprobaciones / Configuración / Tipo de aprobación.")
            if len(category_obj) > 2:
                raise ValidationError(
                    "Existe mas de dos categoría de aprobación para este tipo de registro."
                     "Vaya a Aprobaciones / Configuración / Tipo de aprobación.")

    def button_confirm(self):
        res = super(PurchaseOrder, self).button_confirm()
        for sale in self:
            if sale.is_approval and sale.approver_ids:
                sale.picking_ids.write({
                    'is_approval': True,
                    'approver_ids': sale.approver_ids
                })
        return res


