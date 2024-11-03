import logging
import os
from skin.constants import *

# Constructing the path for log files with LOGS_DIR and TIMESTAMP
logs_path = os.path.join(os.getcwd(), LOGS_DIR, TIMESTAMP)
os.makedirs(logs_path, exist_ok=True)  # Creates logs directory with timestamp

LOG_FILE_PATH = os.path.join(logs_path, LOGS_FILE_NAME)

# Set up logging with both file and console handlers
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# File handler to log to the file
file_handler = logging.FileHandler(LOG_FILE_PATH)
file_handler.setFormatter(logging.Formatter("[ %(asctime)s ] %(lineno)d %(name)s - %(levelname)s - %(message)s"))
file_handler.setLevel(logging.INFO)

# Console handler to log to the console
console_handler = logging.StreamHandler()
console_handler.setFormatter(logging.Formatter("[ %(asctime)s ] %(lineno)d %(name)s - %(levelname)s - %(message)s"))
console_handler.setLevel(logging.INFO)

# Add handlers to the logger
logger.addHandler(file_handler)
logger.addHandler(console_handler)
