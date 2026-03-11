"""Shared token storage helper for auth classes."""

from pathlib import Path

from key_value.aio.stores.disk import DiskStore


def get_default_token_storage(skill_name: str) -> DiskStore:
    return DiskStore(directory=Path.home() / ".mcp-skill" / skill_name / "api-tokens")
