from odoo import api,fields, models
from odoo.exceptions import UserError, ValidationError
from odoo.tools.float_utils import float_compare
from dateutil.relativedelta import relativedelta
import logging

_logger = logging.getLogger(__name__)

class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "tuto real estate property"
    _order = "id desc"

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
    buyer_id = fields.Many2one("res.partner", string="Buyer", copy=False)
    salesperson_id = fields.Many2one("res.users", string="Salesperson",default=lambda self: self.env.user)

    tags_ids = fields.Many2many("estate.property.tag", string="Tag")

    offers_ids = fields.One2many("estate.property.offer", "property_id", string="Offer")

    total_area = fields.Integer(string="Total area", compute="_compute_total_area")
    best_price = fields.Float(string="Best Offer", compute="_compute_best_price")

    _sql_constraints = [
        ('check_selling_price', 'CHECK(selling_price >= 0)', "The selling price should be positive."),
        ('check_expected_price', 'CHECK(expected_price >= 0)', "The expected price should be strictly positive."),
    ]

    @api.depends("garden_area","living_area")
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.garden_area + record.living_area

    @api.depends("offers_ids.price")
    def _compute_best_price(self):
        for record in self:
            prices = record.offers_ids.mapped('price')
        if prices:
            record.best_price = max(prices)
        else:
            record.best_price = 0.0

    @api.onchange("garden")
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = 'north'
        else:
            self.garden_area = 0
            self.garden_orientation = False

    def action_cancel_property(self):
        for record in self:
            record.state = 'cancelled'
        return True
    
    def action_mark_as_sold(self):
        _logger.warning("🚨 estate's action_mark_as_sold() CALLED")
        for record in self:
            if record.state == 'cancelled':
                raise UserError("Canceled properties cannot be sold.")
            else:
                record.state = 'sold'
        return True
    
    @api.constrains("expected_price","selling_price")
    def _check_selling_price(self):
        for record in self:
            if record.selling_price:
                if float_compare(record.selling_price, record.expected_price * 0.9, precision_digits=2) == -1 :
                    raise ValidationError("The selling price cannot be lower than 90 percent of the expected price.")
    
    @api.ondelete(at_uninstall=False)
    def _check_state_delete(self):
        for record in self:
            if record.state != 'new' and record.state != 'cancelled':
                raise ValidationError("Cannot delete a property with an offer or sold property.")