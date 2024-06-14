import functools
import logging
import time

from django.db import connection, reset_queries

logger = logging.getLogger(__file__)


def timeit(method):
    def timed(*args, **kw):
        ts = time.time()
        result = method(*args, **kw)
        te = time.time()
        if "log_time" in kw:
            name = kw.get("log_name", method.__name__.upper())
            kw["log_time"][name] = int((te - ts) * 1000)
        else:
            logger.info(f"{method.__name__!r}  {(te - ts) * 1000:2.2f} ms")
        return result

    return timed


def query_debugger(func):
    @functools.wraps(func)
    def inner_func(*args, **kwargs):
        reset_queries()
        start_queries = len(connection.queries)
        start = time.perf_counter()
        result = func(*args, **kwargs)
        end = time.perf_counter()
        end_queries = len(connection.queries)
        logger.info(f"Function : {func.__name__}")
        logger.info(f"Number of Queries : {end_queries - start_queries}")
        logger.info(f"Finished in : {(end - start):.2f}s")
        function_name = f"Function : {func.__name__}"
        number_of_queries = f"Number of Queries : {end_queries - start_queries}"
        time_taken = f"Finished in : {(end - start):.2f}s"
        logger.error(function_name)
        logger.error(number_of_queries)
        logger.error(time_taken)
        return result

    return inner_func
