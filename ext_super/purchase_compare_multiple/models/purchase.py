from odoo import api, fields, models, _
from odoo.exceptions import ValidationError
from datetime import datetime, timedelta, date


class PurchaseCompareMultiple(models.Model):
    _name = 'purchase.compare.multiple'
    _description = 'Model for comparations of multiple purchase order prices'

    name = fields.Char(string='Reference', default='/')
    purchase_order_ids = fields.Many2many(comodel_name='purchase.order', string='Purchase Orders')
    purchase_compared_prices_ids = fields.One2many(comodel_name='purchase.compared.prices', inverse_name='purchase_compare_multiple_id', string='Purchase Compared Prices')
    state = fields.Selection(string='State', selection=[('draft', 'Draft'), ('done', 'Done'), ('cancel', 'Cancel')], default='draft')
    
    def state_draft(self):
        self.state = 'draft'

    def state_done(self):
        self.state = 'done'

    def state_cancel(self):
        self.state = 'cancel'

    @api.constrains('state')
    def _compute_name(self):
        if self.name == '/' and self.state == 'done':
            self.name = self.env['ir.sequence'].next_by_code('purchase.compare.multiple.sequence')
    
    def _return_date_today(self):
        today_date = datetime.now() - timedelta(hours=4)
        return today_date

    def compare_price(self):
        if len(self.purchase_order_ids) != 3:
            raise ValidationError(_("There must be three records in the purchase orders to be able to compare"))
        else:
            t = self.env['purchase.compared.prices.lines']
            t.search([]).unlink()
            for item in self.purchase_order_ids: #Inicia el ciclo para comparar precios
                for line in item.order_line: #Ubica en las lineas de productos
                    values = {
                        'product_id': line.product_template_id.id,
                        'provider_id': item.partner_id.id,
                        'qty': line.product_qty,
                        'price': line.price_unit,
                    }
                    t.create(values)
            self._compare_lines()

    def _compare_lines(self):
        self.env['purchase.compared.prices'].search([('purchase_compare_multiple_id', '=', self.id)]).unlink()
        xfind = self.env['purchase.compared.prices.lines'].search([])
        provider_l = 0
        qtyl = 0
        price_l = 0
        provider_m = 0
        qtym = 0
        price_m = 0
        provider_h = 0
        qtyh = 0
        price_h = 0
        product_temporal = ''
        counter = len(xfind)
        for item in xfind.sorted(key=lambda a: a.product_id.id): #Recorremos las lineas y asignamos valor a las variables
            #Evaluación de Registro de Lineas
            counter -= 1
            if product_temporal != item.product_id.id: #Aseguramos si cambio de producto
                if product_temporal != '': #Si cambió de producto hará el registro en el modelo
                    values ={
                        'product_id': product_temporal,
                        'provider_id1': provider_l,
                        'qty1': qtyl,
                        'price1': price_l,
                        'provider_id2': provider_m,
                        'qty2': qtym,
                        'price2': price_m,
                        'provider_id3': provider_h,
                        'qty3': qtyh,
                        'price3': price_h,
                        'purchase_compare_multiple_id': self.id,
                    }
                    self.env['purchase.compared.prices'].create(values)     
                    provider_l = 0
                    price_l = 0
                    provider_m = 0
                    price_m = 0
                    provider_h = 0
                    price_h = 0
                product_temporal = item.product_id.id #Asignamos nuevo producto

            #Comparativa de precios
            if item.price < price_l or price_l == 0:
                price_l = item.price
                provider_l = item.provider_id.id
                qtyl = item.qty

            if item.price > price_h or price_h == 0:
                price_h = item.price
                provider_h = item.provider_id.id
                qtyh = item.qty

            if price_m == 0:
                price_count = 0
                find_lines = self.env['purchase.compared.prices.lines'].search([('product_id', '=', item.product_id.id)])
                for line in find_lines:
                    price_count += line.price
                price_count = price_count / len(find_lines)
                find_mid_price = self.env['purchase.compared.prices.lines'].search([('product_id', '=', item.product_id.id), ('price', '<=', price_count)], limit=1)
                price_m = find_mid_price['price']
                provider_m = find_mid_price['provider_id'].id
                qtym = find_mid_price['qty']
            
            if counter == 0: #Registro de la última comparativa
                values ={
                    'product_id': item.product_id.id,
                    'provider_id1': provider_l,
                    'qty1': qtyl,
                    'price1': price_l,
                    'provider_id2': provider_m,
                    'qty2': qtym,
                    'price2': price_m,
                    'provider_id3': provider_h,
                    'qty3': qtyh,
                    'price3': price_h,
                    'purchase_compare_multiple_id': self.id,
                }
                self.env['purchase.compared.prices'].create(values)     

class PurchaseComparedPrices(models.Model):
    _name = 'purchase.compared.prices'

    product_id = fields.Many2one(comodel_name='product.template', string='Product')
    provider_id1 = fields.Many2one(comodel_name='res.partner', string='Provider')
    qty1 = fields.Integer(string='Quantity')
    price1 = fields.Float(string='Lower price')
    provider_id2 = fields.Many2one(comodel_name='res.partner', string='Provider')
    qty2 = fields.Integer(string='Quantity')
    price2 = fields.Float(string='Half price')
    provider_id3 = fields.Many2one(comodel_name='res.partner', string='Provider')
    qty3 = fields.Integer(string='Quantity')
    price3 = fields.Float(string='Higher price')
    purchase_compare_multiple_id = fields.Many2one(comodel_name='purchase.compare.multiple', string='Purchase Compare')
    currency_id = fields.Many2one('res.currency', string='Currency', default=lambda self: self.env.user.company_id.currency_id)

class PurchaseComparedPricesLines(models.Model):
    _name = 'purchase.compared.prices.lines'

    product_id = fields.Many2one(comodel_name='product.template', string='Product')
    provider_id = fields.Many2one(comodel_name='res.partner', string='Provider')
    qty = fields.Integer(string='Quantity')
    price = fields.Float(string='Price')
