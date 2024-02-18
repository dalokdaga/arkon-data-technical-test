import logging
from logging.handlers import RotatingFileHandler


def setup_logging():
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    log_file = 'storage/app.log'
    handler = RotatingFileHandler(log_file, maxBytes=1024 * 1024, backupCount=5)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    return logger
