import os
import logging
from logging.handlers import TimedRotatingFileHandler
from datetime import datetime

# Define a custom log format
log_format = "[%(asctime)s] [%(levelname)s] %(message)s"

# Create a directory for logs if it doesn't exist
log_dir = os.path.join(os.path.dirname(__file__), 'logs')
if not os.path.exists(log_dir):
    os.makedirs(log_dir)

# Generate a log file name with a daily rotation and timestamp prefix
log_prefix = datetime.now().strftime('%Y%m%d')
log_file = os.path.join(log_dir, f'{log_prefix}_app.log')

# Create a logger and configure it
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# Create a timed rotating file handler with daily rotation
file_handler = TimedRotatingFileHandler(
    filename=log_file,
    when='midnight',  # Rotate at midnight
    interval=1,        # Rotate daily
    backupCount=30,    # Keep logs for 30 days
)
file_handler.setLevel(logging.DEBUG)

# Create a stream handler to display log messages in the console
stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.INFO)

# Create a formatter
formatter = logging.Formatter(log_format)

# Set the formatter for the handlers
file_handler.setFormatter(formatter)
stream_handler.setFormatter(formatter)

# Add the handlers to the logger
logger.addHandler(file_handler)
logger.addHandler(stream_handler)
