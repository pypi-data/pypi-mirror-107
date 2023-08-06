"""Python environment module for Django."""
import os
import json
import importlib
from copy import deepcopy
import django
import django.views.decorators.http
from loguru import logger
from escape_cli.executor import execute
from escape_cli.static import METHODS_PATH


def _patch_transactions():
    """Patch to hijack transactions in the middleware."""
    original_fn = deepcopy(importlib.import_module)

    def new_fn(*args, **kwargs):
        res = original_fn(*args, **kwargs)
        for arg in args:
            if 'settings' in arg:
                logger.success(f'Patching file: {arg}')
                res.MIDDLEWARE += (
                    'escape_cli.middlewares.django.GetRequestAndResponseInformation'
                    ,)
        return res
    importlib.import_module = new_fn


def _patch_child_decorators(patched_fn, hijacked_methods):
    """Patch child decorators in django.views.decorators.http, in particuliar @require_POST, @require_GET and @require_safe."""
    original_fn = deepcopy(patched_fn)

    def new_fn(*args, **kwargs):
        with open(METHODS_PATH) as f:
            methods_dicts = json.load(f)
        for arg in args:
            methods_dicts[f'{arg.__module__}.{arg.__name__}'
                ] = hijacked_methods
        with open(METHODS_PATH, 'w+') as f:
            json.dump(methods_dicts, f)
        res = original_fn(*args, **kwargs)
        return res
    return new_fn


def _patch_parent_decorator():
    """Patch django.views.decorators.http.require_http_methods, which is the parent decorator of all @require_X decorators."""
    original_fn = deepcopy(django.views.decorators.http.require_http_methods)

    def new_fn(*args, **kwargs):
        res = original_fn(*args, **kwargs)
        res = _patch_child_decorators(res, *args)
        return res
    django.views.decorators.http.require_http_methods = new_fn


def django_patch(entrypoint, as_module):
    """The `filename` is the file entrypoint executed in the controlled Python environment."""
    _patch_transactions()
    _patch_parent_decorator()
    django.views.decorators.http.require_POST = _patch_child_decorators(django
        .views.decorators.http.require_POST, ['POST'])
    django.views.decorators.http.require_GET = _patch_child_decorators(django
        .views.decorators.http.require_GET, ['GET'])
    django.views.decorators.http.require_safe = _patch_child_decorators(django
        .views.decorators.http.require_GET, ['GET', 'HEAD'])
    os.environ['ESCAPE_ENDPOINTS_MAPPED'] = 'False'
    execute(entrypoint, as_module)
