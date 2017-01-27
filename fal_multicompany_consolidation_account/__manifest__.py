{
    "name": "ACC-34_Multi Company Consolidation Account",
    "version": "1.0",
    'author': 'Falinwa Hans',
    "description": """
    Module to display am consolidation account for multi company
    """,
    "depends" : ['base', 'account', 'analytic'],
    'init_xml': [],
    'update_xml': [
        'views/account_view.xml',
    ],
    'css': [],
    'js' : [],
    'installable': True,
    'active': False,
    'application' : False,
}