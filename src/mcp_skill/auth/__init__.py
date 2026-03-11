"""Authentication module for MCP skill clients.

Provides Bearer token and API key authentication with persistent FileTree-backed storage.
All tokens are stored in ~/.mcp-skill/auth/, keyed by server URL.
"""

from fastmcp.client.auth import OAuth as _FastMCPOAuth

from .api_key import ApiKeyAuth
from .bearer import BearerAuth
from .client_credentials import ClientCredentialsAuth
from .storage import get_token_storage


class OAuth(_FastMCPOAuth):
    """OAuth provider with persistent FileTree-backed token storage.

    Extends fastmcp's OAuth to use the shared ~/.mcp-skill/auth/ store by default,
    so tokens (already keyed by server URL internally) survive process restarts.
    """

    def __init__(self, **kwargs):
        if "token_storage" not in kwargs:
            kwargs["token_storage"] = get_token_storage()
        super().__init__(**kwargs)


__all__ = [
    "BearerAuth",
    "ApiKeyAuth",
    "OAuth",
    "ClientCredentialsAuth",
    "get_token_storage",
]
