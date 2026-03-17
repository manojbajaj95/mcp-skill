"""Shared token storage helper for auth classes."""

from pathlib import Path

from key_value.aio.stores.disk import DiskStore

_STORE_DIR = Path.home() / ".mcp-skill" / "auth"
_store: DiskStore | None = None


def get_token_storage() -> DiskStore:
    """Return the shared token store at ~/.mcp-skill/auth/."""
    global _store
    if _store is None:
        _store = DiskStore(directory=_STORE_DIR)
    return _store


async def put_token(store: DiskStore, key: str, token: str) -> None:
    """Persist a token in the disk store's mapping-based format."""
    await store.put(key=key, value={"token": token})


async def get_token(store: DiskStore, key: str) -> str | None:
    """Load a token from the disk store."""
    stored = await store.get(key=key)
    if not stored:
        return None

    token = stored.get("token")
    if isinstance(token, str) and token:
        return token
    return None
