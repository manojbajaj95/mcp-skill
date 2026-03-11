"""Authentication module for MCP skill clients.

Provides Bearer token and API key authentication with persistent disk-backed storage.
"""

from fastmcp.client.auth import OAuth

from .api_key import ApiKeyAuth
from .bearer import BearerAuth
from .client_credentials import ClientCredentialsAuth
from .storage import get_default_token_storage

# Note: fastmcp's OAuth does not expose a custom token_storage constructor param,
# so it uses its own default caching rather than get_default_token_storage.

__all__ = [
    "BearerAuth",
    "ApiKeyAuth",
    "OAuth",
    "ClientCredentialsAuth",
    "get_default_token_storage",
]
