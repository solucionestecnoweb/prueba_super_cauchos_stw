# Copyright 2020 GregorioCode <Info@gregoriocode.com>


{
    "name": "Purchase Imports Extend",
    "version": "13.0.1.0.1",
    "author": "Ing Gregorio Blanco",
    "website": "https://gregoriocode.com",
    "license": "AGPL-3",
    "depends": ['base', 'purchase'],
    "data": [
        "security/ir.model.access.csv",
        "views/purchase_order_imports_menu_items.xml",
        "views/purchase_order_imports.xml",
        "views/purchase_order_line_imports.xml",
        "views/purchase_order_imports_shipping.xml",
        # "views/purchase_order_importations.xml",
        # "views/purchase_order_importations_containers.xml",
    ],
    'installable': True,
}
