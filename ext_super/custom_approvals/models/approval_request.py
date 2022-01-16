# -*- coding: utf-8 -*-
from odoo import api, fields, models
from odoo.tools import ustr


class ApprovalRequest(models.Model):
    _inherit = 'approval.request'

    is_rejected = fields.Selection(related="category_id.is_rejected")
    type_rejected = fields.Selection(string="Tipo Rechazo", selection=[
        ('credit_limit', 'Limite de Credito'),
        ('expiration', 'Vencimiento'),
        ('documents', 'Documentos'),
        ('Others', 'Otros'),
        ('free_field_writing', 'Campo Libre Escritura')
    ])


class ApprovalApprover(models.Model):
    _inherit = 'approval.approver'

    def name_get(self):
        """ Se reemplaza el atributo de la clase _rec_name para concatenar
            varios campos del objeto
            :return list: la concatenación del nuevo _rec_name
        """
        result = []
        for registro in self:
            name = ustr(registro.user_id.name).capitalize()
            result.append((registro.id, name))
        return result