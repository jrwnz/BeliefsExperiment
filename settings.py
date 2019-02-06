from os import environ

# if you set a property in SESSION_CONFIG_DEFAULTS, it will be inherited by all configs
# in SESSION_CONFIGS, except those that explicitly override it.
# the session config can be accessed from methods in your apps as self.session.config,
# e.g. self.session.config['participation_fee']

SESSION_CONFIG_DEFAULTS = {
    'real_world_currency_per_point': 1,
    'participation_fee': 10.00,
    'doc': "",
    'testing_if_yes': 'no',
    'write_test_data_if_yes': 'no',
    'load_test_data_if_yes': 'no',
    'time_limit': 15,
    'num_demo_participants': 2,
}

SESSION_CONFIGS = [    {
        'name': 'fullgame',
        'display_name': 'Full Game',
        'app_sequence': [
                        'matrix_training',
                        'actions_practice',
                        'actions',
                        'beliefs_practice',
                        'beliefs',
                        # 'undercutting_training',
                        # 'undercutting_practice',
                        # 'undercutting',
                        'payments'
                        ],                        
    },
                {
        'name': 'actions',
        'display_name': 'Actions',
        'app_sequence': ['actions'],
    },
                    {
        'name': 'actions_practice',
        'display_name': 'Actions Practice',
        'app_sequence': ['actions_practice'],
    },
            {
        'name': 'beliefs',
        'display_name': 'Beliefs',
        'app_sequence': ['beliefs'],
    },
                {
        'name': 'beliefs_practice',
        'display_name': 'Beliefs Practice',
        'app_sequence': ['beliefs_practice'],
    },
                {
        'name': 'undercutting',
        'display_name': 'Undercutting',
        'app_sequence': ['undercutting'],
    },
                {
        'name': 'undercutting_practice',
        'display_name': 'Undercutting Practice',
        'app_sequence': ['undercutting_practice'],
    },
                {
        'name': 'matrix_training',
        'display_name': 'Matrix Training',
        'num_demo_participants': 1,
        'app_sequence': ['matrix_training'],
    },
                    {
        'name': 'undercutting_training',
        'display_name': 'Undercutting Training',
        'num_demo_participants': 1,
        'app_sequence': ['undercutting_training'],
    },
            {
        'name': 'payments',
        'display_name': 'Payments',
        'num_demo_participants': 1,
        'app_sequence': ['payments'],
        'load_test_data_if_yes': 'yes',
    },
]

ROOMS = [{
        'name': 'gameroom',
        'display_name': 'Waitroom',
    }]


# ISO-639 code
# for example: de, fr, ja, ko, zh-hans
LANGUAGE_CODE = 'en'

# e.g. EUR, GBP, CNY, JPY
REAL_WORLD_CURRENCY_CODE = 'USD'
USE_POINTS = False

ADMIN_USERNAME = 'admin'
# for security, best to set admin password in an environment variable
ADMIN_PASSWORD = environ.get('OTREE_ADMIN_PASSWORD')

DEMO_PAGE_INTRO_HTML = """ """

SECRET_KEY = environ.get('SECRET_KEY')

# if an app is included in SESSION_CONFIGS, you don't need to list it here
INSTALLED_APPS = ['otree']
