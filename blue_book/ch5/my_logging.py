import logging.config

import settings


def get_my_logger(name):
    logging.config.dictConfig(settings.LOGGING_CONF)
    return logging.getLogger(name)


logger = get_my_logger(__name__)


if __name__ == "__main__":
    logger.debug("DEBUG level")
    logger.info("INFO level")
    logger.warning("WARNING level")
    logger.error("ERROR level")
    logger.critical("CRITICAL level")
