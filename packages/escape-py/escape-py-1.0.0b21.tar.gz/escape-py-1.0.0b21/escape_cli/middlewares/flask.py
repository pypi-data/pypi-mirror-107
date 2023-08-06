"""Main."""
import json
from flask import request, Response, Flask
from loguru import logger
from escape_cli.utils.result import save_transaction
from escape_cli.utils.parse import find_params, parse_parameters, format_lib_to_openapi_path, get_identifier
from escape_cli.static.constants import ENDPOINTS_PATH


def decode_res_body(response):
    """Decode the body response."""
    res_body = {}
    if response.is_json:
        res_body = cast(dict, response.get_json())
    else:
        try:
            res_body = cast(str, response.data.decode('utf-8'))
        except UnicodeDecodeError:
            logger.warning('Enable to decode the body. It is set to empty.')
    return res_body


def flask_middleware(app):
    """Add a middleware called after each request."""

    @app.before_first_request
    def detect_routes():
        """Detect registered routes."""
        endpoints = []
        existing_routes = []
        for rule in app.url_map.iter_rules():
            lib_path = str(rule)
            handler = rule.endpoint
            parameters = find_params(lib_path)
            openapi_path = format_lib_to_openapi_path(lib_path)
            if openapi_path not in existing_routes:
                existing_routes.append(openapi_path)
                for method in (rule.methods - {'HEAD', 'OPTIONS'}):
                    endpoints.append({'openApiPath': openapi_path, 'method':
                        method, 'parameters': parameters, 'handler':
                        handler, '_identifier': get_identifier(method,
                        openapi_path)})
        with open(ENDPOINTS_PATH, 'w') as f:
            json.dump(endpoints, f)

    @app.after_request
    def detect_transaction(response):
        """Detect transactions."""
        save_req_and_res_information(response)
        return response


def save_req_and_res_information(response):
    """Fetch usefull information from requests and responses Save it in the transactions file."""
    response.direct_passthrough = False
    req_parameters = parse_parameters(request.view_args
        ) if request.view_args else {}
    openapi_path = format_lib_to_openapi_path(str(request.url_rule))
    result = {'req': {'openApiPath': openapi_path, 'protocol': request.
        scheme, 'host': request.host, 'route': request.path, 'method':
        request.method, 'parameters': req_parameters, 'query': dict(request
        .args), 'originalUrl': request.path, 'headers': dict(request.
        headers), 'cookies': dict(request.cookies), 'httpVersion': '',
        'body': dict(request.form)}, 'res': {'statusCode': response.
        status_code, 'messageCode': response.status.split(' ')[1],
        'headers': dict(response.headers), 'body': decode_res_body(response
        )}, '_identifier': get_identifier(request.method, openapi_path)}
    save_transaction(result)
