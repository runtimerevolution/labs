import datetime
import logging
import time
from functools import wraps


def async_time_and_log_function(f):
    @wraps(f)
    async def wrapper(*args, **kwargs):
        logger = logging.getLogger(__name__)
        logger.debug(
            f"Running {f.__name__}{args} {kwargs} at {datetime.datetime.now()}."
        )

        start_time = time.perf_counter()

        result = await f(*args, **kwargs)

        end_time = time.perf_counter()
        total_time = end_time - start_time
        logger.debug(
            f"Finished {f.__name__}{args} {kwargs} at {datetime.datetime.now()}. Took {total_time:.4f} seconds."
        )

        return result

    return wrapper


def time_and_log_function(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        logger = logging.getLogger(__name__)
        logger.debug(
            f"Running {f.__name__}{args} {kwargs} at {datetime.datetime.now()}."
        )

        start_time = time.perf_counter()

        result = f(*args, **kwargs)

        end_time = time.perf_counter()
        total_time = end_time - start_time
        logger.debug(
            f"Finished {f.__name__}{args} {kwargs} at {datetime.datetime.now()}. Took {total_time:.4f} seconds."
        )

        return result

    return wrapper
