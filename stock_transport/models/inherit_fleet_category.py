from odoo import fields, models, api

class InheritFleetCategory(models.Model):
    _inherit = "fleet.vehicle.model.category"

    max_weight = fields.Float(string="Max Weight (Kg)", store=True);
    max_volume = fields.Float(string="Max Volume (m\u00B3)", store = True);

    @api.depends('max_weight', 'max_volume')
    def _compute_display_name(self):
        for category in self:
            category.display_name = f"{category.name} ({category.max_weight} kg, {category.max_volume} m3)"
