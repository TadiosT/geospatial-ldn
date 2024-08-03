import logging

def setup_logger(name):
    logger = logging.getLogger(name)
    handler = logging.StreamHandler()
    logging_format = logging.Formatter("%(asctime)s - %(levelname)s - %(module)s - %(message)s")
    handler.setFormatter(logging_format)
    logger.setLevel(logging.DEBUG)
    logger.addHandler(handler)
    return logger
