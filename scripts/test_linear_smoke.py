"""Smoke test for the generated Linear app wrapper."""

import argparse
import asyncio
import importlib
import json
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "skills"))


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Smoke test the existing Linear app.")
    parser.add_argument(
        "--check",
        choices=("teams", "users"),
        default="teams",
        help="Read-only Linear method to exercise.",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=1,
        help="Number of records to request for list methods.",
    )
    return parser


def _summarize_payload(payload: Any) -> dict[str, Any]:
    if isinstance(payload, dict):
        summary: dict[str, Any] = {"type": "dict", "keys": sorted(payload.keys())[:10]}
        for key in ("nodes", "results", "items", "teams", "users"):
            value = payload.get(key)
            if isinstance(value, list):
                summary["collection_key"] = key
                summary["collection_size"] = len(value)
                if value:
                    summary["first_item_keys"] = sorted(value[0].keys())[:10]
                break
        return summary
    return {"type": type(payload).__name__, "repr": repr(payload)[:200]}


async def _run(check: str, limit: int) -> dict[str, Any]:
    linear_module = importlib.import_module("linear.app")
    app_class = linear_module.LinearApp
    app = app_class()
    if check == "users":
        return await app.list_users(limit=limit)
    return await app.list_teams(limit=limit)


def main() -> int:
    args = _build_parser().parse_args()
    try:
        payload = asyncio.run(_run(args.check, args.limit))
    except Exception as exc:
        print(f"linear smoke test failed: {exc}", file=sys.stderr)
        return 1

    print(json.dumps(_summarize_payload(payload), indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
