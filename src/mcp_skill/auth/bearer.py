"""Bearer token authentication with persistent storage keyed by server URL."""
import asyncio

import httpx

from .storage import get_token_storage


class BearerAuth(httpx.Auth):
    """Bearer token auth with persistent storage.

    Tokens are stored under ``<server_url>/api_key`` in the shared token store.
    On first use, pass an api_key to persist it. Subsequent instantiations
    without an api_key will load the token from storage automatically.
    """

    def __init__(self, api_key: str | None = None, server_url: str = ""):
        self._api_key = api_key
        self._storage_key = f"{server_url}/api_key"
        self._token_storage = get_token_storage()
        self._resolved_key: str | None = None
        self._loaded_from_storage = False

    async def _resolve_key(self) -> str:
        if self._resolved_key:
            return self._resolved_key

        self._loaded_from_storage = False
        if self._api_key:
            await self._token_storage.put(key=self._storage_key, value=self._api_key)
            self._resolved_key = self._api_key
            return self._resolved_key

        stored = await self._token_storage.get(key=self._storage_key)
        if stored:
            self._resolved_key = stored
            self._loaded_from_storage = True
            return self._resolved_key

        loop = asyncio.get_event_loop()
        entered = await loop.run_in_executor(
            None, lambda: input(f"Bearer token for {self._storage_key}: ")
        )
        if not entered:
            raise ValueError("No API key provided.")
        await self._token_storage.put(key=self._storage_key, value=entered)
        self._resolved_key = entered
        return self._resolved_key

    async def _clear_stored_key(self) -> None:
        await self._token_storage.delete(key=self._storage_key)
        self._resolved_key = None
        self._loaded_from_storage = False

    async def async_auth_flow(self, request: httpx.Request):
        key = await self._resolve_key()
        request.headers["Authorization"] = f"Bearer {key}"
        response = yield request

        if (
            response.status_code in {401, 403}
            and (self._loaded_from_storage or self._api_key is not None)
        ):
            await self._clear_stored_key()
