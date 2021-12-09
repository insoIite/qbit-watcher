"""
Logging definition module

opts = {
    "debug": True,
    "stream_handler": True,
    "file_handler": {
        "path": "/tmp/foo",
        "name": "foo.log"
    },
    'json_formatter': {
        'enabled': True,
        'extra_fields': {
            'foo': 'foo',
            'bar': 'bar'
        },
        'timestamp_fmt': "%Y-%m-%dT%H:%M:%S.%fZ"
    }
}
"""

import logging

from os import makedirs
from pathlib import Path

from colorlog import ColoredFormatter

from qbit_watcher.logger.exceptions import LogError
from qbit_watcher.logger.json_formatter import QbitJsonFormatter


class LastPartFilter(logging.Filter):
    # pylint: disable=too-few-public-methods
    """
    Logging filter adding a format record containing
    only the last part of the logger name
    """
    def filter(self, record):
        record.name_last = record.name.rsplit('.', 1)[-1]
        return True


def get_logger(name, opts=None):
    """
    Return a new named logger that will inherit the root logger
    """
    __init_main_logger(opts)
    return logging.getLogger('qbit_watcher.' + name)


def __init_main_logger(opts):
    """
    Init the main logger with its handlers when required
    """
    logger = logging.getLogger('qbit_watcher')
    logger.setLevel(logging.INFO)
    if not opts:
        return logger
    __valid_opts(opts)

    is_debug = opts['debug'] if "debug" in opts else False
    if is_debug:
        logger.setLevel(logging.DEBUG)

    stream_handler = opts['stream_handler'] if "stream_handler" in opts else False
    if stream_handler:
        json_opts = None
        if 'json_formatter' in opts:
            if opts.get('json_formatter', {}).get('enabled') is True:
                json_opts = opts['json_formatter']

        if logger.handlers:
            if not __has_handler(logger.handlers, logging.StreamHandler):
                handler = __create_stream_handler(json_opts=json_opts)
                logger.addHandler(handler)
        else:
            handler = __create_stream_handler(json_opts=json_opts)
            logger.addHandler(handler)

    file_handler = bool("file_handler" in opts)
    if file_handler:
        if logger.handlers:
            if not __has_handler(logger.handlers, logging.FileHandler):
                handler = __create_json_file_handler(
                    opts['file_handler']['path'],
                    opts['file_handler']['name']
                )
                logger.addHandler(handler)
        else:
            handler = __create_stream_handler(json_opts=json_opts)
            logger.addHandler(handler)

    return logger


def __valid_opts(opts):
    """
    Raise exception if opts is wrong
    """
    if 'file_handler' in opts:
        if not isinstance(opts['file_handler'], dict):
            raise LogError("file_handler must be a dict {path: '/tmp', file: 'file.log'}")
        if not 'path' in opts['file_handler'] or not 'name' in opts['file_handler']:
            raise LogError("file_handler is set in options but 'name' or 'path' are missing")


def __has_handler(handlers, handler_type):
    """
    Return whether there is a handler of handler_type type
    """
    res = False
    for handler in handlers:
        if isinstance(handler, handler_type):
            res = True
    return res


def __create_stream_handler(json_opts=None):
    """
    Create a stream logger with default formatter
    """
    stream_handler = logging.StreamHandler()
    if json_opts:
        extra = json_opts['extra_fields'] if 'extra_fields' in json_opts else {}
        ts_fmt = json_opts['timestamp_fmt'] if 'timestamp_fmt' in json_opts else None
        formatter = QbitJsonFormatter(extra, ts_fmt)
        stream_handler.setFormatter(formatter)
    else:
        last_filter = LastPartFilter()
        stream_handler.addFilter(last_filter)
        fmt_name = "  %(log_color)s%(name_last)-8s%(reset)s"
        fmt_levelname = "%(log_color)s%(levelname)s%(reset)s"
        fmt_message = "%(log_color)s%(message)s%(reset)s"

        stream_log_fmt = "  %s | %s | %s" % (fmt_name, fmt_levelname, fmt_message)
        stream_format = ColoredFormatter(stream_log_fmt)
        stream_handler.setFormatter(stream_format)

    return stream_handler


def __create_json_file_handler(folder_path, fname):
    """
    Create a json file logger
    """
    path = Path(folder_path)
    if not path.exists():
        makedirs(path, exist_ok=True)

    file_handler = logging.FileHandler(path / fname)
    json_format = logging.Formatter(
        '{"timestamp": "%(asctime)s", "level": "%(levelname)s", "short_message": "%(message)s"}',
        datefmt="%s"
    )
    file_handler.setFormatter(json_format)
    return file_handler
