from odoo import fields, models

class PropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "estate property tag"
    _order = "name"

    name = fields.Char(string="Tag", required=True)
    color = fields.Integer(string="Color")