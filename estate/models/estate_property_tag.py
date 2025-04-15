from odoo import fields,models

class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "used to describe property"
    _order = "name"

    name = fields.Char(string="Tag", required=True)
    color = fields.Integer(string="Color")

    _sql_constraints = [
        ('unique_name','UNIQUE(name)', "The tag name must be unique.")
    ]