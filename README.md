
# mcp-skill

Convert any MCP server into a standalone Python skill for programmatic tool calling.

**Input:** MCP server URL, auth type (API key, OAuth, none)
**Output:** A self-contained skill directory with `app.py` (typed Python class) and `SKILL.md` (agent-facing docs)

## Motivation

MCP servers are great for giving AI agents access to tools, but every tool call requires a round-trip through the model — the agent asks for a tool, the framework executes it, the full result goes back into context, and the agent decides what to do next. For tools that return large payloads or require many sequential calls, this burns tokens and adds latency.

[Programmatic Tool Calling (PTC)](https://platform.claude.com/cookbook/tool-use-programmatic-tool-calling-ptc) solves this by letting the agent write code that calls tools directly in a code execution environment, without round-tripping through the model for each invocation. The agent can fetch data, filter it, aggregate it, and only surface what matters — all in one code block.

**mcp-skill** enables this pattern by converting any MCP server into a plain Python class. Instead of an MCP protocol bridge, you get a typed `App` class with async methods — one per tool — that an agent can import and call from a script. The generated code handles connection, auth, and response parsing. The agent just writes Python.

```python
from scripts.app import ParallelApp

app = ParallelApp(api_key="...")
result = await app.web_search_preview(
    objective="find latest news on topic X",
    search_queries=["topic X 2026"]
)
# Agent processes result in code — no round-trip back to model
```

## How It Works

1. Connects to the MCP server using [fastmcp](https://github.com/jlowin/fastmcp)
2. Introspects all available tools via `list_tools()`
3. Converts each tool's JSON Schema into Python type annotations
4. Generates a typed `App` class where each MCP tool becomes an `async` method
5. Generates `SKILL.md` with tool documentation and usage examples for agents

The generated class handles auth (Bearer token, custom header, or OAuth) and response parsing (JSON or raw text). Each method creates an MCP client, calls the tool, and returns the result as a Python dict.

## Setup

```bash
# Install with uv
uv pip install -e .

# Or use directly
uv run mcp-skill create --url https://your-mcp-server.com/mcp --auth api-key
```

Uses [uv](https://github.com/astral-sh/uv) to manage Python dependencies. Requires Python 3.10+.

## Usage

```bash
# Interactive mode — prompts for URL, auth type, etc.
mcp-skill create

# Non-interactive mode
mcp-skill create \
  --url https://search-mcp.parallel.ai/mcp \
  --auth api-key \
  --api-key YOUR_KEY \
  --name parallel-search \
  --non-interactive
```

The generated skill lands in `.agents/skills/<name>/` with this structure:

```
.agents/skills/<name>/
├── scripts/
│   ├── __init__.py
│   └── app.py          # Typed Python class wrapping the MCP server
└── SKILL.md             # Agent-facing docs, dependencies, and usage instructions
```

## Current Limitations

- Only supports MCP tools (resources and prompts coming soon)
- No post-generation validation (doesn't verify the generated skill can actually call the server)
- Creates a new MCP client connection per method call (no connection reuse)

## Task List

Tracked improvements based on real-world usage:

- [x] **Fix output directory path** — Changed from `.agents/skill/<name>` to `.agents/skills/<name>` to match where agent frameworks discover skills
- [x] **Add dependency info to SKILL.md** — Dependencies are listed in SKILL.md with install commands for both uv and pip
- [x] **Generate `__init__.py` in `scripts/`** — Init file is now created so imports work reliably
- [x] **Add agent usage instructions to SKILL.md** — "How to Run" section with concrete Bash examples, preferring `uv run` with `--with` flags for automatic dependency handling
- [x] **Post-generation validation** — Runs `ast.parse` → `ruff check` → `ty check` on generated `app.py` after writing. Falls back to `uvx` if tools aren't installed locally, skips gracefully if unavailable
- [ ] **Support MCP resources and prompts** — Currently only tools are introspected and generated
