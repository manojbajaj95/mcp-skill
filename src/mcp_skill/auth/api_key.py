"""Custom header API key authentication with persistent storage keyed by server URL."""

import asyncio
import httpx

from .storage import get_token_storage


class ApiKeyAuth(httpx.Auth):
    """Custom header auth with persistent storage.

    Tokens are stored under ``<server_url>/api_key`` in the shared token store.
    On first use, pass an api_key to persist it. Subsequent instantiations
    without an api_key will load the token from storage automatically.
    """

    def __init__(
        self,
        api_key: str | None = None,
        server_url: str = "",
        header_name: str = "x-api-key",
    ):
        self._api_key = api_key
        self._storage_key = f"{server_url}/api_key"
        self._header_name = header_name
        self._token_storage = get_token_storage()
        self._resolved_key: str | None = None

    async def async_auth_flow(self, request: httpx.Request):
        if not self._resolved_key:
            if self._api_key:
                await self._token_storage.put(key=self._storage_key, value=self._api_key)
                self._resolved_key = self._api_key
            else:
                stored = await self._token_storage.get(key=self._storage_key)
                if stored:
                    self._resolved_key = stored
                else:
                    loop = asyncio.get_event_loop()
                    entered = await loop.run_in_executor(
                        None, lambda: input(f"API Key for {self._storage_key}: ")
                    )
                    if not entered:
                        raise ValueError("No API key provided.")
                    await self._token_storage.put(key=self._storage_key, value=entered)
                    self._resolved_key = entered
        request.headers[self._header_name] = self._resolved_key
        yield request
