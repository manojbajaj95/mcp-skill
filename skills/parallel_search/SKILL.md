---
name: parallel-search
description: "MCP skill for search-mcp. Provides 2 tools: web_search_preview, web_fetch"
---

# parallel-search

MCP skill for search-mcp. Provides 2 tools: web_search_preview, web_fetch

## Authentication

This MCP server uses **OAuth** authentication.
The OAuth flow is handled automatically by the MCP client. Tokens are persisted
to `~/.mcp-skill/auth/` so subsequent runs reuse the same credentials without
re-authenticating.

```python
app = ParallelsearchApp()  # uses default OAuth flow
```

To bring your own OAuth provider, pass it via the `auth` argument:

```python
app = ParallelsearchApp(auth=my_oauth_provider)
```

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

## How to Run

**Important:** Add `.agents/skills` to your Python path so imports resolve correctly:

```python
import sys
sys.path.insert(0, ".agents/skills")
from parallel_search.app import ParallelsearchApp
```

Or set the `PYTHONPATH` environment variable:

```bash
export PYTHONPATH=".agents/skills:$PYTHONPATH"
```

**Preferred: use `uv run`** (handles dependencies automatically):

```bash
PYTHONPATH=.agents/skills uv run --with mcp-skill python -c "
import asyncio
from parallel_search.app import ParallelsearchApp

async def main():
    app = ParallelsearchApp()
    result = await app.web_search_preview(objective="example", search_queries="value")
    print(result)

asyncio.run(main())
"
```

**Alternative: use `python` directly** (install dependencies first):

```bash
pip install mcp-skill
PYTHONPATH=.agents/skills python -c "
import asyncio
from parallel_search.app import ParallelsearchApp

async def main():
    app = ParallelsearchApp()
    result = await app.web_search_preview(objective="example", search_queries="value")
    print(result)

asyncio.run(main())
"
```

## Available Tools

### web_search_preview

Purpose: Perform web searches and return results in an LLM-friendly format and with parameters tuned for LLMs.


| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| objective | `str` | Yes | Natural-language description of what the web search is trying to find.
Try to make the search objective atomic, looking for a specific piece of information. May include guidance about preferred sources or freshness. |
| search_queries | `list[str]` | Yes | (optional) List of keyword search queries of 1-6
 words, which may include search operators. The search queries should be related to the
 objective. Limited to 5 entries of 200 characters each. |

**Example:**
```python
result = await app.web_search_preview(objective="example", search_queries="value")
```

### web_fetch

Purpose: Fetch and extract relevant content from
specific web URLs.

Ideal Use Cases:
- Extracting content from specific URLs you've already identified
- Exploring URLs returned by a web search in greater depth


| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| urls | `list[str]` | Yes | List of URLs to extract content from. Must be valid
HTTP/HTTPS URLs. Maximum 10 URLs per request. |
| objective | `str | None` | No | Natural-language description of what
information you're looking for from the URLs. Limit to 200 characters. |

**Example:**
```python
result = await app.web_fetch(urls="value", objective="example")
```

