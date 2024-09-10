"""Tools (catalog) HTTP client."""


class _Tools(object):
    """Tools HTTP client."""

    def __init__(self, client):
        """Create a new instance.

        :param client: The AI4Client instance.
        """
        self.client = client

    def list(self, filters=None):
        """List all tools."""
        params = {}
        for key, value in filters.items():
            if value is None:
                continue
            params[key] = value
        return self.client.request("catalog/tools/detail", "GET", params=params)

    def show(self, tool_id):
        """Show details of a tool."""
        return self.client.request(f"catalog/tools/{tool_id}/metadata", "GET")
