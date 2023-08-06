"""Exec Python file in controlled environment.



Credits: Codecov

https://github.com/nedbat/coveragepy

"""
import os
import sys
import inspect
import platform
from types import ModuleType
from importlib import machinery
from importlib.util import find_spec
from multiprocessing import Process, set_start_method
from loguru import logger
from coverage.execfile import make_code_from_py, make_code_from_pyc


class DummyLoader:
    """A shim for the pep302 __loader__, emulating pkgutil.ImpLoader.



    Currently only implements the .fullname attribute

    """

    def __init__(self, fullname, *_args):
        self.fullname = fullname


class NoSource(Exception):
    """We couldn't find the source for a module."""


def find_module(modulename):
    """Find the module named `modulename`.



    Returns the file path of the module, the name of the enclosing package, and the spec.

    """
    try:
        spec = find_spec(modulename)
    except ImportError as err:
        raise NoSource(str(err)) from err
    if not spec:
        raise NoSource(f'No module named {modulename}')
    origin = spec.origin
    packagename = spec.name
    if spec.submodule_search_locations:
        mod_main = modulename + '.__main__'
        spec = find_spec(mod_main)
        if not spec:
            raise NoSource(
                f'No module named {mod_main}; {modulename} is a package and cannot be directly executed'
                )
        origin = spec.origin
        packagename = spec.name
    packagename = packagename.rpartition('.')[0]
    pathname = str(origin)
    return pathname, packagename, spec


def set_sys_path(args, as_module):
    """Set sys.path properly.



    This needs to happen before any importing, and without importing anything.

    """
    cpython = platform.python_implementation() == 'CPython'
    pyversion = sys.version_info + (int(platform.python_version()[-1] == '+'),)
    actual_syspath0_dash_m = cpython and pyversion >= (3, 7, 0, 'beta', 3)
    if as_module:
        if actual_syspath0_dash_m:
            path0 = os.getcwd()
        else:
            path0 = ''
    elif os.path.isdir(args[0]):
        path0 = args[0]
    else:
        path0 = os.path.abspath(os.path.dirname(args[0]))
    if os.path.isdir(sys.path[0]):
        top_file = inspect.stack()[-1][0].f_code.co_filename
        sys_path_0_abs = os.path.abspath(sys.path[0])
        top_file_dir_abs = os.path.abspath(os.path.dirname(top_file))
        if sys_path_0_abs != top_file_dir_abs:
            path0 = ''
    elif sys.path[1] == os.path.dirname(sys.path[0]):
        del sys.path[1]
    if path0:
        sys.path[0] = os.path.abspath(path0)


def prepare(args, as_module):
    """Do more preparation to run Python code.



    Includes finding the module to run and adjusting sys.argv[0]. This method is allowed to import code.

    """
    package = ''
    spec = None
    if as_module:
        modulename = args[0]
        pathname, package, spec = find_module(modulename)
        if spec:
            modulename = spec.name
        loader = DummyLoader(modulename)
        args[0] = os.path.abspath(pathname)
    elif os.path.isdir(args[0]):
        for ext in ['.py', '.pyc', '.pyo']:
            try_filename = os.path.join(args[0], '__main__' + ext)
            if os.path.exists(try_filename):
                args[0] = try_filename
                break
        else:
            raise NoSource(f'Can\'t find "__main__" module in "{args[0]}"')
        try_filename = os.path.abspath(args[0])
        spec = machinery.ModuleSpec('__main__', None, origin=try_filename)
        spec.has_location = True
        loader = DummyLoader('__main__')
    else:
        loader = DummyLoader('__main__')
    args[0] = os.path.abspath(args[0])
    return args, package, spec, loader


def execute(entrypoint, as_module):
    """The `entrypoint` is the entrypoint to be executed in python (with parameters)"""
    args = entrypoint.split()
    set_sys_path(args, as_module)
    args, package, spec, loader = prepare(args, as_module)
    env_mod = ModuleType('__main__')
    env_mod.__loader__ = loader
    env_mod.__file__ = args[0]
    from_pyc = args[0].endswith(('.pyc', '.pyo'))
    if from_pyc:
        env_mod.__file__ = env_mod.__file__[:-1]
    if package:
        env_mod.__package__ = package
    if spec:
        env_mod.__spec__ = spec
    if from_pyc:
        code = make_code_from_pyc(args[0])
    else:
        code = make_code_from_py(args[0])
    os.getcwd()
    sys.argv = args
    sys.modules['__main__'] = env_mod
    set_start_method('fork')
    execution = Process(target=exec, args=(code, env_mod.__dict__))
    execution.start()
    execution.join()
    if execution.exitcode:
        raise Exception(
            f'Unit test failed with exit code : {execution.exitcode}')
    logger.success('Unit tests succeeded')
