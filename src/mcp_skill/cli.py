"""CLI entry point for mcp-skill."""

import asyncio
import sys
from pathlib import Path

import asyncclick as click

from mcp_skill.catalog import discover_apps, find_method, get_app
from mcp_skill.introspector import connect_and_list_tools
from mcp_skill.generator import generate_app_py, generate_skill_md
from mcp_skill.type_mapper import (
    derive_class_name,
    derive_module_name,
    derive_skill_name,
    derive_skill_name_from_url,
    generate_skill_description,
    generate_skill_short_description,
)
from mcp_skill.validator import validate_generated_code


@click.group()
async def main():
    """Convert any MCP server into an Agent Skill."""


@main.command(name="list-apps")
async def list_apps():
    """List all discovered apps."""

    apps = discover_apps()
    if not apps:
        click.echo("No app.py classes found in skills/ or .agents/skills/.", err=True)
        sys.exit(1)

    click.echo("Listing apps")
    click.echo(f"Apps found: {len(apps)}")
    click.echo("")
    for app in sorted(apps.values(), key=lambda item: item.name):
        click.echo(
            f"  - {app.name}: {app.class_name} "
            f"({len(app.methods)} functions, {app.source_label})"
        )


@main.command(name="list-functions")
@click.argument("app_name")
async def list_functions(app_name):
    """List functions for a specific app."""

    app = get_app(app_name)
    if app is None:
        click.echo(f"Error: App '{app_name}' not found.", err=True)
        sys.exit(1)

    click.echo(f"Listing functions for app: {app.name}")
    click.echo(f"Class: {app.class_name}")
    click.echo(f"Path: {app.app_path}")
    click.echo(f"Matched app: {app.name}")
    click.echo(f"Functions found: {len(app.methods)}")
    click.echo("")
    for method in app.methods:
        summary = method.docstring.strip().splitlines()[0]
        click.echo(f"  - {method.signature}")
        click.echo(f"    {summary}")


@main.command()
@click.argument("app_name")
@click.argument("function_name")
async def inspect(app_name, function_name):
    """Inspect a function on a discovered app."""

    app = get_app(app_name)
    if app is None:
        click.echo(f"Error: App '{app_name}' not found.", err=True)
        sys.exit(1)

    method = find_method(app, function_name)
    if method is None:
        click.echo(
            f"Error: Function '{function_name}' not found in app '{app.name}'.",
            err=True,
        )
        sys.exit(1)

    click.echo(f"App: {app.name}")
    click.echo(f"Class: {app.class_name}")
    click.echo(f"Path: {app.app_path}:{method.line}")
    click.echo(f"Function: {method.name}")
    click.echo(f"Signature: {method.signature}")
    click.echo("")
    click.echo("Description:")
    click.echo(method.docstring.strip())


@main.command()
@click.option("--url", help="MCP server URL")
@click.option(
    "--auth",
    type=click.Choice(["none", "api-key", "oauth"]),
    default="none",
    help="Authentication type",
)
@click.option("--name", help="Skill name (auto-detected if not provided)")
@click.option("--api-key", "api_key", help="API key (when auth=api-key)")
@click.option(
    "--oauth-client-id",
    "oauth_client_id",
    default=None,
    help="Pre-registered OAuth client ID for PKCE/public-client flows",
)
@click.option(
    "--oauth-client-secret",
    "oauth_client_secret",
    default=None,
    help="Optional OAuth client secret for static clients",
)
@click.option(
    "--oauth-scopes",
    "oauth_scopes",
    default=None,
    help="Optional space-separated OAuth scopes",
)
@click.option(
    "--oauth-client-metadata-url",
    "oauth_client_metadata_url",
    default=None,
    help="Optional hosted client metadata URL to use instead of dynamic client registration",
)
@click.option(
    "--auth-header",
    "auth_header",
    default=None,
    help="Header name for API key (e.g. 'x-api-key'). Omit for Bearer token.",
)
@click.option("--force", is_flag=True, help="Overwrite existing directory")
@click.option("--non-interactive", is_flag=True, help="Skip interactive prompts")
@click.option(
    "--app-name",
    "app_name",
    default=None,
    help="App class base name (e.g. 'Fetch' → FetchApp)",
)
async def create(
    url,
    auth,
    name,
    api_key,
    oauth_client_id,
    oauth_client_secret,
    oauth_scopes,
    oauth_client_metadata_url,
    auth_header,
    force,
    non_interactive,
    app_name,
):
    """Create an Agent Skill from an MCP server."""
    # Generation order:
    # 1. Ask/resolve URL
    # 2. Derive and confirm skill name from URL
    # 3. Derive and confirm app name from skill name
    # 4. Resolve auth type (using skill name for token storage)
    # 5. Connect and list tools
    # 6. Generate app.py and skill.md
    # 7. Run validation on generated code
    try:
        # Step 1: Resolve URL
        if non_interactive:
            if not url:
                click.echo("Error: --url is required in non-interactive mode", err=True)
                sys.exit(1)
        else:
            if not url:
                url = await click.prompt("MCP Server URL")

        # Step 2: Derive and confirm skill name from URL
        url_derived_name = derive_skill_name_from_url(url)
        if not name:
            if non_interactive:
                name = url_derived_name
            else:
                name = await click.prompt("Skill name", default=url_derived_name)
        else:
            name = derive_skill_name(name)

        # Step 3: Derive and confirm app name from skill name
        if not app_name:
            default_app = name.replace("-", " ").title().replace(" ", "")
            if non_interactive:
                app_name = default_app
            else:
                app_name = await click.prompt(
                    "App name (base name, 'App' suffix added automatically)",
                    default=default_app,
                )

        # Step 4: Resolve auth type, using skill name for token storage
        if not non_interactive and auth == "none":
            auth = await click.prompt(
                "Authentication type",
                type=click.Choice(["none", "api-key", "oauth"]),
                default="none",
            )

        if auth == "api-key" and not api_key:
            if non_interactive:
                click.echo(
                    "Error: --api-key is required when auth=api-key in non-interactive mode",
                    err=True,
                )
                sys.exit(1)
            api_key = await click.prompt("API Key", hide_input=True)
        elif auth == "oauth" and not non_interactive:
            if oauth_client_id is None:
                oauth_client_id = await click.prompt(
                    "OAuth client ID (leave blank to use dynamic client registration)",
                    default="",
                    show_default=False,
                )
            if oauth_client_id == "":
                oauth_client_id = None

            if oauth_scopes is None:
                oauth_scopes = await click.prompt(
                    "OAuth scopes (optional, space-separated)",
                    default="",
                    show_default=False,
                )
            if oauth_scopes == "":
                oauth_scopes = None

            if oauth_client_id and oauth_client_secret is None:
                oauth_client_secret = await click.prompt(
                    "OAuth client secret (optional)",
                    default="",
                    hide_input=True,
                    show_default=False,
                )
            if oauth_client_secret == "":
                oauth_client_secret = None

            if oauth_client_id and oauth_client_metadata_url is None:
                oauth_client_metadata_url = await click.prompt(
                    "OAuth client metadata URL (optional)",
                    default="",
                    show_default=False,
                )
            if oauth_client_metadata_url == "":
                oauth_client_metadata_url = None

        auth_str = None
        headers: dict[str, str] | None = None
        if auth == "api-key" and api_key:
            if auth_header:
                headers = {auth_header: api_key}
                auth_type = "header"
            else:
                auth_str = api_key
                auth_type = "bearer"
        elif auth == "oauth":
            auth_str = "oauth"
            auth_type = "oauth"
        else:
            auth_type = "none"

        # Step 5: Connect and list tools
        click.echo(f"Connecting to {url}...")
        try:
            server_name, tools = await connect_and_list_tools(
                url,
                auth_str,
                headers=headers,
                oauth_client_id=oauth_client_id,
                oauth_client_secret=oauth_client_secret,
                oauth_scopes=oauth_scopes,
                oauth_client_metadata_url=oauth_client_metadata_url,
            )
        except (ConnectionError, RuntimeError) as e:
            click.echo(f"Error: {e}", err=True)
            sys.exit(1)

        click.echo(f"Found {len(tools)} tools:")
        for tool in tools:
            desc = (tool.description or "")[:60]
            click.echo(f"  - {tool.name}: {desc}")

        if not tools:
            click.echo("Warning: Server has 0 tools. Generating minimal skill.")

        module_name = derive_module_name(name)
        output_dir = Path(".agents") / "skills" / module_name
        if output_dir.exists():
            if not force:
                if non_interactive:
                    click.echo(
                        f"Error: Directory '{output_dir}' already exists. Use --force to overwrite.",
                        err=True,
                    )
                    sys.exit(1)
                if not click.confirm(f"Directory '{output_dir}' exists. Overwrite?"):
                    click.echo("Aborted.")
                    sys.exit(0)

        # Generate class name and description
        class_name = derive_class_name(app_name)
        description = generate_skill_description(server_name, tools)
        short_description = generate_skill_short_description(server_name)

        click.echo("Generating skill...")

        app_code = generate_app_py(
            class_name,
            url,
            tools,
            auth_type=auth_type,
            auth_header=auth_header,
            oauth_client_id=oauth_client_id,
            oauth_scopes=oauth_scopes,
            oauth_client_metadata_url=oauth_client_metadata_url,
            skill_name=name,
            module_name=module_name,
        )
        skill_md = generate_skill_md(
            name,
            description,
            tools,
            class_name,
            auth_type=auth_type,
            auth_header=auth_header,
            oauth_client_id=oauth_client_id,
            oauth_scopes=oauth_scopes,
            oauth_client_metadata_url=oauth_client_metadata_url,
            module_name=module_name,
            short_description=short_description,
        )

        output_dir.mkdir(parents=True, exist_ok=True)

        await asyncio.gather(
            asyncio.to_thread((output_dir / "__init__.py").write_text, ""),
            asyncio.to_thread((output_dir / "app.py").write_text, app_code),
            asyncio.to_thread((output_dir / "SKILL.md").write_text, skill_md),
        )

        app_py_path = output_dir / "app.py"
        click.echo("Validating generated code...")
        report = validate_generated_code(app_py_path)
        click.echo(report.summary())

        if not report.passed:
            click.echo(
                "\nWarning: Validation found issues. The skill was still generated but may need fixes.",
                err=True,
            )

        click.echo(f"\nSkill generated at ./{output_dir}/")
        click.echo(f"  {output_dir}/app.py")
        click.echo(f"  {output_dir}/SKILL.md")

    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)
