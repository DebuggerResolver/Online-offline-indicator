from utils.db_setup import Redis
from redis import asyncio as redis
import pytest


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "host, port, username, password, expected_host, expected_port, expected_username, expected_password",
    [
        ("localhost", 6379, "testuser", "testpassword", "localhost", 6379, "testuser", "testpassword"),  # Happy path
        ("192.168.1.1", 1234, None, None, "192.168.1.1", 1234, None, None),  # Edge case: No username/password
        (None, None, None, None, "localhost", 6379, None, None),  # Edge case: All defaults
    ],
    ids=["happy_path", "no_auth", "all_defaults"]
)
async def test_connect_happy_path(monkeypatch, host, port, username, password, expected_host, expected_port, expected_username, expected_password):
    # Arrange
    if host:
        monkeypatch.setenv('HOST', host)
    if port:
        monkeypatch.setenv('REDIS_PORT', str(port))
    if username:
        monkeypatch.setenv('REDIS_USERNAME', username)
    if password:
        monkeypatch.setenv('REDIS_PASSWORD', password)

    # Act
    redis_instance = await Redis.connect()

    # Assert
    assert redis_instance.connection_pool.connection_kwargs['host'] == expected_host
    assert redis_instance.connection_pool.connection_kwargs['port'] == expected_port
    assert redis_instance.connection_pool.connection_kwargs['username'] == expected_username
    assert redis_instance.connection_pool.connection_kwargs['password'] == expected_password


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "exception_type",
    [
        (ConnectionError),
        (TimeoutError),
        (redis.exceptions.RedisError),
    ],
    ids=["connection_error", "timeout_error", "redis_error"]
)
async def test_connect_error(monkeypatch, mocker, exception_type):
    # Arrange
    monkeypatch.setenv('HOST', 'non_existent_host')
    mock_connection_pool = mocker.patch('redis.asyncio.BlockingConnectionPool')
    mock_connection_pool.side_effect = exception_type

    # Act and Assert
    with pytest.raises(Exception):
        await Redis.connect()
