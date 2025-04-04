from odoo import fields,models

class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "offer made by a potential buyer"

    price = fields.Float(string="Price")
    status = fields.Selection(
        string="Status",
        copy=False,
        selection=[('accepted','Accepted'),('refused','Refused')])
    partner_id = fields.Many2one("res.partner", string="Partner", required=True)
    property_id = fields.Many2one("estate.property", required=True)