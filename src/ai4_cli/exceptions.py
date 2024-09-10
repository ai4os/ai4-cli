"""Exceptions for the AI4 client."""


class BaseError(Exception):
    """The base exception class for all exceptions this library raises."""

    message = "An unknown exception occurred."
    details = ""

    def __init__(self, message=None, details=None, **kwargs):
        """Create a new exception with the given message."""
        self.kwargs = kwargs

        if details:
            self.details = details

        if not message:
            try:
                message = self.message % kwargs
            except Exception:
                # kwargs doesn't match a variable in the message
                # log the issue and the kwargs
                print("Exception in string format operation")
                for name, value in kwargs.iteritems():
                    print("%s: %s" % (name, value))
                raise

        message = "  ERROR: " + message
        if self.details:
            message += "\n\nDETAILS: " + self.details

        super(BaseError, self).__init__(message)


class InvalidUsageError(BaseError):
    """The client is being used incorrectly."""

    message = "Invalid client usage"


class InvalidUrlError(BaseError):
    """The provided URL is not valid."""

    message = "URL provided is not valid (%(url)s)"


class BaseHTTPError(BaseError):
    """The base exception class for all HTTP exceptions."""

    message = "HTTP error: %(code)s"
    http_status = 500


class BadRequestError(BaseHTTPError):
    """HTTP 400 - Bad request.

    You sent some malformed data.
    """

    http_status = 400
    message = "Bad request"


class UnauthorizedError(BaseHTTPError):
    """HTTP 401 - Unauthorized.

    Bad credentials.
    """

    http_status = 401
    message = "Unauthorized"


class ForbiddenError(BaseHTTPError):
    """HTTP 403 - Forbidden.

    Your credentials don't give you access to this resource.
    """

    http_status = 403
    message = "Forbidden"


class NotFoundError(BaseHTTPError):
    """HTTP 404 - Not found."""

    http_status = 404
    message = "Not found"


class MethodNotAllowedError(BaseHTTPError):
    """HTTP 405 - Method Not Allowed."""

    http_status = 405
    message = "Method Not Allowed"


class NotAcceptableError(BaseHTTPError):
    """HTTP 406 - Not Acceptable."""

    http_status = 406
    message = "Not Acceptable"


class ConflictError(BaseHTTPError):
    """HTTP 409 - Conflict."""

    http_status = 409
    message = "Conflict"


class HTTPNotImplementedError(BaseHTTPError):
    """HTTP 501 - Not Implemented.

    The server does not support this operation.
    """

    http_status = 501
    message = "Not Implemented"


_code_map = dict((c.http_status, c) for c in BaseHTTPError.__subclasses__())


def from_response(response, body, url, method=None):
    """Return an instance of BaseHTTPError or subclass based on a response.

    Usage::

        resp, body = requests.request(...)
        if resp.status_code != 200:
            raise exception_from_response(resp, rest.text)
    """
    cls = _code_map.get(response.status_code, BaseHTTPError)

    kwargs = {
        "code": response.status_code,
        "method": method,
        "url": url,
        "request_id": None,
    }

    if body:
        message = "n/a"
        details = "n/a"

        if hasattr(body, "keys"):
            message = body.get("message")
            details = body.get("detail")

        kwargs["message"] = message
        kwargs["details"] = details

    return cls(**kwargs)
