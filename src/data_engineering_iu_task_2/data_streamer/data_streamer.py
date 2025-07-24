import time
from datetime import datetime

from kafka import KafkaProducer

from data_engineering_iu_task_2.config import Config, get_config_from_file
from data_engineering_iu_task_2.data_streamer.data_loading import load_sample_dataset
from data_engineering_iu_task_2.data_streamer.kafka_producer import get_kafka_producer
from data_engineering_iu_task_2.data_streamer.setup_streamer_logger import logger
from data_engineering_iu_task_2.models import AirQualityPollutionData


class DataStreamer:
    """Simulates a data stream from a list of AirQualityPollutionData datasets with a given time interval and sends it to kafka."""

    def __init__(
        self,
        config: Config,
        data: list[AirQualityPollutionData],
    ) -> None:
        self._data = data
        """Data to be streamed, represented as a list of AirQualityPollutionData models."""

        self._config: Config = config
        """Configuration for the data streamer"""

        self._producer: KafkaProducer = get_kafka_producer()
        """Kafka producer for sending data to the configured Kafka topic."""

        logger.info("New data streamer created")

    def run(self) -> None:
        """Run data stream from the DataFrame."""

        logger.info(f"Start streaming data to topic {self._config.kafka.topic_name}")
        logger.info(f"Mode: {'infinite' if self._config.streamer.is_infinite else 'one-time'}")
        logger.info(f"Interval: {self._config.streamer.interval_in_seconds} seconds")

        while True:
            for index, entry in enumerate(self._data):
                # timestamp needed for simulation of a stream
                entry.timestamp = datetime.now().timestamp()  # Update timestamp

                # send data to kafka
                try:
                    self._producer.send(
                        topic=self._config.kafka.topic_name,
                        value=entry.model_dump(),
                    )
                    self._producer.flush()
                    logger.info(f"Sending row {index} to kafka successful: {entry}")
                except Exception as e:
                    logger.error(f"Failed to send data to Kafka: {e}")

                time.sleep(self._config.streamer.interval_in_seconds)

            logger.info(
                "Data stream completed. Restarting..."
                if self._config.streamer.is_infinite
                else "Data stream completed."
            )
            if not self._config.streamer.is_infinite:
                break


if __name__ == "__main__":
    config: Config = get_config_from_file()

    data: list[AirQualityPollutionData] = load_sample_dataset()

    streamer: DataStreamer = DataStreamer(config=config, data=data)

    # Start streaming the static dataset
    streamer.run()
