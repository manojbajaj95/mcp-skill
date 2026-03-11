# Agent Instructions — mcp-skill

This file provides context for AI coding agents working on the `mcp-skill` project.

## Project Overview

`mcp-skill` is a CLI tool that turns any MCP server into a typed Python SDK. It connects to an MCP server, introspects tools, and generates a Python `App` class where each tool becomes a typed `async` method.

## Development Setup

```bash
# Create and activate the virtual environment
uv sync

# Run the CLI
uv run mcp-skill create --url <url>
```

## Key Files

| File | Purpose |
|------|---------|
| `src/mcp_skill/cli.py` | CLI entry point (asyncclick-based, fully async) |
| `src/mcp_skill/introspector.py` | Connects to MCP server, lists tools |
| `src/mcp_skill/generator.py` | Generates `app.py` and `SKILL.md` via Jinja2 |
| `src/mcp_skill/type_mapper.py` | JSON Schema → Python type conversion, URL utilities |
| `src/mcp_skill/validator.py` | Validates generated code via ast/ruff/ty |
| `src/mcp_skill/auth/` | Auth implementations (Bearer, ApiKey, OAuth, ClientCredentials) |
| `src/mcp_skill/templates/` | Jinja2 templates for generated files |

## Architecture

```
CLI (asyncclick)
  → introspector.connect_and_list_tools()   # MCP connection
  → generator.generate_app_py()              # Code generation
  → generator.generate_skill_md()            # Doc generation
  → validator.validate_generated_code()      # Validation
  → writes to .agents/skills/<module_name>/
```

## Auth Storage

All credentials are stored in `~/.mcp-skill/auth/` using `FileTreeStore` (from `py-key-value-aio[filetree]`). Keys are namespaced by server URL:

- Bearer/ApiKey tokens: `<server_url>/api_key`
- OAuth tokens: `<server_url>/tokens` and `<server_url>/client_info` (managed by fastmcp)
- Client Credentials tokens: `<token_url>/cc_token`

## Generated Output

Skills land in `.agents/skills/<module_name>/` (excluded from git via `.gitignore`):

```
.agents/skills/<module_name>/
├── __init__.py
├── app.py      # Typed Python class
└── SKILL.md    # Agent-facing documentation
```

## Conventions

- Use `asyncclick` for the CLI — all commands are `async def`
- Use `Path` objects throughout, never `os.path.join`
- Auth classes use `server_url` (not `skill_name`) for storage namespacing
- `type_mapper.py` is the canonical place for URL parsing utilities (see `extract_server_name_from_url`)
- Pre-built example skills live in `skills/` (version-controlled); generated skills go to `.agents/skills/` (gitignored)

## Release

Release-please configs are in `.github/release/`. The workflow in `.github/workflows/release.yml` handles automated changelog and PyPI publishing.
