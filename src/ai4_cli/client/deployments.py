"""Deployments HTTP client."""


class _Deployments(object):
    """Deployments HTTP client."""

    def __init__(self, client):
        """Create a new instance.

        :param client: The AI4Client instance.
        """
        self.client = client

    def list(self, filters=None):
        """List all deployments."""
        params = {}
        if filters:
            for key, value in filters.items():
                if value is None:
                    continue
                params[key] = value
        token = self.client.oidc_agent.get_token()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}

        return self.client.request(
            "deployments/modules", "GET", params=params, headers=headers
        )
