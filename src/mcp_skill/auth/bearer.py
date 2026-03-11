"""Bearer token authentication with persistent disk-backed storage."""
import httpx

from .storage import get_default_token_storage


class BearerAuth(httpx.Auth):
    """Bearer token auth with persistent disk-backed storage.

    On first use, pass an api_key to persist it. Subsequent instantiations
    without an api_key will load the token from disk automatically.
    """

    def __init__(self, api_key: str | None = None, skill_name: str = "default"):
        self._api_key = api_key
        self._skill_name = skill_name
        self._token_storage = get_default_token_storage(skill_name)
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
        request.headers["Authorization"] = f"Bearer {self._resolved_key}"
        yield request
