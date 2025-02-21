from dateutil.relativedelta import relativedelta

from odoo import fields, models, api, _
from odoo.exceptions import UserError


class EstateOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Offer Made"
    _rec_name = "property_id"
    _order = "price desc"

    price = fields.Float()
    status = fields.Selection(
        [
            ("accepted","Accepted"),
            ("refused","Refused")
        ], copy = False,
    )

    validity = fields.Integer(String="Validity", Default=7)
    date_deadline = fields.Date(compute="_compute_date_deadline", inverse="_inverse_date_deadline")

    # Relational
    partner_id = fields.Many2one("res.partner",required=True, string="Partner")
    property_id = fields.Many2one("estate.property",required=True, string="Property")
    property_type_id = fields.Many2one(related="property_id.property_type_id", store=True)

    # Function
    @api.depends("validity")
    def _compute_date_deadline(self):
        for property in self:
            property.date_deadline = fields.Date.today() + relativedelta(days=property.validity)

    def _inverse_date_deadline(self):
        for property in self:
            property.validity = (property.date_deadline - fields.Date.today()).days


    # Action Accept
    def action_accept(self):
        self.ensure_one()
        if "accepted" in self.property_id.offer_ids.mapped('status'):
            raise UserError(_("The house has been sold."))
        self.status = "accepted"
        self.property_id.selling_price = self.price
        self.property_id.buyer_id = self.partner_id


    # Action Refuse
    def action_refuse(self):
        self.status = "refused"