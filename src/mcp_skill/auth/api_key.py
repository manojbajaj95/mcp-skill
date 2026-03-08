"""Custom header API key authentication with persistent disk-backed storage."""
from pathlib import Path

import httpx
from key_value.aio.stores.disk import DiskStore


class ApiKeyAuth(httpx.Auth):
    """Custom header auth with persistent disk-backed storage.

    On first use, pass an api_key to persist it. Subsequent instantiations
    without an api_key will load the token from disk automatically.
    """

    def __init__(
        self,
        api_key: str | None = None,
        skill_name: str = "default",
        header_name: str = "x-api-key",
    ):
        self._api_key = api_key
        self._skill_name = skill_name
        self._header_name = header_name
        self._token_storage = DiskStore(
            directory=Path.home() / ".mcp-skill" / skill_name / "api-tokens"
        )
        self._resolved_key: str | None = None

    async def async_auth_flow(self, request: httpx.Request):
        if not self._resolved_key:
            if self._api_key:
                await self._token_storage.put(key="api-key", value=self._api_key)
                self._resolved_key = self._api_key
            else:
                stored = await self._token_storage.get(key="api-key")
                if stored:
                    self._resolved_key = stored
                else:
                    raise ValueError(
                        "No API key provided and none found in storage at "
                        f"~/.mcp-skill/{self._skill_name}/api-tokens/. "
                        "Pass auth= on first use to persist it."
                    )
        request.headers[self._header_name] = self._resolved_key
        yield request
