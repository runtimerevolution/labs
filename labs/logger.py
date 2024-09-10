from datetime import datetime, timezone
import logging
from logging.handlers import RotatingFileHandler
from pythonjsonlogger import jsonlogger


DEFAULT_MAX_BYTES = 10000
DEFAULT_BACKUP_COUNT = 5
LOG_FORMAT = "%Y-%m-%d %H:%M:%S"


class CustomJsonFormatter(jsonlogger.JsonFormatter):
    def add_fields(self, log_record, record, message_dict):
        super(CustomJsonFormatter, self).add_fields(log_record, record, message_dict)

        if not log_record.get("timestamp"):
            log_record["timestamp"] = datetime.now(timezone.utc).strftime(LOG_FORMAT)

        if log_record.get("level"):
            log_record["level"] = log_record["level"].upper()
        else:
            log_record["level"] = record.levelname

def setup_logger_rotating_file_handler(logger: logging.Logger, log_file, level, max_bytes=DEFAULT_MAX_BYTES, backup_count=DEFAULT_BACKUP_COUNT):
    formatter = CustomJsonFormatter("[%(timestamp)s][%(level)s][%(name)s]: %(message)s")

    handler = RotatingFileHandler(log_file, maxBytes=max_bytes, backupCount=backup_count)
    handler.setFormatter(formatter)
    handler.setLevel(level)

    logger.addHandler(handler)

    return handler

def setup_logger():
    logging.basicConfig(level=logging.DEBUG, datefmt=LOG_FORMAT)
    logger = logging.getLogger(__name__)
    logger.propagate = False

    logformat = "[%(asctime)s][%(levelname)s][%(name)s]: %(message)s"                 
    formatter = logging.Formatter(fmt=logformat, datefmt=LOG_FORMAT)

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)

    setup_logger_rotating_file_handler(logger, "debug.log", logging.DEBUG)
  
