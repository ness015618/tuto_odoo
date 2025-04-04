from odoo import fields,models

class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "type of the property (apartment, house, etc.)"

    name = fields.Char(string='Property Type', required=True)
