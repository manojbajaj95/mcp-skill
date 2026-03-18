# mcp-skill

Turn any MCP server into a typed Python SDK.

> **Compile MCP tools into code.**

`mcp-skill` introspects an MCP server and generates a Python class where each tool becomes a typed async method.

## Before and After

### Before

Agents call MCP tools through the model loop — one round-trip per tool call:

```
llm.call_tool("web_search_preview", {"query": "..."})
# → model decides next step → calls another tool → model decides again → ...
```

### After

Agents call tools directly in code:

```python
result = await app.web_search_preview(
    objective="find latest news",
    search_queries=["topic X 2026"]
)
# Agent processes result in code — no round-trip back to model
```

## How It Works

```
┌─────────────┐      ┌───────────────┐      ┌────────────────────┐
│  MCP Server  │─────▶│  mcp-skill    │─────▶│  Generated Skill   │
│  (any URL)   │      │  CLI          │      │                    │
│              │      │               │      │  app.py            │
│  Tools:      │      │  1. Connect   │      │  ├─ Typed class    │
│  - search    │      │  2. Introspec │      │  ├─ Async methods  │
│  - fetch     │      │  3. Map types │      │  ├─ Auth + storage │
│  - ...       │      │  4. Generate  │      │  └─ JSON parsing   │
│              │      │  5. Validate  │      │                    │
└─────────────┘      └───────────────┘      │  SKILL.md          │
                                             │  └─ Agent docs     │
                                             └────────────────────┘
```

1. Connects to the MCP server using [fastmcp](https://github.com/jlowin/fastmcp)
2. Introspects all available tools via `list_tools()`
3. Converts each tool's JSON Schema into Python type annotations
4. Generates a typed `App` class where each MCP tool becomes an `async` method
5. Validates the output with `ast.parse` → `ruff` → `ty`
6. Generates `SKILL.md` with tool documentation and usage examples for agents

## Motivation

MCP servers give agents access to tools, but every tool call round-trips through the model — request tool, execute, full result back into context, decide next step. For large payloads or sequential calls, this burns tokens and adds latency.

[Programmatic Tool Calling](https://platform.claude.com/cookbook/tool-use-programmatic-tool-calling-ptc) fixes this: the agent writes code that calls tools directly, without model round-trips per invocation. Fetch, filter, aggregate — all in one code block.

**mcp-skill** makes this possible by compiling any MCP server into a plain Python class. Each tool becomes a typed async method. The agent just writes Python.

For a deeper explanation of why MCP vs. CLI is the wrong framing, see [MCP vs CLI is the Wrong Question](https://www.mbajaj.me/blog/mcp-vs-cli-is-wrong-question).

```python
from parallel_search.app import ParallelApp

app = ParallelApp(auth="sk-...")
result = await app.web_search_preview(
    objective="find latest news on topic X",
    search_queries=["topic X 2026"]
)
```

## Setup

```bash
# Install with uv
uv pip install -e .

# Or use directly without installing globally
uvx --from . mcp-skill create --url https://your-mcp-server.com/mcp --auth api-key
```

Requires [uv](https://github.com/astral-sh/uv) and Python 3.10+.

## Release Workflow

Releases are managed by `release-please`, which only considers commits on `main` that follow the Conventional Commits format.

Use commit subjects like:

```text
feat: add CLI command to inspect generated apps
fix: handle auth recovery when cached credentials are stale
chore: update release workflow docs
```

Version bump behavior:

- `feat:` creates a minor release
- `fix:` creates a patch release
- `feat!:` or a `BREAKING CHANGE:` footer creates a major release

Best practices:

- Prefer squash merges so the PR title becomes the commit on `main`
- Write PR titles in Conventional Commits format
- Keep the subject line short and imperative
- Add a short body when the change needs extra context

Optional local enforcement with `pre-commit`:

```bash
uv tool install pre-commit
pre-commit install
pre-commit install --hook-type commit-msg
```

This repo includes a `commit-msg` hook in `.pre-commit-config.yaml` that rejects non-conventional commit subjects before they are created.

If release-please says a commit "could not be parsed", push a new conventional commit to `main` and rerun the workflow.

## Usage

```bash
# Interactive mode — prompts for URL, auth type, etc.
uvx --from . mcp-skill create

# Non-interactive mode
uvx --from . mcp-skill create \
  --url https://search-mcp.parallel.ai/mcp \
  --auth api-key \
  --api-key YOUR_KEY \
  --name parallel-search \
  --non-interactive

# Generate directly into the version-controlled skills/ directory
uvx --from . mcp-skill create \
  --url https://mcp.granola.ai/mcp \
  --name granola \
  --output-dir skills \
  --non-interactive
```

### Discover Existing Apps

Use the CLI as a local catalog for both version-controlled `skills/` apps and generated `.agents/skills/` apps.

```bash
# List every discovered app
uvx --from . mcp-skill list-apps

# List callable functions for a specific app
uvx --from . mcp-skill list-functions notion

# Inspect a specific function's signature and docstring
uvx --from . mcp-skill inspect notion notion_search
```

### Use an App in Python

Once you find the app and method you need, call it from async Python:

```python
import asyncio
from sentry.app import SentryApp


async def main():
    sentry = SentryApp()
    user = await sentry.whoami()
    print(user)


asyncio.run(main())
```

All generated tool wrappers are `async`. Use them carefully with `await` inside an async function. If you skip `await`, you will get a coroutine object instead of the actual result.

### Generated Output

By default, the skill lands in `.agents/skills/<name>/` as a Python package. Pass
`--output-dir skills` when you want to generate a version-controlled built-in skill instead.

```
.agents/skills/parallel_search/
├── __init__.py
├── app.py          # Typed Python class wrapping the MCP server
└── SKILL.md        # Agent-facing docs, dependencies, and usage
```

Here's what the generated `app.py` looks like:

```python
class ParallelApp:

    def __init__(self, url: str = "https://...", auth=None) -> None:
        ...

    async def web_search_preview(
        self,
        objective: str,
        search_queries: list[str],
    ) -> dict[str, Any]:
        """Search the web with multiple queries in parallel."""
        ...

    async def fetch_url(
        self,
        url: str,
        max_length: int = None,
    ) -> dict[str, Any]:
        """Fetch and extract content from a URL."""
        ...

    def list_tools(self):
        return [self.web_search_preview, self.fetch_url]
```

Each method connects to the MCP server, calls the underlying tool, and returns parsed JSON. Auth credentials are persisted to `~/.mcp-skill/auth/` after first use — keyed by server URL, so credentials persist across restarts automatically.

## Who Is This For?

Developers building:

- **MCP-based agents** that need direct tool access without model round-trips
- **Automation systems** using MCP tools as programmatic building blocks
- **Code-execution agents** using [Programmatic Tool Calling](https://platform.claude.com/cookbook/tool-use-programmatic-tool-calling-ptc)

## Current Limitations

- **Auth**: Supports API key (Bearer or custom header), OAuth (including PKCE with either dynamic client registration or pre-registered `client_id`), and none — no mTLS
- **Runtime dependency**: Generated code depends on [fastmcp](https://github.com/jlowin/fastmcp) for MCP client connections
- **Connection per call**: Each method creates a new MCP client connection (no pooling)
- **Tools only**: MCP resources and prompts not yet supported

## Task List

Tracked improvements based on real-world usage:

- [x] **Fix output directory path** — Changed from `.agents/skill/<name>` to `.agents/skills/<name>`
- [x] **Add dependency info to SKILL.md** — Dependencies listed with `uv` and `pip` install commands
- [x] **Generate `__init__.py`** — Skill directory is a proper Python package
- [x] **Post-generation validation** — `ast.parse` → `ruff check` → `ty check` with `uvx` fallback
- [x] **Package-style imports** — Moved `app.py` to skill root; import via `from <skill>.app import <Class>`
- [x] **Persistent token storage** — FileTree-backed credential storage at `~/.mcp-skill/auth/`, keyed by server URL
- [x] **Unified auth signature** — All auth types use `auth=None` in `__init__`
- [x] **Sanitize skill names** — Hyphens/dots converted to underscores for valid Python identifiers
- [x] **Async CLI** — CLI commands are fully async via `asyncclick`
- [x] **Local app discovery** — `mcp-skill list-apps`, `mcp-skill list-functions <app>`, and `mcp-skill inspect <app> <function>`
- [ ] **Support MCP resources and prompts** — Currently only tools are introspected and generated
