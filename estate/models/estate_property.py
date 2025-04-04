from odoo import fields, models
from dateutil.relativedelta import relativedelta

class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "tuto real estate property"

    name = fields.Char(string='Title', required=True)
    description = fields.Text(string='Description')
    postcode = fields.Char(string="Post Code")
    date_availability = fields.Date(string="Date Availability", copy=False, default=lambda self: fields.Date.today() + relativedelta(months=3))
    expected_price = fields.Float(string="Expected Price", required=True)
    selling_price = fields.Float(string="Selling Price", readonly=True, copy=False)
    bedrooms = fields.Integer(string="Bedrooms", default=2)
    living_area = fields.Integer(string="Living Area")
    facades = fields.Integer(string="Facades")
    garage = fields.Boolean(string="Garage")
    garden = fields.Boolean(string="Garden")
    garden_area = fields.Integer(string="Garden Area")
    garden_orientation = fields.Selection(
        string="Garden Orientation",
        selection=[('north','North'),('east','East'),('south','South'),('west','West')])
    active = fields.Boolean(string="Active", default=True)
    state = fields.Selection(
        string="Status",
        selection=[('new','New'),('offer_received', 'Offer Received'),
                   ('offer_accepted','Offer Accepted'),('sold','Sold'),('cancelled','Cancelled')],
                   required=True,
                   copy=False,
                   default='new')

    property_type_id = fields.Many2one("estate.property.type", string="Property Type")
    buyer_id = fields.Many2one("res.users", string="Buyer", copy=False)
    salesperson_id = fields.Many2one("res.users", string="Salesperson",default=lambda self: self.env.user)

    tags_ids = fields.Many2many("estate.property.tag", string="Tag")

    offers_ids = fields.One2many("estate.property.offer", "property_id", string="Offer")