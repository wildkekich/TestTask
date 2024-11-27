import logging
import os
from functools import wraps

BASE_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "other")
LOG_PATH = os.path.join(BASE_PATH, "logs")
os.makedirs(LOG_PATH, exist_ok=True)

for handler in logging.root.handlers:
    logging.root.removeHandler(handler)

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

console_logger = logging.getLogger("console_logger")
console_logger.setLevel(logging.DEBUG)
console_handler = logging.FileHandler(os.path.join(LOG_PATH, "console-logfile.log"))
console_handler.setFormatter(formatter)
console_logger.addHandler(console_handler)

db_logger = logging.getLogger("db_logger")
db_logger.setLevel(logging.DEBUG)
db_handler = logging.FileHandler(os.path.join(LOG_PATH, "db-logfile.log"))
db_handler.setFormatter(formatter)
db_logger.addHandler(db_handler)


def console_logger_wrap(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        console_logger.info(f"Executing {func.__name__} with arguments {args} and {kwargs}")
        result = func(*args, **kwargs)
        console_logger.info(f"Result of {func.__name__}: {result}")
        return result
    return wrapper


def db_logger_wrap(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        db_logger.info(f"Executing {func.__name__} with arguments {args} and {kwargs}")
        result = func(*args, **kwargs)
        db_logger.info(f"Result of {func.__name__}: {result}")
        return result
    return wrapper
