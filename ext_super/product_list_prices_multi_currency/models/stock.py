from odoo import api, fields, models
from datetime import datetime, timedelta
import xlsxwriter
import shutil
import base64
import csv
import xlwt


class ProductPricesList(models.Model):
    _inherit = 'product.product'

    prices_list_item_ids = fields.Many2many('product.pricelist.item', string=' Prices', compute='_compute_prices_list_item')

    def _compute_prices_list_item(self):
        for item in self:
            item.prices_list_item_ids = False
            xfind = self.env['product.pricelist.item'].search([
                ('product_id', '=', item.id)
            ])
            if len(xfind) > 0:
                item.prices_list_item_ids = xfind

class TemplatePricesList(models.Model):
    _inherit = 'product.template'

    prices_list_item_ids = fields.Many2many('product.pricelist.item', string=' Prices', compute='_compute_prices_list_item')
    
    def _compute_prices_list_item(self):
        for item in self:
            item.prices_list_item_ids = False
            xfind = self.env['product.pricelist.item'].search([
                ('product_tmpl_id', '=', item.id)
            ])
            if len(xfind) > 0:
                item.prices_list_item_ids = xfind
