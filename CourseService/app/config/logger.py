import logging
from logging.handlers import RotatingFileHandler
import os

if not os.path.exists("logs"):
    os.makedirs("logs")

formatter = logging.Formatter(
    "%(asctime)s - [%(levelname)s] - %(name)s - %(message)s"
)

combined_handler = RotatingFileHandler(
    "logs/combined.log", maxBytes=5*1024*1024, backupCount=5
)
combined_handler.setFormatter(formatter)
combined_handler.setLevel(logging.INFO)

# Error log handler
error_handler = RotatingFileHandler(
    "logs/error.log", maxBytes=5*1024*1024, backupCount=5
)
error_handler.setFormatter(formatter)
error_handler.setLevel(logging.ERROR)

# Main logger setup
logger = logging.getLogger("course-service")
logger.setLevel(logging.INFO)
logger.addHandler(combined_handler)
logger.addHandler(error_handler)
