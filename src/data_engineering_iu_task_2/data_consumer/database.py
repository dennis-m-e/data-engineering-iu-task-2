from typing import Any

from pymongo import MongoClient
from pymongo.errors import ConnectionFailure

from data_engineering_iu_task_2.data_consumer.setup_consumer_logger import logger


class DatabaseClient:
    """Client for interacting with the database."""

    def __init__(
        self,
        database_name: str,
        host: str = "mongodb",
        port: int = 27017,
        user: str | None = None,
        password: str | None = None,
    ) -> None:
        self._database_name: str = database_name
        """Name of the database to connect to."""

        self._client: MongoClient = self._create_client(host, port, user, password)
        """MongoDB client instance."""

        try:
            # The ismaster command is cheap and does not require auth.
            self._client.admin.command("ismaster")
            logger.info(f"Connected to MongoDB at {host}:{port}")
        except ConnectionFailure:
            logger.error(f"Could not connect to MongoDB at {host}:{port}")
            raise Exception("Could not connect to MongoDB server.")

        self._database = self._client[self._database_name]
        """MongoDB database instance."""

    @staticmethod
    def _create_client(
        host: str, port: int, user: str | None = None, password: str | None = None
    ) -> str:
        """Create a MongoDB client.

        Args:
            host (str): Hostname of the MongoDB server.
            port (int): Port number of the MongoDB server.
            user (str | None, optional): Username for authentication. Defaults to None.
            password (str | None, optional): Password for authentication. Defaults to None.

        Returns:
            str: MongoDB client instance.
        """
        if user and password:
            uri = f"mongodb://{user}:{password}@{host}:{port}/"
            logger.info("New MongoDB client created with authentication")
            return MongoClient(uri)
        else:
            logger.info("New MongoDB client created without authentication")
            return MongoClient(host=host, port=port)

    def insert_one(self, collection_name: str, data: dict[str, Any]) -> Any | None:
        """Inserts a single document into the specified collection.

        Args:
            collection_name (str): Name of the collection to insert data into.
            data (dict[str, Any]): Data to be inserted as a dictionary.

        Returns:
            Any | None: The ID of the inserted document. None if procedure fails
        """

        collection = self._database[collection_name]
        try:
            result = collection.insert_one(data)
            logger.info(
                f"Data has been inserted successfully into the collection {collection_name}"
            )
            return result.inserted_id
        except Exception as e:
            logger.error(
                f"Failed to insert data into collection {collection_name}: {e}"
            )

    def insert_many(
        self, collection_name: str, data: list[dict[str, Any]]
    ) -> list[Any] | None:
        """Inserts multiple datasets into the specified collection

        Args:
            collection_name (str): Name of the collection to insert data into
            data (list[dict[str, Any]]): Data to be inserted as a dictionary

        Returns:
            list[Any] | None: List of IDs of the inserted documents. None if procedure fails
        """

        collection = self._database[collection_name]
        try:
            result = collection.insert_many(data)
            logger.info(
                f"Data have been inserted successfully into the collection {collection_name}"
            )
            return result.inserted_ids

        except Exception as e:
            logger.error(
                f"Failed to insert data into collection {collection_name}: {e}"
            )

    def close(self) -> None:
        """Close database client connection"""

        self._client.close()
        logger.info("Database client connection closed")
