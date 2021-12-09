"""
Definition of a custom json formatter

{'level' : <level>, 'timestamp': <timestamp>}

are added by default
"""
from datetime import datetime

from pythonjsonlogger import jsonlogger


class QbitJsonFormatter(jsonlogger.JsonFormatter):
    """
    JsonFormatter
    """
    def __init__(self, extra=None, ts_fmt=None):
        super().__init__()
        self.extra = extra if extra else {}
        self.ts_fmt = '%Y-%m-%dT%H:%M:%S.%fZ'
        if ts_fmt:
            self.ts_fmt = ts_fmt

    def add_fields(self, log_record, record, message_dict):
        # Call of super will add the {'message': ...} dict
        super().add_fields(log_record, record, message_dict)
        # Let's add the extra dict attribute in the json log
        for key, value in self.extra.items():
            if not log_record.get(key):
                log_record[key] = value

        if not log_record.get('timestamp'):
            # this doesn't use record.created, so it is slightly off
            now = datetime.utcnow().strftime(self.ts_fmt)
            log_record['timestamp'] = now

        if log_record.get('level'):
            log_record['level'] = log_record['level']
        else:
            log_record['level'] = record.levelname
