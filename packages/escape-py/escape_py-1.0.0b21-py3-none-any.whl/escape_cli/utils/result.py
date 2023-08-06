"""Utils to save patching results."""
import json
from loguru import logger
from escape_cli.static.constants import TRANSACTIONS_PATH


def save_transaction(result):
    """Save request and response informations in the transactions file."""
    for key in ['req', 'res', '_identifier']:
        if key not in result.keys():
            logger.warning(f'\n{key} is not in the result')
            return
    with open(TRANSACTIONS_PATH, 'a') as f:
        f.write(f'{json.dumps(dict(result))},')
