from odoo import fields,models,api

class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "type of the property (apartment, house, etc.)"
    _order = "sequence, name"

    name = fields.Char(string='Property Type', required=True)
    sequence = fields.Integer("Sequence", default=1)

    property_ids = fields.One2many("estate.property","property_type_id",string="Properties")

    _sql_constraints = [
        ('unique_type_name','UNIQUE(name)', "The type name must be unique.")
    ]

    offer_ids = fields.One2many("estate.property.offer","property_type_id",string="Offers")

    offer_count = fields.Integer(string="Number of offers", compute="_compute_offer_count")

    @api.depends("offer_ids")
    def _compute_offer_count(self):
        for record in self:
            record.offer_count = len(record.offer_ids)