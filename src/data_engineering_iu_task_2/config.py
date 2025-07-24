from pathlib import Path

import yaml
from pydantic import BaseModel, Field

DEFAULT_FILEPATH: Path = (
    Path(__file__).parent.parent.parent.joinpath("config").joinpath("config.yml")
)
"""Default configuration file path."""


class KafkaConfig(BaseModel):
    topic_name: str = Field(
        default="topic_air_quality_pollution_data",
        description="Kafka topic name for data streaming",
    )
    kafka_bootstrap_servers: str = Field(
        default="kafka:9092", description="Kafka bootstrap servers"
    )


class StreamerConfig(BaseModel):
    interval_in_seconds: float = Field(
        default=2.0, description="Interval in seconds for streaming data"
    )
    is_infinite: bool = Field(default=False, description="Run the streamer in an infinite loop")


class DatabaseConfig(BaseModel):
    host: str = Field(default="mongodb", description="Database host")
    port: int = Field(default=27017, description="Database port")
    name: str = Field(default="air_quality_pollution_db", description="Database name")
    collection_name: str = Field(
        default="air_quality_pollution_data",
        description="Collection name for storing air quality and pollution data",
    )


class LogsConfig(BaseModel):
    folder: str = Field(default="/tmp", description="Folder where logs will be stored")
    filemode: str = Field(
        default="w", description="File mode for log files ('a' for append, 'w' for overwrite)"
    )


class AppConfig(BaseModel):
    logs: LogsConfig = Field(
        default_factory=LogsConfig,
        description="Configuration for application logs",
    )


class Config(BaseModel):
    kafka: KafkaConfig = Field(
        default_factory=KafkaConfig,
        description="Configuration for Kafka producer and topic",
    )
    streamer: StreamerConfig = Field(
        default_factory=StreamerConfig,
        description="Configuration for the data streamer",
    )
    database: DatabaseConfig = Field(
        default_factory=DatabaseConfig,
        description="Configuration for the database connection",
    )
    app: AppConfig = Field(
        default_factory=AppConfig,
        description="Configuration for the application",
    )


def get_default_config() -> Config:
    """Get configuration object with default values.

    Returns:
        Config: Initialized configuration object with default values.
    """
    return Config()


def get_config_from_file(filepath: Path = DEFAULT_FILEPATH) -> Config:
    """Get configuration object from a YAML file.

    Args:
        filepath (Path, optional): Path to configuration file (YAML). Defaults to DEFAULT_FILEPATH.

    Returns:
        Config: Initialized configuration object with values from the file.
    """

    if not filepath.exists():
        raise FileNotFoundError(f"Configuration file not found: {filepath}")

    if not filepath.is_file():
        raise ValueError(f"Provided path is not a file: {filepath}")

    if not filepath.suffix == ".yml" and not filepath.suffix == ".yaml":
        raise ValueError(f"Configuration file must be a YAML file: {filepath}")

    with open(filepath, "r") as file:
        config_data = yaml.safe_load(file)

    return Config(**config_data)
