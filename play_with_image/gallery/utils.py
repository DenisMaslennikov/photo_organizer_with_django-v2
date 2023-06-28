import logging
from logging.handlers import RotatingFileHandler

from django.conf import settings

logger = logging.getLogger(__package__)
logger.setLevel(settings.LOG_LEVEL)
file_handler = RotatingFileHandler(
    settings.LOG_DIR / f'{__package__}.log',
    maxBytes=settings.LOG_MAX_SIZE,
    backupCount=settings.LOG_BACKUP_COUNT,
)
stream_handler = logging.StreamHandler()
formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(filename)s - %(levelname)s - %(funcName)s - '
    '%(lineno)d - %(message)s'
)
file_handler.setFormatter(formatter)
stream_handler.setFormatter(formatter)

logger.addHandler(file_handler)
logger.addHandler(stream_handler)
