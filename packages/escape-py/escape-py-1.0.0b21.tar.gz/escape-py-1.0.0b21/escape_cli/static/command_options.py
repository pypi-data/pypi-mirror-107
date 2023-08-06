"""Options shared between the commands."""
from escape_cli.static.constants import CONFIG_FILENAME
config_option = {'name': 'config_path', 'options': ['-c', '--config'],
    'default': CONFIG_FILENAME, 'help': 'Path of the escape config file.'}
manual_option = {'name': 'manual', 'options': ['--manual'], 'is_flag': True}
OPTION_DICTIONNARY = {'init': [config_option], 'cover': [config_option],
    'discover': [config_option, manual_option], 'scan': [config_option]}
