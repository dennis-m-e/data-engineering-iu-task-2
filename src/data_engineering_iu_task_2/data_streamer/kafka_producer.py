import json

from kafka import KafkaProducer


def get_kafka_producer(bootstrap_server: str = "kafka", port: int = 9092) -> KafkaProducer:
    """Get a Kafka producer instance.

    Args:
        bootstrap_server (str, optional): The Kafka bootstrap server address. Defaults to "kafka".
        port (int, optional): The port on which the Kafka broker is running. Defaults to 9092.

    Returns:
        KafkaProducer: Configured Kafka producer instance.
    """
    return KafkaProducer(
        bootstrap_servers=f"{bootstrap_server}:{port}",
        value_serializer=lambda v: json.dumps(v).encode("utf-8"),
    )
