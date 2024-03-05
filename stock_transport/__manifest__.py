{
    'name': 'Stock Transport',
    'version': '1.0',
    'description':"""This is stock transport module""",
    'author':'Tushar Agrawal',
    'depends':['stock_picking_batch', 'fleet'],
    'data' : [
        'security/ir.model.access.csv',
        
        'views/fleet_category_view.xml',
        'views/batch_picking_view.xml',
        'views/batch_picking_volume.xml',
    ],
    'installable': True,
    'application': True,
}
