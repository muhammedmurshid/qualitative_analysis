{
    'name': "Ratings",
    'version': "14.0.1.0",
    'sequence': "0",
    'depends': ['base', 'mail'],
    'data': [
        'security/groups.xml',
        'security/ir.model.access.csv',
        'security/record_rule.xml',
        'views/quality.xml',
        'views/attributes.xml',
        'views/quantitative_analysis.xml',
        'views/quantitative_attrs.xml',
    ],
    'demo': [],
    'summary': "logic_qualitataive_analysis",
    'description': "this_is_my_app",
    'installable': True,
    'auto_install': False,
    'license': "LGPL-3",
    'application': False
}
