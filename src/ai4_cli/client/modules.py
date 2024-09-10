"""Modules (catalog) HTTP client."""


class _Modules(object):
    """Module HTTP client."""

    def __init__(self, client):
        """Create a new instance.

        :param client: The AI4Client instance.
        """
        self.client = client

    def list(self, filters=None):
        """List all modules."""
        params = {}
        for key, value in filters.items():
            if value is None:
                continue
            params[key] = value
        return self.client.request("catalog/modules/detail", "GET", params=params)

    def show(self, module_id):
        """Show details of a module."""
        return self.client.request(f"catalog/modules/{module_id}/metadata", "GET")
