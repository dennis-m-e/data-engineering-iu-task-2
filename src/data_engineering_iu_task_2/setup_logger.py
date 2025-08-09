import logging
from pathlib import Path
from typing import Literal


def get_new_file_logger(
    name: str,
    level: int = logging.INFO,
    logs_folder_path: Path = Path("/tmp"),
    filemode: Literal["a", "w"] = "a",
) -> logging.Logger:
    """Create a new logger with the specified name.

    Args:
        name (str): Name of the logger.

    Returns:
        logging.Logger: Configured logger instance.
    """

    custom_logger = logging.getLogger(name)
    logging.basicConfig(
        format="[%(asctime)s] - %(levelname)s - %(filename)s - %(message)s",
        style="%",
        datefmt="%Y-%m-%d %H:%M:%S",
        level=level,
        filename=logs_folder_path.joinpath(f"{name}.log").as_posix(),
        filemode=filemode,
    )

    custom_logger.setLevel(level)

    return custom_logger
