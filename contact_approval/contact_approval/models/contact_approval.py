from odoo import models, fields, api, _
from datetime import date
from odoo.exceptions import UserError, ValidationError

class ContactApproval(models.Model):
    _inherit = 'res.partner'

    # ================ Non Relational Data ================

    state = fields.Selection(
        [
            ("draft","Draft"),
            ("approved","Approved"),
            ("canceled","Canceled")
        ],
        string="State",
        default="draft"
    )

    # ================ Relational Data ================

    approver_id = fields.Many2one('res.users', string='Approved By', readonly=True)

    # ================ Function ================

    def action_approve(self):
        for rec in self:
            rec.approver_id = self.env.user
            rec.state = 'approved'

    def action_cancel(self):
        for rec in self:
            rec.approver_id = self.env.user
            rec.state = 'canceled'

    def action_reset(self):
        for rec in self:
            rec.approver_id = False
            rec.state = 'draft'