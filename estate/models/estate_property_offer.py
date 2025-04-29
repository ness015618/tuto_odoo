from odoo import api,fields,models
from odoo.exceptions import UserError, ValidationError
from dateutil.relativedelta import relativedelta

class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "offer made by a potential buyer"
    _order = "price desc"

    price = fields.Float(string="Price")
    status = fields.Selection(
        string="Status",
        copy=False,
        selection=[('accepted','Accepted'),('refused','Refused')])
    partner_id = fields.Many2one("res.partner", string="Partner", required=True)
    property_id = fields.Many2one("estate.property", string="Propriété", required=True)
    
    validity = fields.Integer(string="Validity", default=7)
    date_deadline = fields.Date(string="Deadline", compute="_compute_deadline", inverse="_inverse_deadline")

    _sql_constraints = [
        ('check_offer_price','CHECK(price >= 0)', "An offer should be positive.")
    ]

    property_type_id = fields.Many2one(related="property_id.property_type_id", store=True, string="Property Type")

    @api.depends("create_date","validity")
    def _compute_deadline(self):
        for record in self:
            if record.create_date:
                record.date_deadline = record.create_date + relativedelta(days=record.validity)
            else:
                record.date_deadline = fields.Date.today() + relativedelta(days=record.validity)

    @api.depends("date_deadline")
    def _inverse_deadline(self):
        for record in self:
            if record.date_deadline and record.create_date:
                delta = record.date_deadline - record.create_date.date()
                record.validity = delta.days

    def action_refuse_offer(self):
        for record in self:
            record.status = 'refused'
        return True
    
    def action_accept_offer(self):
        for record in self:
            for offer in record.property_id.offers_ids:
                if offer != record: 
                    if offer.status == 'accepted':
                        raise UserError("Another offer was already accepted.")
                    else:
                        offer.status = 'refused'
            record.status = 'accepted'
            record.property_id.state = 'offer_accepted'
            record.property_id.selling_price = record.price
            record.property_id.buyer_id = record.partner_id
        return True
    
    @api.model
    def create(self, vals):
        if vals.get("property_id"):
            property = self.env["estate.property"].browse(vals["property_id"])
            higher_offers = self.search([
            ('property_id', '=', vals["property_id"]),
            ('price', '>=', vals['price'])])

        if higher_offers:
            raise ValidationError("You cannot create an offer lower than an existing offer.")
        
        property.state = 'offer_received'
        return super().create(vals)