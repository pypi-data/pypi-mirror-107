"""Parsing modules."""
import re
import json
from loguru import logger


def parse_parameters(raw_params):
    """Parse potential uuid values in parameters."""
    parameters = {}
    for key in raw_params:
        value = raw_params[key]
        if not isinstance(value, str):
            try:
                parameters[key] = str(value)
                continue
            except UnicodeDecodeError:
                logger.error(
                    f'Param in url cannot be converted into string: {key}: {value}'
                    )
        parameters[key] = value
    return parameters


def parse_body(raw_body, content_type):
    """Parse body into json when content_type is application/json."""
    if not content_type:
        return {}
    decoded_body = raw_body.decode('utf-8') if isinstance(raw_body, bytes
        ) else raw_body
    if 'application/json' in content_type:
        try:
            parsed_body = json.loads(decoded_body)
            return parsed_body
        except json.decoder.JSONDecodeError:
            return 'Invalid JSON: ' + decoded_body
    else:
        return decoded_body


def interpolate_openapi_path(raw_route, params):
    """Interpolate the raw_route to Open API path using the parameters in params."""
    openapi_path = raw_route
    for key, value in params.items():
        openapi_path = openapi_path.replace(value, f'{{{key}}}')
    openapi_path = f"/{openapi_path.strip('$^/')}"
    return openapi_path


def format_lib_to_openapi_path(raw_path):
    """Format the path parameters according to the Open API Spec."""
    param_patterns = ['\\^?\\(\\?P\\<[^>]+\\>[^)]*\\)', '\\<[^>]+\\>']
    openapi_path = raw_path
    for regex in param_patterns:
        for raw_param in re.findall(regex, openapi_path):
            param = re.findall('\\<(?:.+:)?([^>]+)\\>', raw_param)[0]
            openapi_path = openapi_path.replace(raw_param, '{' + param + '}')
    openapi_path = f"/{openapi_path.strip('$^/')}"
    return openapi_path


def find_params(path, regex=''):
    """Find name, type and pattern of params in path."""
    parameters = {}
    for raw_param in re.findall('\\<(.*?)\\>', path):
        splitted_params = raw_param.split(':')
        name = splitted_params[-1]
        new_param = {'name': name}
        if len(splitted_params) == 2:
            new_param['type'] = splitted_params[0]
        parameters[name] = new_param
    for name, pattern in re.findall('\\(\\?P<([^>]+)>([^)]+)\\)', regex):
        if name not in parameters.keys():
            parameters[name] = {'name': name}
        parameters[name]['pattern'] = pattern
    return list(parameters.values())


def get_identifier(method, openapi_path):
    """Format the identifier shared in common with the endpoints and the transactions."""
    method = method.lower()
    return f'{method.lower()}<>{openapi_path}'
