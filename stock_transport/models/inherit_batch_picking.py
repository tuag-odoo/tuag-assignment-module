from odoo import models, fields, api
from odoo.exceptions import ValidationError

class InheritBatchPicking(models.Model):
    _inherit = 'stock.picking.batch'

    dock_id = fields.Many2one('stock.dock', string="Dock", placeholder="eg. dock 1")
    vehicle_id = fields.Many2one('fleet.vehicle', string='Vehicle', store=True)
    vehicle_category_id = fields.Many2one('fleet.vehicle.model.category', string='Vehicle Category', store=True)
    volume = fields.Float(compute="_compute_volume", store=True)
    weight = fields.Float(compute="_compute_weight", store=True)
    
    @api.depends("vehicle_category_id.max_volume", "picking_ids", "picking_ids.move_ids_without_package.quantity", "picking_ids.move_ids_without_package.product_id.volume")
    def _compute_volume(self):
        for record in self:
            total_volume = 0
            for batch in record.picking_ids:
                for product in batch.move_ids_without_package:
                    total_volume += (product.product_id.volume)*(product.quantity)
        if(record.vehicle_category_id.max_volume != 0):
            volume_percentage = round(100 * (total_volume / record.vehicle_category_id.max_volume))
            if(volume_percentage > 100):
                raise ValidationError(f"""Your Product volume is greater then inventory capacity""")
            else:
                self.volume = volume_percentage
        else:
            self.volume = 0
 
    @api.depends("vehicle_category_id.max_weight","picking_ids", "picking_ids.move_ids_without_package.quantity", "picking_ids.move_ids_without_package.product_id.weight")
    def _compute_weight(self):
        for record in self:
            total_weight = 0
            for batch in record.picking_ids:
                for product in batch.move_ids_without_package:
                    total_weight += (product.product_id.weight)*(product.quantity)
        if(record.vehicle_category_id.max_weight != 0):
            weight_percentage = round(100 * (total_weight / record.vehicle_category_id.max_weight))
            if(weight_percentage > 100):
                raise ValidationError(f"""Your Product weight is greater then inventory capacity""")
            else:
                self.weight = weight_percentage
        else:
            self.weight = 0

    @api.depends('weight', 'volume')
    def _compute_display_name(self):
        for category in self:
            category.display_name = f"{category.name} ({category.weight} kg, {category.volume} m3) - {category.vehicle_id.driver_id.name}"
