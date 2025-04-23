{
    'name' : 'estate',
    'depends' : [
        'base_setup'
    ],
    'application' : True,
    'data' : [
        'security/ir.model.access.csv',
        'views/estate_property_views.xml',
        'views/estate_property_offers_views.xml',
        'views/estate_property_types_views.xml',
        'views/estate_property_tags_views.xml',
        'views/estate_menus.xml'
    ]
}