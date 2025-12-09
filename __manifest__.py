{
    'name': 'Gestion des Visites',
    'version': '1.0.0',
    'category': 'Sales/Sales',
    'summary': 'Manage client visits and track sales results',
    'description': """
        Visit Management Module
        =======================
        * Plan and track client visits
        * Record visit results and sales
        * Generate visit reports
        * Manage clients and products
    """,
    'author': 'ENSAH GI3-GL',
    'website': 'https://www.ensah.ma',
    'license': 'LGPL-3',
    'depends': [
        'base',
        'product',
        'web',
        'mail',  # Pour le chatter et activités
    ],
    'data': [
        'security/groups.xml',
        'security/ir.model.access.csv',
        'data/sequence.xml',
        'data/visite_tag_data.xml',
        'views/visite_tag_views.xml',
        'views/client_view.xml',
        'views/visite_views.xml',
        'views/result_view.xml',
        'views/product_line.xml',
        'views/product_view.xml',
        'views/menu.xml',
        'report/visite_report.xml',
        'report/visite_report_template.xml',
    ],
    'sequence': 1,
    'installable': True,
    'application': True,
    'auto_install': False,
}

