import time
import functools
import logging


def create_logger(logger_name, log_fpath):
    """
    Creates a logging object and returns it
    """
    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.INFO)

    fh = logging.FileHandler(log_fpath)

    fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    formatter = logging.Formatter(fmt)
    fh.setFormatter(formatter)

    logger.addHandler(fh)
    return logger


def exception(function):
    """
    A decorator that wraps the passed in function and logs
    exceptions should one occur
    """
    @functools.wraps(function)
    def wrapper(*args, **kwargs):
        logger = create_logger("exception_logger", "logs/test.log")
        try:
            return function(*args, **kwargs)
        except:
            err = "There was an exception in  "
            err += function.__name__
            logger.exception(err)
            raise
    return wrapper


def function_timer(function):
    """
    A decorator that wraps the passed in function and times
    its runtime
    """
    @functools.wraps(function)
    def wrapper(*args, **kwargs):
        logger = create_logger("time_logger", "logs/time_profile.log")
        start = time.time()
        ret = function(*args, **kwargs)
        end = time.time()
        msg = '%s function took %0.3f ms' % (function.func_name, (end - start) * 1000.0)
        logger.info(msg)
        return ret

    return wrapper
