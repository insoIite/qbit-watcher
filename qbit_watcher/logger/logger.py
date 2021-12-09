"""
Logging definition module
"""

import logging
import logging.handlers
import sys

from pathlib import Path

from colorlog import ColoredFormatter

from qbit_watcher.settings import APP_LOGFILE
from qbit_watcher.logger.exceptions import LogError


class LastPartFilter(logging.Filter):
    # pylint: disable=too-few-public-methods
    """
    Logging filter adding a format record containing
    only the last part of the logger name
    """
    def filter(self, record):
        record.name_last = record.name.rsplit('.', 1)[-1]
        return True


def get_logger(name):
    """
    Return a new named logger that will inherit the root logger
    """
    __init_main_logger()
    return logging.getLogger('qbit_watcher.' + name)


def __init_main_logger():
    """
    Init the main logger with its handlers when required
    """
    logger = logging.getLogger('qbit_watcher')
    logger.setLevel(logging.INFO)

    if sys.stdout.isatty() and sys.stderr.isatty():
        stream_handler = __create_stream_handler()
        logger.addHandler(stream_handler)

    if logger.handlers:
        if not __has_handler(logger.handlers, logging.StreamHandler):
            if sys.stdout.isatty() and sys.stderr.isatty():
                handler = __create_stream_handler()
                logger.addHandler(handler)
        if not __has_handler(logger.handlers, logging.FileHandler):
            handler = __create_file_handler()
            logger.addHandler(handler)
    else:
        if sys.stdout.isatty() and sys.stderr.isatty():
            handler = __create_stream_handler()
            logger.addHandler(handler)
        fhandler = __create_file_handler()
        logger.addHandler(fhandler)
    return logger


def __valid_opts(opts):
    """
    Raise exception if opts is wrong
    """
    if 'file_handler' in opts:
        if not isinstance(opts['file_handler'], dict):
            raise LogError("file_handler must be a dict {path: '/tmp', file: 'file.log'}")
        if 'path' not in opts['file_handler'] or 'name' not in opts['file_handler']:
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


def __create_stream_handler():
    """
    Create a stream logger with default formatter
    """
    stream_handler = logging.StreamHandler()
    last_filter = LastPartFilter()
    stream_handler.addFilter(last_filter)
    fmt_name = "  %(log_color)s%(name_last)-8s%(reset)s"
    fmt_levelname = "%(log_color)s%(levelname)s%(reset)s"
    fmt_message = "%(log_color)s%(message)s%(reset)s"

    stream_log_fmt = "  %s | %s | %s" % (fmt_name, fmt_levelname, fmt_message)
    stream_format = ColoredFormatter(stream_log_fmt)
    stream_handler.setFormatter(stream_format)
    return stream_handler


def __create_file_handler():
    """ Add filehandler
    """
    last_filter = LastPartFilter()
    fmt_date = "  %(asctime)s"
    fmt_name = "%(name_last)-8s"
    fmt_levelname = "%(levelname)s"
    fmt_message = "%(message)s"

    file_log_fmt = "%s  %s | %s | %s" % (fmt_date, fmt_name, fmt_levelname, fmt_message)
    if not APP_LOGFILE.parent.exists():
        Path.mkdir(APP_LOGFILE.parent, exist_ok=True)
    file_handler = logging.handlers.RotatingFileHandler(
        APP_LOGFILE,
        maxBytes=(1048576 * 5),
        backupCount=7
    )

    file_handler.addFilter(last_filter)
    file_handler.setFormatter(logging.Formatter(file_log_fmt))
    return file_handler
