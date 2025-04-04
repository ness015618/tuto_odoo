from odoo import fields,models

class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "used to describe property"

    name = fields.Char(string="Tag", required=True)