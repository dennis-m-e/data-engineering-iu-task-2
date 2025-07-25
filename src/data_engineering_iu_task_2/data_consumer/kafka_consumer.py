import json

from kafka import KafkaConsumer


def get_kafka_consumer(
    topic: str, bootstrap_server: str = "kafka:9092"
) -> KafkaConsumer:
    """Get a Kafka consumer instance.

    Args:
        topic (str): The topic to consume messages from.
        bootstrap_server (str, optional): The Kafka bootstrap server address. Defaults to "kafka:9092".

    Returns:
        KafkaConsumer: Configured Kafka consumer instance.
    """
    return KafkaConsumer(
        topic,
        bootstrap_servers=bootstrap_server,
        value_deserializer=lambda m: json.loads(m.decode("utf-8")) if m else None,
        auto_offset_reset="earliest",
        allow_auto_create_topics=True,
        fetch_max_wait_ms=0,
        group_id="my-group",
    )
