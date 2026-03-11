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
