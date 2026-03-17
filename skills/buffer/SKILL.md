---
name: buffer
description: "Use this skill when you need to work with buffer through its generated async Python app, call its MCP-backed functions from code, or inspect available functions with the mcp-skill CLI."
metadata:
  short-description: "Use buffer from async Python"
---

# buffer

Use this skill when you need to work with buffer through its generated async Python app, call its MCP-backed functions from code, or inspect available functions with the mcp-skill CLI.

## Authentication

This MCP server uses **Bearer token** authentication. The API key is persisted
to `~/.mcp-skill/auth/` after first use, so subsequent runs can omit it.

```python
# First use — provide and persist the key
app = BufferApp(auth="YOUR_API_KEY")

# Subsequent uses — loaded from disk automatically
app = BufferApp()
```

The key is sent as `Authorization: Bearer <auth>` on every request.

## Dependencies

This skill requires the following Python packages:

- `mcp-skill`

Install with uv:

```bash
uv pip install mcp-skill
```

Or with pip:

```bash
pip install mcp-skill
```

## Python Usage

Use the generated app directly in async Python code:

```python
import asyncio
from buffer.app import BufferApp


async def main():
    app = BufferApp(auth="YOUR_API_KEY")
    result = await app.get_account()
    print(result)


asyncio.run(main())
```

## Async Usage Notes

- Every generated tool method is `async`, so call it with `await`.
- Use these apps inside an async function, then run that function with `asyncio.run(...)` if you are in a script.
- If you forget `await`, you will get a coroutine object instead of the actual tool result.
- Be careful when mixing this with other event-loop environments such as notebooks, web servers, or async frameworks.

## Discover Functions with the CLI

Use the CLI to find available apps, list functions on an app, and inspect a function before calling it:

```bash
uvx mcp-skill list-apps
uvx mcp-skill list-functions buffer
uvx mcp-skill inspect buffer get_account
```

**Important:** Add `.agents/skills` to your Python path so imports resolve correctly:

```python
import sys
sys.path.insert(0, ".agents/skills")
from buffer.app import BufferApp
```

Or set the `PYTHONPATH` environment variable:

```bash
export PYTHONPATH=".agents/skills:$PYTHONPATH"
```

**Preferred: use `uv run`** (handles dependencies automatically):

```bash
PYTHONPATH=.agents/skills uv run --with mcp-skill python -c "
import asyncio
from buffer.app import BufferApp

async def main():
    app = BufferApp(auth='YOUR_API_KEY')
    result = await app.get_account()
    print(result)

asyncio.run(main())
"
```

**Alternative: use `python` directly** (install dependencies first):

```bash
pip install mcp-skill
PYTHONPATH=.agents/skills python -c "
import asyncio
from buffer.app import BufferApp

async def main():
    app = BufferApp(auth='YOUR_API_KEY')
    result = await app.get_account()
    print(result)

asyncio.run(main())
"
```
