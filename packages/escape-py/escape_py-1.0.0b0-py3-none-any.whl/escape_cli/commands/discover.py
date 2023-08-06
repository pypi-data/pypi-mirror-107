"""Discovery."""
import sys
import traceback
import click
from loguru import logger
from termcolor import colored
import escape_cli.utils.coverage as coverage
from escape_cli.utils.sdk import EscapeIntelligenceSDK
from escape_cli.static.constants import COVERAGE_NAMESPACE, DISCOVER_NAMESPACE, PROJECT_NAMESPACE
from escape_cli.utils.config import patch_and_run
from escape_cli.commands.common import extract_as_module, extract_config


@click.command()
@click.argument('entrypoint', nargs=-1, required=True, type=str)
@click.option('--manual', is_flag=True)
@extract_config
@extract_as_module
@logger.catch
def discover(entrypoint, config, manual, as_module):
    """ Discover routes on your application while running your tests and assess coverage. This will send results to the Escape web application.



    

    Example: escape-py discover pytest

    Example: escape-py discover --config .escaperc.staging.json pytest

    """
    project_uri = config[PROJECT_NAMESPACE]['key']
    coverage_config = config[DISCOVER_NAMESPACE].get(COVERAGE_NAMESPACE, {})
    if manual:
        logger.warning('')
        logger.warning(colored('MANUAL MODE DETECTED', 'yellow', attrs=[
            'bold']))
        logger.warning(colored('Discovery results will be stored ',
            'yellow') + colored('regardless of the exit code', 'yellow',
            attrs=['bold']) + colored(
            ', including at keyboard interruption', 'yellow'))
        logger.warning(colored('To prevent this, ', 'yellow') + colored(
            'hit CTRL+C twice for exiting', 'yellow', attrs=['bold']) +
            colored(' or ', 'yellow') + colored(
            'run without the manual mode', 'yellow', attrs=['bold']))
        logger.warning('')
    logger.info('Creating run')
    client = EscapeIntelligenceSDK(project_uri)
    run = client.create_run('manual' if manual else 'automatic')
    logger.info(f"Run created with uuid {run['uuid']}")
    try:
        result = patch_and_run(' '.join(entrypoint), config, as_module, manual)
        if not result:
            return
        coverage_data = coverage.run_coverage(result['transactions'],
            result['endpoints'], coverage_config)
        filtered_coverage, coverage_stats, enriched_endpoints = coverage_data
        logger.info('Saving HTTP messages into the DB')
        client.add_transactions_to_run(run['uuid'], transactions=result[
            'transactions'])
        logger.info('Generating OpenAPI specification')
        client.generate_run_openapi_spec(run['uuid'])
        logger.info('Saving the endpoints in the DB')
        client.add_endpoints_to_run(run['uuid'], endpoints=enriched_endpoints)
        logger.info('Saving run metadata')
        client.update_run(run['uuid'], {'status': 'success:discovery', **
            coverage_stats})
        coverage.display_coverage_reports(filtered_coverage, coverage_stats,
            coverage_config)
        logger.success('Succesfully discovered routes on your application')
        logger.info(
            f"To proceed with scan, run `escape-scanner scan {run['uuid']}` in your project's folder"
            )
    except Exception as err:
        traceback.print_exc()
        logger.error(err)
        client.update_run(run['uuid'], {'status': 'failed:discovery'})
        sys.exit(1)
