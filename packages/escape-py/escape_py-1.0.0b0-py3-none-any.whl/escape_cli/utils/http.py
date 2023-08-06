"""Utils to manipulate HTTP Requests."""
import datetime
from loguru import logger
from simplejson import dumps


def parse_dates(dct, date_format='%Y-%m-%dT%H:%M:%S.%fZ'):
    """Parses string dates of a `dict` to a Python datetime `date_format`."""
    for key, value in dct.items():
        if isinstance(value, str) and value.endswith('Z'):
            try:
                dct[key] = datetime.datetime.strptime(value, date_format)
            except ValueError as e:
                logger.warning(f'Coul not parse date "{value}": {e}')
    return dct


def serialize_dates(obj):
    """Serializes dates in `obj` to backend-readable date strings."""
    if isinstance(obj, (datetime.datetime, datetime.date)):
        return obj.isoformat()
    raise TypeError('Type %s is not serializable' % type(obj))


def prepare_request_data(data):
    """Clean `data` dictionnary and format it for to send with Python `requests` module.



    Python dicts might contains some non-json-serializable data such as NaNs which we must remove before sending to backend.

    """
    if isinstance(data, dict):
        data = {k: data[k] for k in data if not isinstance(k, (int, float))}
        data = dumps(data, default=serialize_dates, ignore_nan=True)
    return data.replace('\\u0000', '')
