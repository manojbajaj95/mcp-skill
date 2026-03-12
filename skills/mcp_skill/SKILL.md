---
name: mcp-skill
description: Use this skill when working with the mcp-skill CLI to create generated MCP app wrappers, list available generated apps, list functions for a specific app, inspect a generated function signature and docstring, or understand how to call generated apps from async Python.
metadata:
  short-description: Use the mcp-skill CLI and generated apps
---

# mcp-skill

Use this skill when you need to work with the `mcp-skill` CLI or use a generated MCP-backed app from Python.

## What It Does

This skill helps with:

1. Creating a new generated app wrapper from an MCP server
2. Listing generated apps available locally
3. Listing functions for a specific generated app
4. Inspecting a function before calling it
5. Using the generated app from async Python

## Dependencies

CLI usage depends on:

- `uv`
- `mcp-skill`

Python usage depends on:

- `mcp-skill`

## Core Commands

```bash
# Create a new generated app wrapper
uvx mcp-skill create --url https://example.com/mcp --name example --non-interactive

# List generated apps
uvx mcp-skill list-apps

# List functions for one app
uvx mcp-skill list-functions notion

# Inspect one function
uvx mcp-skill inspect notion notion_search
```

## Example

Find a generated app, inspect the function you need, then call it from async Python:

```python
import asyncio
from sentry.app import SentryApp


async def main():
    sentry = SentryApp()
    user = await sentry.whoami()
    print(user)


asyncio.run(main())
```

## Async Usage Notes

- Generated app methods are `async` and should be called with `await`.
- Use them inside `async def`, then run that function with `asyncio.run(...)` in a normal script.
- If you skip `await`, you will get a coroutine object instead of the real result.
- Be careful in environments that already manage an event loop.

## Recommended Workflow

1. Run `uvx mcp-skill list-apps` to find the generated app name.
2. Run `uvx mcp-skill list-functions <app>` to see available functions.
3. Run `uvx mcp-skill inspect <app> <function>` to confirm the exact signature and docstring.
4. Import the app class from `<app>.app` and call the async method you found.
