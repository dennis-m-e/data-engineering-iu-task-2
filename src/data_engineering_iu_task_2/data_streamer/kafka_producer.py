import json

from kafka import KafkaProducer


def get_kafka_producer(bootstrap_server: str = "kafka:9092") -> KafkaProducer:
    """Get a Kafka producer instance.

    Args:
        bootstrap_server (str, optional): The Kafka bootstrap server address. Defaults to "kafka:9092".

    Returns:
        KafkaProducer: Configured Kafka producer instance.
    """
    return KafkaProducer(
        bootstrap_servers=bootstrap_server,
        value_serializer=lambda v: json.dumps(v).encode("utf-8"),
    )
