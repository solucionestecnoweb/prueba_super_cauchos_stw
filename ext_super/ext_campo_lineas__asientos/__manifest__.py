# -*- coding: utf-8 -*-
{
    'name': "Campos adicionales en LINEAS asientos",

    'summary': """Campos adicionales en lineas asientos""",

    'description': """
       Campos adicionales en lineas asientos 
       Colaborador: Ing. Darrell Sojo
    """,
    'version': '1.0',
    'author': 'INM&LDR Soluciones Tecnologicas',
    'category': 'Campos adicionales en flineas asientos super cauchos',

    # any module necessary for this one to work correctly
    'depends': ['product','account'],

    # always loaded
    'data': [
        'acccount_move_line_inherit.xml',
        #'view_add.xml',
        #'security/ir.model.access.csv',
    ],
    'application': True,
}
