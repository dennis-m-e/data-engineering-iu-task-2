from typing import Any

from kafka import KafkaConsumer

from data_engineering_iu_task_2.config import Config, get_config_from_file
from data_engineering_iu_task_2.data_consumer.database import DatabaseClient
from data_engineering_iu_task_2.data_consumer.kafka_consumer import get_kafka_consumer
from data_engineering_iu_task_2.data_consumer.setup_consumer_logger import logger
from data_engineering_iu_task_2.models import AirQualityPollutionData


class DataConsumer:
    """Consumer instance reading data from a Kafka stream in order to store it in a database"""

    def __init__(
        self,
        config: Config,
    ) -> None:
        self._config: Config = config
        """Configuration for the data streamer"""

        self._consumer: KafkaConsumer = get_kafka_consumer(
            self._config.kafka.topic_name
        )
        """Kafka producer for sending data to the configured Kafka topic."""

        self._database_client: DatabaseClient = DatabaseClient(
            database_name=self._config.database.name,
            host=self._config.database.host,
            port=self._config.database.port,
        )
        """Database client for interacting with the database."""

        logger.info("New data consumer created")

    def run(self) -> None:
        """Run data consumption and database loading"""
        logger.info(f"Start consuming messages from {self._config.kafka.topic_name}")

        for index, message in enumerate(self._consumer):
            # check whether received data corresponds to expected format/model
            data: AirQualityPollutionData = AirQualityPollutionData.model_validate(
                message.value
            )
            logger.info(
                f"Received new message. Data converted successfully to {AirQualityPollutionData.__name__}"
            )

            inserted_id: Any = self._database_client.insert_one(
                self._config.database.collection_name, data.model_dump()
            )
            logger.info(
                f"Message #{index} written to database with id {inserted_id}: {data.model_dump()}"
            )


if __name__ == "__main__":
    config: Config = get_config_from_file()

    consumer: DataConsumer = DataConsumer(config=config)

    # Start consuming incoming messages
    consumer.run()
