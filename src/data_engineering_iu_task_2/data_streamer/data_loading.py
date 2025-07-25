import sys
from pathlib import Path

import pandas as pd

from data_engineering_iu_task_2.data_streamer.setup_streamer_logger import logger
from data_engineering_iu_task_2.models import AirQualityPollutionData

DEFAULT_FILENAME: str = "sample_air_quality_pollution_data.csv"
"""Default filename for the sample dataset."""

DEFAULT_FILEPATH: Path = (
    Path(__file__)
    .parent.parent.parent.parent.joinpath("data")
    .joinpath(DEFAULT_FILENAME)
)
"""Default file path for the sample dataset."""


def add_timestamp_column(data: pd.DataFrame) -> pd.DataFrame:
    """Add timestamp column to the DataFrame if it does not exist.

    Args:
        data (pd.DataFrame): DataFrame to which the timestamp column will be added.

    Returns:
        pd.DataFrame: DataFrame with a timestamp column added if it was not present.
    """

    if "timestamp" not in data.columns:
        data["timestamp"] = None  # Add a timestamp column with NaT values

    logger.info("Timestamp column added to the dataframe")
    return data


def lower_column_names(data: pd.DataFrame) -> pd.DataFrame:
    """Lowercase all column names in the DataFrame.

    Args:
        data (pd.DataFrame): DataFrame with column names to be lowercased.

    Returns:
        pd.DataFrame: DataFrame with lowercased column names.
    """
    data.columns = [col.lower() for col in data.columns]

    logger.info("Column names have been lowercased")

    return data


def remove_whitespace_from_column_names(data: pd.DataFrame) -> pd.DataFrame:
    """Remove whitespace from column names in the DataFrame.

    Args:
        data (pd.DataFrame): DataFrame with column names to be cleaned.

    Returns:
        pd.DataFrame: DataFrame with column names without whitespace.
    """
    data.columns = [col.replace(" ", "_") for col in data.columns]

    logger.info("Whitespace has been removed from column names")

    return data


def rename_column(data: pd.DataFrame, old_name: str, new_name: str) -> pd.DataFrame:
    """Rename a column in the DataFrame.

    Args:
        data (pd.DataFrame): DataFrame with the column to be renamed.
        old_name (str): Current name of the column.
        new_name (str): New name for the column.

    Returns:
        pd.DataFrame: DataFrame with the renamed column.
    """
    data = data.rename(columns={old_name: new_name})

    logger.info(f"Column '{old_name}' has been renamed to '{new_name}'")

    return data


def load_sample_dataset(
    filepath: Path = DEFAULT_FILEPATH,
) -> list[AirQualityPollutionData]:
    """Load a sample dataset from a CSV file and prepare it for streaming.

    Args:
        filepath (Path): Path to the CSV file containing the dataset.

    Returns:
        list[AirQualityPollutionData]: List of AirQualityPollutionData models created from the DataFrame rows.
    """
    data: pd.DataFrame = pd.read_csv(filepath)
    data = add_timestamp_column(data)
    data = lower_column_names(data)
    data = remove_whitespace_from_column_names(data)
    data = rename_column(data, "pm2.5", "pm_2_5")
    data = rename_column(data, "pm10", "pm_10")
    data = rename_column(data, "no2", "no_2")
    data = rename_column(data, "so2", "so_2")

    # Validate and convert DataFrame rows to AirQualityPollutionData models
    validated_data: list[AirQualityPollutionData] = []
    for _, row in data.iterrows():
        try:
            validated_data.append(AirQualityPollutionData(**row.to_dict()))
        except Exception as e:
            logger.error(f"Error validating row {row}: {e}")
            sys.exit(1)
    logger.info("Sample dataset loaded and prepared for streaming")

    return validated_data
