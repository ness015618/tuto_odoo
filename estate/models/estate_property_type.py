from odoo import fields,models

class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "type of the property (apartment, house, etc.)"

    name = fields.Char(string='Property Type', required=True)

    property_ids = fields.One2many("estate.property","property_type_id",string="Properties")

    _sql_constraints = [
        ('unique_type_name','UNIQUE(name)', "The type name must be unique.")
    ]