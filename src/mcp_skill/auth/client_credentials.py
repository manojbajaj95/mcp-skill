"""OAuth2 Client Credentials authentication flow."""

import httpx

from .storage import get_default_token_storage


class ClientCredentialsAuth(httpx.Auth):
    """OAuth2 Client Credentials auth with disk-backed token caching."""

    def __init__(
        self,
        client_id: str,
        client_secret: str,
        token_url: str,
        skill_name: str = "default",
        **kwargs,
    ) -> None:
        self._client_id = client_id
        self._client_secret = client_secret
        self._token_url = token_url
        self._token_storage = get_default_token_storage(skill_name)
        self._access_token: str | None = None

    async def async_auth_flow(self, request: httpx.Request):
        if not self._access_token:
            self._access_token = await self._fetch_token()
        request.headers["Authorization"] = f"Bearer {self._access_token}"
        yield request

    async def _fetch_token(self) -> str:
        cached = await self._token_storage.get(key="cc-token")
        if cached:
            return cached
        async with httpx.AsyncClient() as client:
            resp = await client.post(self._token_url, data={
                "grant_type": "client_credentials",
                "client_id": self._client_id,
                "client_secret": self._client_secret,
            })
            resp.raise_for_status()
            token = resp.json()["access_token"]
            await self._token_storage.put(key="cc-token", value=token)
            return token
