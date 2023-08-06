"""Init."""
import json
import os.path
from pathlib import Path
from importlib import resources
import click
import inquirer
from loguru import logger
from escape_cli import static
from escape_cli.commands.common import config_option


@click.command()
@config_option
@logger.catch
def init(config_path):
    """Init Escape Python Instrumenter by creating escaperc file."""
    with resources.open_text(static, 'supported-libs.json') as f:
        supported_libs = json.load(f)
    project_questions = [inquirer.Text(name='key', message=
        'Please enter the Escape project key')]
    project_answers = inquirer.prompt(project_questions,
        raise_keyboard_interrupt=True)
    answers = {'project': project_answers}
    discover_questions = [inquirer.List(name='httpLib', choices=
        supported_libs['httpLib'].keys(), message=
        'What HTTP library do you use for this project?')]
    discover_answers = inquirer.prompt(discover_questions,
        raise_keyboard_interrupt=True)
    answers.update({'discover': discover_answers})
    logged_action = 'written'
    if os.path.isfile(config_path):
        with open(config_path) as f:
            existing_config = json.load(f)
            for key, val in existing_config.items():
                if key not in answers:
                    answers[key] = val
            logged_action = 'updated'
    with open(config_path, 'w') as f:
        json.dump(answers, f, indent=2)
        logger.success(
            f'Config file {logged_action}: {Path(config_path).resolve()}')
