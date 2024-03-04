from odoo import models, fields

class StockDock(models.Model):
    _name = 'stock.dock'

    name = fields.Char()