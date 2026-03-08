"""Stub for OAuth2 Client Credentials auth flow (not yet implemented)."""


class ClientCredentialsAuth:
    """Stub for OAuth2 Client Credentials auth flow (not yet implemented)."""

    def __init__(
        self,
        client_id: str,
        client_secret: str,
        skill_name: str = "default",
        **kwargs,
    ) -> None:
        raise NotImplementedError(
            "ClientCredentialsAuth is not yet implemented. Use BearerAuth or ApiKeyAuth instead."
        )
