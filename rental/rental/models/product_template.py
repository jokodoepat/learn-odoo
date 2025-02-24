from odoo import models, fields, api

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    # ================ Non Relational Data ================

    is_rent  = fields.Boolean(string='Can Be Rented')
    count_rent  = fields.Integer(compute="_compute_count_rent")

    # ================ Function ================

    @api.depends('is_rent')
    def _compute_count_rent(self):
        rent_count = self.env['product.template'].search_count([('is_rent', '=', True)])
        for rent in self:
            rent.count_rent = rent_count