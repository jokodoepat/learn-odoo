from odoo import fields, models, api
from odoo.exceptions import ValidationError


class PropertyType(models.Model):
    _name = "estate.property.type"
    _description = "estate property type"
    _order = "name"

    name = fields.Char(string="Name")
    sequence = fields.Integer(default=1)

    property_ids = fields.One2many("estate.property", "property_type_id")

    # ================ Python Constraint ================

    @api.constrains("name")
    def _check_name(self):
        for record in self:
            existing_tag = self.search([
                ("name", "=", record.name)
            ])
            if existing_tag:
                raise ValidationError("The property type id must be unique!")