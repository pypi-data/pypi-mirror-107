"""python logging json formatter"""

__version__ = "0.0.1"

import json
import logging
import socket
import sys
from datetime import datetime
from typing import Any, Dict

if sys.version_info < (3, 0):
    EASY_TYPES = (basestring, bool, dict, float, int, list, tuple, type(None))
else:
    EASY_TYPES = (str, bool, dict, float, int, list, tuple, type(None))

# http://docs.python.org/library/logging.html#logrecord-attributes
SKIP_LOGRECORD_ATTRIBUTES = (
    'asctime', 'created', 'exc_info', 'exc_text', 'filename', 'args',
    'funcName', 'id', 'levelname', 'levelno', 'lineno', 'module', 'msg',
    'msecs', 'msecs', 'message', 'name', 'pathname', 'process',
    'processName', 'relativeCreated', 'thread', 'threadName', 'extra', "stack_info"
)


class JSONFormatter(logging.Formatter):
    def __init__(self, hostname=None, fqdn=False, indent: bool = False, *args, **kwargs) -> None:
        if hostname:
            self.hostname = hostname
        elif fqdn:
            self.hostname = socket.getfqdn()
        else:
            self.hostname = socket.gethostname()

        self.indent = indent
        super().__init__(*args, **kwargs)

    def format(self, record: logging.LogRecord) -> str:
        log_message = {
            "@timestamp": datetime.utcfromtimestamp(record.created).isoformat(sep=" ") + " +00:00",
            "app_host_name": self.hostname,
            "logger_name": record.name,
            "level": record.levelname,
            "pathname": record.pathname,
            "lineno": record.lineno,
            "func_name": record.funcName,
            "thread_id": record.thread,
            "thread_name": record.threadName,
            "process_id": record.process,
            "process_name": record.processName,
        }

        if isinstance(record.msg, dict):
            log_message["data"] = record.msg
        else:
            log_message["message"] = record.getMessage()

        # Add extra fields
        log_message.update(self.get_extra_fields(record=record))
        # If exception, add debug info
        if record.exc_info or record.exc_text:
            log_message['stack_trace'] = self.formatException(record.exc_info) if record.exc_info else record.exc_text

        if self.indent:
            return json.dumps(log_message, indent=1, ensure_ascii=False)
        return json.dumps(log_message, ensure_ascii=False)

    @staticmethod
    def get_extra_fields(record: logging.LogRecord) -> Dict[str, Any]:
        extra_fields = {}
        for k, v in record.__dict__.items():
            if k in SKIP_LOGRECORD_ATTRIBUTES:
                continue

            if isinstance(v, EASY_TYPES):
                extra_fields[k] = v
            elif isinstance(v, set):
                extra_fields[k] = list(v)
            elif isinstance(v, bytes):
                extra_fields[k] = v.decode()
            else:
                extra_fields[k] = repr(v.__dict__) if hasattr(v, "__dict__") else repr(v)

        return extra_fields