"""Python environment module for Flask."""
import flask
from escape_cli.executor import execute
from escape_cli.middlewares import flask_middleware


def flask_patch(entrypoint, as_module):
    """The `filename` is the file entrypoint executed in the controlled Python environment."""


    class NewClass(flask.Flask):
        """Patched Flask class."""

        def __init__(self, *args, **kwargs):
            """Overriden constructor."""
            super().__init__(*args, **kwargs)
            flask_middleware(self)
    flask.Flask = NewClass
    execute(entrypoint, as_module)
