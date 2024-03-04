from odoo import models, fields, api

class InheritBatchPicking(models.Model):
    _inherit = 'stock.picking.batch'

    dock_id = fields.Many2one('stock.dock', string="Dock")
    vehicle_id = fields.Many2one('fleet.vehicle.model', string='Vehicle', placeholder='Third party provider')
    vehicle_category_id = fields.Many2one('fleet.vehicle.model.category', string='Vehicle Category', placeholder='eg. Semi-truck')
    volume = fields.Float(compute="_compute_volume", store=True)
    weight = fields.Float(compute="_compute_weight", store=True)
    
    @api.depends("vehicle_category_id", "move_line_ids")
    def _compute_volume(self):
        total_volume = 0
        for record in self.move_ids:
            total_volume += (record.product_id.volume)*(record.quantity)
        if(self.vehicle_category_id.max_volume != 0):
            self.volume = round(total_volume / self.vehicle_category_id.max_volume)
        else:
            self.volume = 0
 
    @api.depends("vehicle_category_id","move_line_ids")
    def _compute_weight(self):
        total_weight = 0
        for record in self.move_ids:
            total_weight += (record.product_id.weight)*(record.quantity)
        if(self.vehicle_category_id.max_volume != 0):
            self.weight = round(total_weight / self.vehicle_category_id.max_weight)
        else:
            self.weight = 0
