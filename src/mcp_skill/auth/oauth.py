"""OAuth authentication wrapper with shared token storage defaults."""

from contextlib import aclosing
import os

from fastmcp.client.auth import OAuth as _FastMCPOAuth

from .storage import get_token_storage

_DEFAULT_OAUTH_CALLBACK_PORT = int(os.getenv("MCP_SKILL_OAUTH_CALLBACK_PORT", "8765"))


class OAuth(_FastMCPOAuth):
    """OAuth provider with persistent FileTree-backed token storage.

    Extends fastmcp's OAuth to use the shared ~/.mcp-skill/auth/ store by default,
    so tokens (already keyed by server URL internally) survive process restarts.
    """

    def __init__(self, **kwargs):
        if "token_storage" not in kwargs:
            kwargs["token_storage"] = get_token_storage()
        if "callback_port" not in kwargs:
            kwargs["callback_port"] = _DEFAULT_OAUTH_CALLBACK_PORT
        super().__init__(**kwargs)

    async def _clear_cached_auth(self) -> None:
        self._initialized = False
        await self.token_storage_adapter.clear()

    @staticmethod
    def _is_retryable_oauth_error(error: Exception) -> bool:
        message = str(error)
        retryable_markers = (
            "Unexpected authorization response: 500",
            'Token exchange failed (400): {"error":"invalid_grant","error_description":"Invalid redirect URI"}',
            '"error":"invalid_grant"',
            "Invalid redirect URI",
        )
        return any(marker in message for marker in retryable_markers)

    async def async_auth_flow(self, request):
        if not self._bound:
            raise RuntimeError(
                "OAuth provider has no server URL. Either pass mcp_url to OAuth() "
                "or use it with Client(auth=...) which provides the URL automatically."
            )

        response = None
        try:
            async with aclosing(super().async_auth_flow(request)) as gen:
                while True:
                    try:
                        yielded_request = await gen.asend(response)  # ty: ignore[invalid-argument-type]
                        response = yield yielded_request
                    except StopAsyncIteration:
                        break
        except Exception as error:
            if not self._is_retryable_oauth_error(error):
                raise
            await self._clear_cached_auth()
            async with aclosing(super().async_auth_flow(request)) as gen:
                retry_response = None
                while True:
                    try:
                        yielded_request = await gen.asend(retry_response)  # ty: ignore[invalid-argument-type]
                        retry_response = yield yielded_request
                    except StopAsyncIteration:
                        break
            return

        if response is not None and response.status_code in {401, 403}:
            await self._clear_cached_auth()

            async with aclosing(super().async_auth_flow(request)) as gen:
                retry_response = None
                while True:
                    try:
                        yielded_request = await gen.asend(retry_response)  # ty: ignore[invalid-argument-type]
                        retry_response = yield yielded_request
                    except StopAsyncIteration:
                        break
