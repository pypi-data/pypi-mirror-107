"""Handle .escaperc config file."""
import os
import json
from loguru import logger
from escape_cli.static.constants import ESCAPE_DIR, TRANSACTIONS_PATH, ENDPOINTS_PATH, METHODS_PATH
from escape_cli.patchs import patch_app


def get_config(config_filename, discover_namespace):
    """Get configuration to correctly patch the application."""
    if not os.path.isfile(config_filename):
        logger.error(
            f'Config file at path {config_filename} not found. Did you run `escape-py init`?'
            )
        return None
    with open(config_filename, 'r') as f:
        config = json.load(f)
        f.close()
        if not isinstance(config, dict
            ) or discover_namespace not in config.keys():
            logger.error(
                f'Config file at path {config_filename} has a wrong format. Did you run `escape-py init`?'
                )
            return None
        return config


def init_logs(escape_dir, transactions_path, endpoints_path, methods_path):
    """Reset the escape config directory where logs will be saved."""
    if not os.path.isdir(escape_dir):
        os.mkdir(escape_dir)
    with open(transactions_path, 'w+') as f:
        f.write('[')
        logger.success(f'Transactions have been reset: {transactions_path}')
    with open(endpoints_path, 'w+') as f:
        logger.success(f'Endpoints have been reset: {endpoints_path}')
    with open(methods_path, 'w+') as f:
        json.dump({}, f)
        logger.success(f'Methods have been reset: {methods_path}')


def close_json(char, file):
    """Properly end the json file."""

    def move_backward():
        """Move one char backward in the file."""
        fb.seek(-1, os.SEEK_END)
    with open(file, 'rb+') as fb:
        move_backward()
        if fb.read(1) == b',':
            move_backward()
            fb.truncate()
        fb.write(bytes(char, 'utf-8'))


def close_logs(transactions_path, endpoints_path):
    """Once completed format logs to make them readable."""
    close_json(']', transactions_path)
    with open(transactions_path, 'r') as f:
        transactions = json.load(f)
    try:
        with open(endpoints_path, 'r') as f:
            patterns = json.load(f)
    except json.JSONDecodeError as error:
        raise ValueError(
            'Unable to parse the endpoints. You may need to make at least one request to the API.'
            ) from error
    return transactions, patterns


def patch_and_run(entrypoint, config, as_module, manual=False):
    """Patch the app and run the entrypoint."""
    result = {}
    init_logs(ESCAPE_DIR, TRANSACTIONS_PATH, ENDPOINTS_PATH, METHODS_PATH)
    try:
        patch_app(config, entrypoint, as_module)
    except KeyboardInterrupt as error:
        if manual:
            logger.warning(
                "KeyboardInterrupt exception detected, but the flag `--manual` is enabled,  so we'll send results anyway."
                )
        else:
            raise error
    result['transactions'], result['endpoints'] = close_logs(TRANSACTIONS_PATH,
        ENDPOINTS_PATH)
    return result
