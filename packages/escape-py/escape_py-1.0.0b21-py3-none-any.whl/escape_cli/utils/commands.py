"""Options shared between the commands."""
from os.path import isfile
from functools import wraps
import click
from escape_cli.static.constants import DISCOVER_NAMESPACE
from escape_cli.utils.config import get_config
from escape_cli.static.command_options import OPTION_DICTIONNARY


def extract_config(func):
    """Extract the config given the config path."""

    @wraps(func)
    def wrapped(*args, **kwargs):
        config_path = kwargs['config_path']
        config = get_config(config_path, DISCOVER_NAMESPACE)
        if not config:
            raise ValueError(
                f'Cannot read the config in the file {config_path}')
        del kwargs['config_path']
        kwargs['config'] = config
        return func(*args, **kwargs)
    return wrapped


def extract_as_module(func):
    """Check if the entrypoint correspond to a file in the cwd."""

    @wraps(func)
    def wrapped(*args, **kwargs):
        kwargs['as_module'] = not isfile(kwargs['entrypoint'][0].split(' ')[0])
        return func(*args, **kwargs)
    return wrapped


def add_options(func):
    """Add click options."""

    def add_option(func, command_option):
        """Add click option."""
        return click.option(*command_option['options'], command_option[
            'name'], default=command_option.get('default'), help=
            command_option.get('default', ''), is_flag=command_option.get(
            'is_flag'))(func)
    command_options = OPTION_DICTIONNARY[func.__name__]
    func_with_options = func
    for option in command_options:
        func_with_options = add_option(func_with_options, option)
    return func_with_options


def parse_command(argv):
    """Separate the options from the escape command and the app entrypoint."""
    command = argv[1]
    index = 2
    for option in OPTION_DICTIONNARY[command]:
        index += 1 if option.get('is_flag') else 2
    return argv[1:index] + [' '.join(argv[index:])]
