from odoo import fields, models, api

class StockPicking(models.Model):
    _inherit = 'stock.picking'

    volume = fields.Float('Volume', compute='_compute_volume')

    @api.depends("move_ids.product_id", "move_ids.quantity")
    def _compute_volume(self):
        for record in self:
                total = 0
                for move in record.move_ids:
                    total += move.product_id.volume*move.quantity
                record.volume = total
