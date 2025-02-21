from email.policy import default
from tokenize import String

from odoo import models, fields, api, _
from datetime import date
from odoo.exceptions import UserError, ValidationError


class EstateProperty(models.Model):
    _name = 'estate.property'
    _description = 'model estate property'
    _order = "name desc"

    def _default_date(self):
        return fields.Date.today()

    active = fields.Boolean(default=True)
    name = fields.Char(string="Title", required=True)
    state = fields.Selection(
        [
            ("new","New"),
            ("received","Offer Received"),
            ("accepted","Offer Accepted"),
            ("sold","Sold"),
            ("canceled","Canceled")
        ],
        required=True,
        copy=False,
        default="new"
    )


    description = fields.Text()
    postcode = fields.Char(string="Postcode")
    date_availability = fields.Date(default=_default_date, string="Date Availability")
    expected_price = fields.Float(required=True, string="Expected Price")
    selling_price = fields.Float(string="Selling Price")
    bedrooms = fields.Integer()
    living_area = fields.Integer(string="Living Area")
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer(string="Garden Area")
    garden_orientation = (
        fields.Selection([('north', 'North'), ('south', 'South'), ('east', 'East'), ('west', 'West')]))

    total_area = fields.Integer(compute="_compute_total")
    best_price = fields.Float(compute="_compute_best_price")

    # ================ Relational Data ================
    property_type_id = fields.Many2one("estate.property.type", string="Property Type")
    buyer_id = fields.Many2one("res.partner", string="Buyer")
    sales_person_id = fields.Many2one("res.users", string="Sales Person")
    offer_ids = fields.One2many("estate.property.offer", "property_id")
    tag_ids = fields.Many2many("estate.property.tag")


    # ================ Function ================
    @api.depends("living_area","garden_area")
    def _compute_total(self):
        for property in self:
            property.total_area = property.living_area + property.garden_area

    @api.depends("offer_ids.price")
    def _compute_best_price(self):
        for property in self:
            property.best_price = max(property.offer_ids.mapped('price')) if property.offer_ids else 0

    @api.onchange("garden")
    def _onchange_garden(self):
        for estate in self:
            if not estate.garden:
                estate.garden_area=0

    # Date Availibility
    @api.onchange("date_availability")
    def _onchange_date_availability(self):
        if self.date_availability < date.today():

            return {
                "warning": {
                    "title": _("Warning"),
                    "message": _("The availability date cannot be in the past."),
                }
            }

    # Action Sold
    def action_sold(self):
        for estate in self:
            if estate.state == "canceled":
                raise UserError(_("A sold property cannot be canceled."))
            estate.state = "sold"

    # Action Cancel
    def action_cancel(self):
        for estate in self:
            if estate.state == "sold":
                raise UserError(_("A canceled property cannot be set as sold."))
            estate.state = "canceled"

    # ================ Python Constraint ================

    @api.constrains("expected_price")
    def _check_expected_price(self):
        for record in self:
            if record.expected_price < 0:
                raise ValidationError(_("The expected price must be strictly positive"))

    @api.constrains("selling_price")
    def _check_selling_price(self):
        for record in self:
            if record.selling_price < 0:
                raise ValidationError(_("The selling price must be strictly positive"))

    @api.constrains("selling_price", "expected_price")
    def _check_selling_price_lower(self):
        for record in self:
            if record.selling_price and record.expected_price:
                min_price = record.expected_price * 0.9
                if record.selling_price < min_price:
                    raise ValidationError("The selling price cannot be lower than 90% of the expected price!")

    # ================ SQL Constraint ================
    # _sql_constraints = [
    #     ("check_expected_price", "CHECK(expected_price > 0)", "The expected price must be strictly positive."),
    #     ("check_selling_price", "CHECK(selling_price >= 0)", "The selling price must be positive."),
    #     ("unique_property_type", "UNIQUE(property_type_id)", "The property type name must be unique."),
    # ]