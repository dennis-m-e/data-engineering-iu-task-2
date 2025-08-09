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
    """Test successful insertion of a single document."""
    client: DatabaseClient = DatabaseClient(DATABASE_NAME)
    collection: MagicMock = MagicMock()
    client._database = {"col": collection}
    collection.insert_one.return_value.inserted_id = "id1"
    result = client.insert_one("col", {"a": 1})
    assert result == "id1"


def test_insert_one_failure(mock_mongo_client: Any) -> None:
    """Test failure of inserting a single document."""
    client: DatabaseClient = DatabaseClient(DATABASE_NAME)
    collection: MagicMock = MagicMock()
    client._database = {"col": collection}
    collection.insert_one.side_effect = Exception("fail")
    with pytest.raises(Exception, match="fail"):
        client.insert_one("col", {"a": 1})


def test_find_one_found(mock_mongo_client: Any) -> None:
    """Test finding a document that exists."""
    client: DatabaseClient = DatabaseClient(DATABASE_NAME)
    collection: MagicMock = MagicMock()
    client._database = {"col": collection}
    collection.find_one.return_value = {"_id": "id1", "a": 1}
    result = client.find_one("col", {"a": 1})
    assert result == {"_id": "id1", "a": 1}


def test_find_one_not_found(mock_mongo_client: Any) -> None:
    """Test finding a document that does not exist."""
    client: DatabaseClient = DatabaseClient(DATABASE_NAME)
    collection: MagicMock = MagicMock()
    client._database = {"col": collection}
    collection.find_one.return_value = None
    result = client.find_one("col", {"a": 2})
    assert result is None


def test_close(mock_mongo_client: Any) -> None:
    client: DatabaseClient = DatabaseClient(DATABASE_NAME)
    client._client = MagicMock()
    client.close()
    client._client.close.assert_called_once()
