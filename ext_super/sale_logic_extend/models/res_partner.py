from odoo import api, fields, models

class ResPartnerLogicExtend(models.Model):
    _inherit = 'res.partner'
    
    customer_type = fields.Selection(string='Customer Type', selection=[('distributor', 'Distributor'), ('fleet', 'Fleet'), ('final_consumer', 'Final Consumer'), ('other_entities', 'Other Entities')])
    assigned_seller_id = fields.Many2one(comodel_name='res.partner', string='Assigned Seller')
    zone_id = fields.Many2one(comodel_name='res.partner.zone', string='Zone')
    payment_condition = fields.Selection(string='Payment Condition', selection=[('credit', 'Credit'), ('cash', 'Cash')])

    delivery_schedule = fields.Date(string='Delivery Schedule')
    direction_map = fields.Binary(string='Direction Map')

class ResPartnerZone(models.Model):
    _name='res.partner.zone'

    name = fields.Char(string='Name')
    description = fields.Char(string='Description')
    
