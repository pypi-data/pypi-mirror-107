"""Cover."""
import sys
import click
from loguru import logger
from escape_cli.static.constants import COVERAGE_NAMESPACE, DISCOVER_NAMESPACE
import escape_cli.utils.coverage as coverage
from escape_cli.utils.config import patch_and_run
from escape_cli.commands.common import extract_as_module, extract_config


@click.command()
@click.argument('entrypoint', nargs=-1, required=True, type=str)
@extract_config
@extract_as_module
@logger.catch
def cover(entrypoint, config, as_module):
    """ Discover routes on your application while running your tests and assess routes coverage. This will NOT send results to the Escape web application.



    

    Example: escape-py cover pytest

    Example: escape-py cover --config .escaperc.staging.json pytest

    """
    coverage_config = config[DISCOVER_NAMESPACE].get(COVERAGE_NAMESPACE, {})
    result = patch_and_run(' '.join(entrypoint), config, as_module)
    if not result:
        return
    coverage_data = coverage.run_coverage(result['transactions'], result[
        'endpoints'], coverage_config)
    filtered_coverage, coverage_stats, _ = coverage_data
    try:
        coverage.display_coverage_reports(filtered_coverage, coverage_stats,
            coverage_config)
    except ValueError as err:
        logger.error(err)
        sys.exit(1)
