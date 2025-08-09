import json

from kafka import KafkaConsumer


def get_kafka_consumer(
    topic: str, bootstrap_servers: str = "kafka", port: int = 9092
) -> KafkaConsumer:
    """Get a Kafka consumer instance.

    Args:
        topic (str): The topic to consume messages from.
        bootstrap_servers (str, optional): The Kafka bootstrap server address. Defaults to "kafka".
        port (int, optional): The port on which the Kafka broker is running. Defaults to 9092.

    Returns:
        KafkaConsumer: Configured Kafka consumer instance.
    """
    return KafkaConsumer(
        topic,
        bootstrap_servers=f"{bootstrap_servers}:{port}",
        value_deserializer=lambda m: json.loads(m.decode("utf-8")) if m else None,
        enable_auto_commit=False,
        auto_offset_reset="earliest",
        allow_auto_create_topics=True,
        fetch_max_wait_ms=0,
        group_id="kafka-consumer-iu",
    )
