import logging
from logging.handlers import RotatingFileHandler

from app.core.settings import get_settings

settings = get_settings()

formatter = logging.Formatter(
    '[%(asctime)s] - %(module)s - p%(process)s {%(pathname)s:%(lineno)d} %(levelname)s - %(message)s',
    '%m-%d %H:%M:%S'
)

site_log_names = (
    'main',
    'activities',
    'users',
    'courses',
    'authentication',
    'exercises'
)


def setup_logger(name, log_file, level=logging.INFO):
    """
    Custom logger setup
    """

    _2MB: int = 1024 * 1024 * 200
    _backups_num = 1

    handler = RotatingFileHandler(log_file, maxBytes=_2MB, backupCount=_backups_num)
    handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(handler)

    # Additional stream to throw the errors to the console too
    logger.addHandler(logging.StreamHandler())

    return logger


for log_name in site_log_names:
    setup_logger(f'{log_name}', f'{settings.logs_dir}/{log_name}.log')



