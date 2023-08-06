"""Init."""
import click
from loguru import logger
import escape_scanner_wrapper


@click.command()
@click.argument('options', nargs=-1, required=False, type=str)
@logger.catch
def scan(options):
    """Start the scanner and pass the options."""
    escape_scanner_wrapper.execute(*options)
