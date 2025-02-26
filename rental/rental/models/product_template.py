from odoo import models, fields, api

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    # ================ Non Relational Data ================

    is_rent  = fields.Boolean(string='Can Be Rented')
    count_rent  = fields.Integer(compute="_compute_count_rent")

    # ================ Function ================

    # Count Is Rent
    @api.depends('is_rent')
    def _compute_count_rent(self):
        rent_count = self.env['product.template'].search_count([('is_rent', '=', True)])
        for rent in self:
            rent.count_rent = rent_count

    # List Rent
    def action_view_reserved_orders(self):
        # Filter Sale Order
        sale_orders = self.env['sale.order.line'].search([
            ('product_id.product_tmpl_id', '=', self.id),
            ('order_id.rental_status', '=', 'reserved')
        ]).mapped('order_id')
        return {
            'name': 'Reserved Sale Orders',
            'type': 'ir.actions.act_window',
            'view_mode': 'tree,form',
            'res_model': 'sale.order',
            'domain': [('id', 'in', sale_orders.ids)],
            'views': [(self.env.ref('rental.view_sale_order_reserved_tree').id, 'tree'),
                      (False, 'form')],
            'context': {'default_rental_status': 'reserved'},
        }