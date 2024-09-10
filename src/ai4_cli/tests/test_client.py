"""Test the client module."""

import json
from unittest import mock

import pytest

from ai4_cli.client import client
from ai4_cli.client import modules


@pytest.fixture
def endpoint():
    """Return the endpoint URL."""
    return "http://localhost:8080"


@pytest.fixture
def ai4_client(endpoint, monkeypatch):
    """Return an AI4Client instance."""
    obj = client.AI4Client(endpoint)

    mock_logger = mock.Mock()
    monkeypatch.setattr(obj, "_logger", mock_logger)

    return obj


def test_client(ai4_client, endpoint):
    """Test the AI4Client class."""
    assert ai4_client.endpoint == endpoint
    assert ai4_client.version == client.APIVersion.v1
    assert ai4_client.url == "http://localhost:8080/v1/"
    assert isinstance(ai4_client.modules, modules._Modules)


def test_client_invalid_version():
    """Test the AI4Client class with an invalid version."""
    endpoint = "http://localhost:8080"
    version = "foo"
    with pytest.raises(client.exceptions.InvalidUsageError):
        client.AI4Client(endpoint, version=version)


@mock.patch("ai4_cli.client.client.AI4Client.request")
def test_client_get(mock_request, ai4_client):
    """Test the AI4Client.get method."""
    ai4_client.get("foo")
    mock_request.assert_called_with("foo", "GET")


@mock.patch("ai4_cli.client.client.AI4Client.request")
def test_client_get_with_params(mock_request, ai4_client):
    """Test the AI4Client.get method with parameters."""
    ai4_client.get("foo", params={"bar": "baz"})
    mock_request.assert_called_with("foo", "GET", params={"bar": "baz"})


@mock.patch("ai4_cli.client.client.AI4Client.request")
def test_client_post(mock_request, ai4_client):
    """Test the AI4Client.post method."""
    ai4_client.post("foo", json={"bar": "baz"})
    mock_request.assert_called_with("foo", "POST", json={"bar": "baz"})


@mock.patch("ai4_cli.client.client.AI4Client.request")
def test_client_put(mock_request, ai4_client):
    """Test the AI4Client.put method."""
    ai4_client.put("foo", json={"bar": "baz"})
    mock_request.assert_called_with("foo", "PUT", json={"bar": "baz"})


@mock.patch("ai4_cli.client.client.AI4Client.request")
def test_client_delete(mock_request, ai4_client):
    """Test the AI4Client.delete method."""
    ai4_client.delete("foo")
    mock_request.assert_called_with("foo", "DELETE")


@mock.patch("ai4_cli.client.client.AI4Client.request")
def test_client_patch(mock_request, ai4_client):
    """Test the AI4Client.patch method."""
    ai4_client.patch("foo", json={"bar": "baz"})
    mock_request.assert_called_with("foo", "PATCH", json={"bar": "baz"})


@mock.patch("ai4_cli.client.client.AI4Client.request")
def test_client_head(mock_request, ai4_client):
    """Test the AI4Client.head method."""
    ai4_client.head("foo")
    mock_request.assert_called_with("foo", "HEAD")


def test_redact_top_level(ai4_client):
    """Test the _redact method with a top-level key."""
    target = {"key1": "original_value"}
    path = ["key1"]
    expected = {"key1": "{SHA1}2a259fa2c72c0a48475e16cd85bdffe08b58752c"}

    ai4_client._redact(target, path)
    assert target == expected


def test_redact_nested_dict(ai4_client):
    """Test the _redact method with a nested dict."""
    target = {"level1": {"level2": {"key2": "original_value"}}}
    path = ["level1", "level2", "key2"]
    expected = {
        "level1": {"level2": {"key2": "{SHA1}2a259fa2c72c0a48475e16cd85bdffe08b58752c"}}
    }

    ai4_client._redact(target, path)
    assert target == expected


def test_redact_nonexistent_key(ai4_client):
    """Test the _redact method with a nonexistent key."""
    target = {"key1": "original_value"}
    path = ["nonexistent_key"]

    ai4_client._redact(target, path)
    assert target == {"key1": "original_value"}


def test_redact_with_custom_text(ai4_client):
    """Test the _redact method with custom text."""
    target = {"key1": "original_value"}
    path = ["key1"]
    text = "custom_text"
    expected = {"key1": "custom_text"}

    ai4_client._redact(target, path, text)
    assert target == expected


def test_redact_none_value(ai4_client):
    """Test the _redact method with a None value."""
    target = {"key1": None}
    path = ["key1"]

    ai4_client._redact(target, path)
    assert target == {"key1": None}


@pytest.fixture
def response_data():
    """Return a response data."""
    return {
        "links": [
            {"rel": "self", "href": "https://api.example.com/v1/resource"},
            {"rel": "next", "href": "https://api.example.com/v1/resource?page=2"},
            {"rel": "last", "href": "https://api.example.com/v1/resource?page=10"},
        ]
    }


@pytest.fixture
def response(response_data):
    """Return a response."""

    class CustomResponse:
        def json(self):
            return response_data

    return CustomResponse()


def test_get_links_from_response(ai4_client, response):
    """Test the _get_links_from_response method."""
    self_link, next_link, last_link = ai4_client._get_links_from_response(response)

    assert self_link == "https://api.example.com/v1/resource"
    assert next_link == "https://api.example.com/v1/resource?page=2"
    assert last_link == "https://api.example.com/v1/resource?page=10"


@pytest.fixture
def response_data_missing_links():
    """Return a response data missing links."""
    return {}


@pytest.fixture
def response_missing_links(response_data_missing_links):
    """Return a response missing links."""

    class CustomResponse:
        def json(self):
            return response_data_missing_links

    return CustomResponse()


def test_get_links_from_response_missing_links(ai4_client, response_missing_links):
    """Test the _get_links_from_response method with a response missing links."""
    self_link, next_link, last_link = ai4_client._get_links_from_response(
        response_missing_links
    )

    assert self_link is None
    assert next_link is None
    assert last_link is None


class _CustomResponse:
    def __init__(self, status_code, data):
        self.status_code = status_code
        self.headers = {}
        self.text = json.dumps(data)

    def json(self):
        return json.loads(self.text)


def test_http_log_req_debug_enabled(ai4_client):
    """Test the http_log_req method with debug enabled."""
    ai4_client.http_debug = True

    # Simulate a request with headers and data
    method = "POST"
    url = "https://api.example.com/endpoint"
    kwargs = {
        "headers": {
            "Authorization": "Bearer token123",
            "Content-Type": "application/json",
        },
        "data": json.dumps({"key": "value"}),
    }

    ai4_client.http_log_req(method, url, kwargs)

    ai4_client._logger.debug.assert_called_once_with(
        "REQ: curl -g -i 'https://api.example.com/endpoint' -X POST "
        '-H "Authorization: {SHA1}667d57c570d304ad23da77d5467514035a084b64" '
        '-H "Content-Type: application/json" -d \'{"key": "value"}\''
    )


def test_http_log_req_debug_disabled(ai4_client):
    """Test the http_log_req method with debug disabled."""
    ai4_client.http_debug = False

    # Simulate a request
    method = "GET"
    url = "https://api.example.com/another_endpoint"
    kwargs = {}

    ai4_client.http_log_req(method, url, kwargs)

    # Verify that no log is emitted
    ai4_client._logger.debug.assert_not_called()


def test_http_log_resp_debug_enabled(ai4_client, response_data):
    """Test the http_log_resp method with debug enabled."""
    ai4_client.http_debug = True

    response = _CustomResponse(200, response_data)
    ai4_client.http_log_resp(response)

    ai4_client._logger.debug.assert_called_once_with(
        "RESP: [200] {}\nRESP BODY: "
        "{'links': [{'rel': 'self', 'href': 'https://api.example.com/v1/resource'}, "
        "{'rel': 'next', 'href': 'https://api.example.com/v1/resource?page=2'}, "
        "{'rel': 'last', 'href': 'https://api.example.com/v1/resource?page=10'}]}"
    )


def test_http_log_resp_debug_disabled(ai4_client, response_data):
    """Test the http_log_resp method with debug disabled."""
    ai4_client.http_debug = False

    # Simulate a response
    response = _CustomResponse(200, response_data)

    ai4_client.http_log_resp(response)

    # Verify that no log is emitted
    ai4_client._logger.debug.assert_not_called()


def test_http_log_resp_error_response(ai4_client, response_data):
    """Test the http_log_resp method with an error response."""
    ai4_client.http_debug = True

    response = _CustomResponse(400, {"error": "Invalid request"})
    ai4_client.http_log_resp(response)

    ai4_client._logger.debug.assert_called_once_with(
        "RESP: [400] {}\nRESP BODY: {'error': 'Invalid request'}"
    )
