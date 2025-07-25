from typing import Any
from unittest.mock import MagicMock, patch

import pytest
from pymongo.errors import ConnectionFailure

from data_engineering_iu_task_2.data_consumer.database import DatabaseClient

DATABASE_NAME = "test_db"
"""Test cases for the DatabaseClient class."""


@pytest.fixture
def mock_mongo_client() -> Any:
    """Mock MongoDB client fixture.

    Yields:
        Any: Mocked MongoDB client
    """
    with patch("data_engineering_iu_task_2.data_consumer.database.MongoClient") as mongo:
        yield mongo


def test_init_success(mock_mongo_client: Any) -> None:
    """Test successful initialization of DatabaseClient.

    Args:
        mock_mongo_client (Any): MongoDB client mock object
    """

    mock_client: MagicMock = MagicMock()
    mock_mongo_client.return_value = mock_client
    mock_client.admin.command.return_value = {"ok": 1}

    client: DatabaseClient = DatabaseClient(DATABASE_NAME)
    assert client._database_name == DATABASE_NAME


def test_init_connection_failure(mock_mongo_client: Any) -> None:
    """Test initialization failure of DatabaseClient.

    Args:
        mock_mongo_client (Any): MongoDB client mock object
    """
    mock_client = MagicMock()
    mock_mongo_client.return_value = mock_client
    mock_client.admin.command.side_effect = ConnectionFailure()

    with pytest.raises(Exception, match="Could not connect to MongoDB server."):
        DatabaseClient(DATABASE_NAME)


def test_create_client_with_auth() -> None:
    """Test creating a MongoDB client with authentication."""
    with patch("data_engineering_iu_task_2.data_consumer.database.MongoClient") as mongo:
        DatabaseClient._create_client("host", 1234, "user", "pass")
        mongo.assert_called_with("mongodb://user:pass@host:1234/")


def test_create_client_without_auth() -> None:
    """Test creating a MongoDB client without authentication."""
    with patch("data_engineering_iu_task_2.data_consumer.database.MongoClient") as mongo:
        DatabaseClient._create_client("host", 1234)
        mongo.assert_called_with(host="host", port=1234)


def test_insert_one_success(mock_mongo_client: Any) -> None:
    """Test successful insertion of a single document.

    Args:
        mock_mongo_client (Any): Mock MongoDB client
    """
    client: DatabaseClient = DatabaseClient(DATABASE_NAME)
    collection: MagicMock = MagicMock()

    client._database = {"col": collection}
    collection.insert_one.return_value.inserted_id = "id1"

    result = client.insert_one("col", {"a": 1})
    assert result == "id1"


def test_insert_one_failure(mock_mongo_client: Any) -> None:
    """Test failure of inserting a single document.

    Args:
        mock_mongo_client (Any): Mock MongoDB client
    """
    client: DatabaseClient = DatabaseClient(DATABASE_NAME)
    collection: MagicMock = MagicMock()

    client._database = {"col": collection}
    collection.insert_one.side_effect = Exception("fail")

    result = client.insert_one("col", {"a": 1})
    assert result is None


def test_insert_many_success(mock_mongo_client: Any) -> None:
    """Test successful insertion of multiple documents.

    Args:
        mock_mongo_client (Any): Mock MongoDB client
    """
    client: DatabaseClient = DatabaseClient(DATABASE_NAME)
    collection = MagicMock()

    client._database = {"col": collection}
    collection.insert_many.return_value.inserted_ids = ["id1", "id2"]

    result = client.insert_many("col", [{"a": 1}, {"b": 2}])
    assert result == ["id1", "id2"]


def test_insert_many_failure(mock_mongo_client: Any) -> None:
    """Test failure of inserting multiple documents.

    Args:
        mock_mongo_client (Any): Mock MongoDB client
    """
    client: DatabaseClient = DatabaseClient(DATABASE_NAME)
    collection: MagicMock = MagicMock()

    client._database = {"col": collection}
    collection.insert_many.side_effect = Exception("fail")

    result = client.insert_many("col", [{"a": 1}])
    assert result is None


def test_close(mock_mongo_client: Any) -> None:
    client: DatabaseClient = DatabaseClient(DATABASE_NAME)
    client._client = MagicMock()

    client.close()
    client._client.close.assert_called_once()
