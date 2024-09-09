"""Module HTTP client."""


class _Modules(object):
    """Module HTTP client."""

    def __init__(self, client):
        """Create a new instance.

        :param client: The AI4Client instance.
        """
        self.client = client

    def list(self):
        """List all modules."""
        return self.client.request("catalog/modules/detail", "GET")
