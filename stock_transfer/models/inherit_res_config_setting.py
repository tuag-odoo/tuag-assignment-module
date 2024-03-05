from odoo import fields, models

class InheritResConfigSetting(models.TransientModel):
    _inherit = 'res.config.settings'

    module_stock_transport = fields.Boolean(string="Dispatch Management System",  help="Trasport management: organize packs in your fleet, or carriers")
