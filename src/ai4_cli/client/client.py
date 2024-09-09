"""An HTTP Client for AI4 API."""

import copy
import enum
import hashlib
import json
from urllib import parse

import requests

import ai4_cli
from ai4_cli.client import modules
from ai4_cli import exceptions


class APIVersion(str, enum.Enum):
    """Supported API versions."""

    v1 = "v1"


class AI4Client(object):
    """Client for the AI4 API."""

    def __init__(self, endpoint, version="v1", http_debug=False):
        """Create a new AI4Client.

        :param str endpoint: The URL of the AI4 API.
        :param str version: The version of the API to use. (default: v1)
        :param bool http_debug: Enable HTTP debugging. (default: False)
        """
        self.endpoint = endpoint

        self.version = version

        self.url = parse.urljoin(self.endpoint, self.version.value + "/")

        self._modules = modules._Modules(self)

        self.session = requests.Session()
        self.http_debug = http_debug

    @property
    def modules(self):
        """Return the modules client."""
        return self._modules

    # TODO(aloga): implement cache_request
    # @cache_request
    def request(self, url, method, json=None, **kwargs):
        """Send an HTTP request with the specified characteristics.

        Wrapper around `requests.Session.request` to handle tasks such as
        setting headers, JSON encoding/decoding, and error handling.

        Arguments that are not handled are passed through to the requests
        library.

        :param str url: Path or fully qualified URL of the HTTP request. If
                        only a path is provided then the URL will be prefixed
                        with the attribute self.url. If a fully qualified URL
                        is provided then self.url will be ignored.
        :param str method: The http method to use. (e.g. 'GET', 'POST')
        :param json: Some data to be represented as JSON. (optional)
        :param kwargs: any other parameter that can be passed to
                       :meth:`requests.Session.request` (such as `headers`).
                       Except:

                       - `data` will be overwritten by the data in the `json`
                         param.
                       - `allow_redirects` is ignored as redirects are handled
                         by the session.

        :returns: The response to the request.
        """
        method = method.lower()

        kwargs.setdefault("headers", kwargs.get("headers", {}))

        kwargs["headers"]["User-Agent"] = "ai4-cli-%s" % ai4_cli.__version__
        kwargs["headers"]["Accept"] = "application/json"

        if json is not None:
            kwargs["headers"].setdefault("Content-Type", "application/json")
            kwargs["data"] = self._json.encode(json)

        url = parse.urljoin(self.url, url)

        self.http_log_req(method, url, kwargs)

        resp = self.session.request(method, url, **kwargs)

        self.http_log_resp(resp)

        if resp.status_code >= 400:
            raise exceptions.from_response(resp, resp.json(), url, method)

        content = resp.json()

        return resp, content

    def _get_links_from_response(self, response):
        """Get the links from a JSON response."""
        d = {}
        for link in response.json().get("links", []):
            d[link["rel"]] = link["href"]
        return d.get("self"), d.get("next"), d.get("last")

    def http_log_req(self, method, url, kwargs):
        """Log the request for an HTTP request."""
        if not self.http_debug:
            return

        string_parts = ["curl -g -i"]

        if not kwargs.get("verify", True):
            string_parts.append(" --insecure")

        string_parts.append(" '%s'" % url)
        string_parts.append(" -X %s" % method)

        headers = copy.deepcopy(kwargs["headers"])
        self._redact(headers, ["Authorization"])
        # because dict ordering changes from 2 to 3
        keys = sorted(headers.keys())
        for name in keys:
            value = headers[name]
            header = ' -H "%s: %s"' % (name, value)
            string_parts.append(header)

        if "data" in kwargs:
            data = json.loads(kwargs["data"])
            string_parts.append(" -d '%s'" % json.dumps(data))
        self._logger.debug("REQ: %s" % "".join(string_parts))

    def http_log_resp(self, resp):
        """Log the response from an HTTP request."""
        if not self.http_debug:
            return

        if resp.text and resp.status_code != 400:
            try:
                body = json.loads(resp.text)
                self._redact(body, ["access", "token", "id"])
            except ValueError:
                body = None
        else:
            body = None

        self._logger.debug(
            "RESP: [%(status)s] %(headers)s\nRESP BODY: " "%(text)s\n",
            {
                "status": resp.status_code,
                "headers": resp.headers,
                "text": json.dumps(body),
            },
        )

    def _redact(self, target, path, text=None):
        """Replace the value of a key in `target`.

        The key can be at the top level by specifying a list with a single
        key as the path. Nested dictionaries are also supported by passing a
        list of keys to be navigated to find the one that should be replaced.
        In this case the last one is the one that will be replaced.

        :param dict target: the dictionary that may have a key to be redacted;
                            modified in place
        :param list path: a list representing the nested structure in `target`
                          that should be redacted; modified in place
        :param string text: optional text to use as a replacement for the
                            redacted key. if text is not specified, the
                            default text will be sha1 hash of the value being
                            redacted
        """
        key = path.pop()

        # move to the most nested dict
        for p in path:
            try:
                target = target[p]
            except KeyError:
                return

        if key in target:
            if text:
                target[key] = text
            elif target[key] is not None:
                # because in python3 byte string handling is ... ug
                value = target[key].encode("utf-8")
                sha1sum = hashlib.sha1(value)  # nosec
                target[key] = "{SHA1}%s" % sha1sum.hexdigest()

    def head(self, url, **kwargs):
        """Perform a HEAD request.

        This calls :py:meth:`.request()` with ``method`` set to ``HEAD``.
        """
        return self.request(url, "HEAD", **kwargs)

    def get(self, url, **kwargs):
        """Perform a GET request.

        This calls :py:meth:`.request()` with ``method`` set to ``GET``.
        """
        return self.request(url, "GET", **kwargs)

    def post(self, url, **kwargs):
        """Perform a POST request.

        This calls :py:meth:`.request()` with ``method`` set to ``POST``.
        """
        return self.request(url, "POST", **kwargs)

    def put(self, url, **kwargs):
        """Perform a PUT request.

        This calls :py:meth:`.request()` with ``method`` set to ``PUT``.
        """
        return self.request(url, "PUT", **kwargs)

    def delete(self, url, **kwargs):
        """Perform a DELETE request.

        This calls :py:meth:`.request()` with ``method`` set to ``DELETE``.
        """
        return self.request(url, "DELETE", **kwargs)

    def patch(self, url, **kwargs):
        """Perform a PATCH request.

        This calls :py:meth:`.request()` with ``method`` set to ``PATCH``.
        """
        return self.request(url, "PATCH", **kwargs)
