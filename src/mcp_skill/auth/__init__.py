"""Authentication module for MCP skill clients.

Provides Bearer token and API key authentication with persistent disk-backed storage.
"""
from fastmcp.client.auth import OAuth

from .api_key import ApiKeyAuth
from .bearer import BearerAuth
from .client_credentials import ClientCredentialsAuth

__all__ = [
    "BearerAuth",
    "ApiKeyAuth",
    "OAuth",
    "ClientCredentialsAuth",
]
