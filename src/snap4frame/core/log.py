import logging
from logging.handlers import TimedRotatingFileHandler

LOGGER_NAME = "snap4frame"

logger = logging.getLogger(LOGGER_NAME)


def config_logger(logger: logging.Logger):
    logger.handlers.clear()

    formatter = logging.Formatter(
        "[%(asctime)s] %(name)s - %(levelname)s - %(message)s"
    )

    handler = TimedRotatingFileHandler(
        filename="snap4frame.log",
        when="D",
    )
    handler.setFormatter(formatter)

    logger.handlers.append(handler)


config_logger(logger)
logger.setLevel(logging.DEBUG)

# expose logging functions
debug = logger.debug
info = logger.info
warning = logger.warning
error = logger.error
critical = logger.critical
