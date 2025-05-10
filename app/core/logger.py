import logging
import os
from datetime import datetime
from logging import StreamHandler
from logging import getLogger
from logging.handlers import TimedRotatingFileHandler

log_folder = "logging"
if not os.path.exists(log_folder):
    os.makedirs(log_folder)

logger = getLogger(__name__)
logger.setLevel(os.getenv("LOG_LEVEL", "INFO"))

stream_handler = StreamHandler()
stream_handler.setLevel(os.getenv("LOG_LEVEL", "INFO"))

log_filename = os.path.join(log_folder, datetime.now().strftime("%Y%m%d") + ".log")
file_handler = TimedRotatingFileHandler(log_filename, when="midnight", interval=1)

file_handler.suffix = "%Y-%m-%d"
file_handler.setLevel(os.getenv("LOG_LEVEL", "INFO"))

formatter = logging.Formatter("""[%(levelname)s] %(asctime)s %(message)s (%(filename)s:%(lineno)d:%(funcName)s)""")

stream_handler.setFormatter(formatter)
file_handler.setFormatter(formatter)

logger.addHandler(stream_handler)
logger.addHandler(file_handler)
