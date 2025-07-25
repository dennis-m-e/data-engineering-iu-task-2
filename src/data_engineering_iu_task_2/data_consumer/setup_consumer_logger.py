import logging
from datetime import datetime
from pathlib import Path

from data_engineering_iu_task_2.setup_logger import get_new_file_logger

_logger_timestamp: int = int(datetime.now().timestamp())
_logger_name: str = Path(__file__).parent.stem
logger: logging.Logger = get_new_file_logger(f"{_logger_timestamp}_{_logger_name}")
"""Logger setup for the data consumer module."""
