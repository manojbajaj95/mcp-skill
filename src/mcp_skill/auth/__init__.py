"""Authentication module for MCP skill clients.

Provides Bearer token and API key authentication with persistent FileTree-backed storage.
All tokens are stored in ~/.mcp-skill/auth/, keyed by server URL.
"""

from .api_key import ApiKeyAuth
from .bearer import BearerAuth
from .client_credentials import ClientCredentialsAuth
from .oauth import OAuth
from .storage import get_token_storage

__all__ = [
    "BearerAuth",
    "ApiKeyAuth",
    "OAuth",
    "ClientCredentialsAuth",
    "get_token_storage",
]
