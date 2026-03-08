"""Authentication module for MCP skill clients.

Provides Bearer token and API key authentication with persistent disk-backed storage.
"""
from fastmcp.client.auth import OAuth

from .api_key import ApiKeyAuth
from .bearer import BearerAuth

__all__ = [
    "BearerAuth",
    "ApiKeyAuth",
    "OAuth",
    "ClientCredentialsAuth",  # Forward reference - will be added in Task 2
]
