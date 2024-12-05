import logging
from datetime import datetime
from logging.handlers import RotatingFileHandler

from pythonjsonlogger import jsonlogger

DEFAULT_MAX_BYTES = 10000000
DEFAULT_BACKUP_COUNT = 5
LOG_FORMAT = "%Y-%m-%d %H:%M:%S,%f"


class CustomJsonFormatter(jsonlogger.JsonFormatter):
    def add_fields(self, log_record, record, message_dict):
        super(CustomJsonFormatter, self).add_fields(log_record, record, message_dict)

        if not log_record.get("timestamp"):
            log_record["timestamp"] = datetime.now().strftime(LOG_FORMAT)

        if log_record.get("level"):
            log_record["level"] = log_record["level"].upper()
        else:
            log_record["level"] = record.levelname

        log_record["project"] = "codemonkey"


def setup_logger():
    logging.basicConfig(level=logging.DEBUG, datefmt=LOG_FORMAT)
    logger = logging.getLogger("labs")
    logger.propagate = False

    log_format = "[%(asctime)s][%(levelname)s][%(name)s]: %(message)s"
    formatter = logging.Formatter(fmt=log_format, datefmt=LOG_FORMAT)
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)

    try:
        formatter = CustomJsonFormatter()
        handler = RotatingFileHandler(
            "logs/debug.log",
            maxBytes=DEFAULT_MAX_BYTES,
            backupCount=DEFAULT_BACKUP_COUNT,
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    except Exception:
        pass
