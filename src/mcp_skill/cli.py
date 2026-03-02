"""CLI entry point for mcp-skill."""
import asyncio
import os
import sys

import click

from mcp_skill.introspector import connect_and_list_tools
from mcp_skill.generator import generate_app_py, generate_skill_md
from mcp_skill.type_mapper import derive_class_name, derive_skill_name, generate_skill_description


@click.group()
def main():
    """Convert any MCP server into an Agent Skill."""


@main.command()
@click.option("--url", help="MCP server URL")
@click.option("--auth", type=click.Choice(["none", "api-key", "oauth"]), default="none", help="Authentication type")
@click.option("--name", help="Skill name (auto-detected if not provided)")
@click.option("--api-key", "api_key", help="API key (when auth=api-key)")
@click.option("--force", is_flag=True, help="Overwrite existing directory")
@click.option("--non-interactive", is_flag=True, help="Skip interactive prompts")
@click.option("--app-name", "app_name", default=None, help="App class base name (e.g. 'Fetch' → FetchApp)")
def create(url, auth, name, api_key, force, non_interactive, app_name):
    """Create an Agent Skill from an MCP server."""
    try:
        # Gather inputs - interactive or from flags
        if non_interactive:
            if not url:
                click.echo("Error: --url is required in non-interactive mode", err=True)
                sys.exit(1)
        else:
            # Interactive prompts
            if not url:
                url = click.prompt("MCP Server URL")
            if auth == "none":
                auth_choice = click.prompt(
                    "Authentication type",
                    type=click.Choice(["none", "api-key", "oauth"]),
                    default="none",
                )
                auth = auth_choice

        # Get API key if needed
        if auth == "api-key" and not api_key:
            if non_interactive:
                click.echo("Error: --api-key is required when auth=api-key in non-interactive mode", err=True)
                sys.exit(1)
            api_key = click.prompt("API Key", hide_input=True)

        # Build auth string for introspector
        auth_str = None
        if auth == "api-key" and api_key:
            auth_str = api_key
        elif auth == "oauth":
            auth_str = "oauth"

        # Connect and discover tools
        click.echo(f"Connecting to {url}...")
        try:
            server_name, tools = asyncio.run(connect_and_list_tools(url, auth_str))
        except (ConnectionError, RuntimeError) as e:
            click.echo(f"Error: {e}", err=True)
            sys.exit(1)

        click.echo(f"Found {len(tools)} tools:")
        for tool in tools:
            desc = (tool.description or "")[:60]
            click.echo(f"  - {tool.name}: {desc}")

        if not tools:
            click.echo("Warning: Server has 0 tools. Generating minimal skill.")

        # Determine skill name
        if not name:
            default_name = derive_skill_name(server_name)
            if non_interactive:
                name = default_name
            else:
                name = click.prompt("Skill name", default=default_name)
        else:
            name = derive_skill_name(name)

        # Determine app class name
        if not app_name:
            if non_interactive:
                app_name = server_name
            else:
                default_app = server_name.capitalize()
                app_name = click.prompt("App name (base name, 'App' suffix added automatically)", default=default_app)

        # Check if directory exists
        if os.path.exists(name):
            if not force:
                if non_interactive:
                    click.echo(f"Error: Directory '{name}' already exists. Use --force to overwrite.", err=True)
                    sys.exit(1)
                if not click.confirm(f"Directory '{name}' exists. Overwrite?"):
                    click.echo("Aborted.")
                    sys.exit(0)

        # Generate class name and description
        class_name = derive_class_name(app_name)
        description = generate_skill_description(server_name, tools)

        click.echo("Generating skill...")

        # Generate code
        app_code = generate_app_py(class_name, url, tools)
        skill_md = generate_skill_md(name, description, tools, class_name)

        # Write output files
        os.makedirs(os.path.join(name, "scripts"), exist_ok=True)

        with open(os.path.join(name, "scripts", "app.py"), "w") as f:
            f.write(app_code)

        with open(os.path.join(name, "SKILL.md"), "w") as f:
            f.write(skill_md)

        click.echo(f"Skill generated at ./{name}/")
        click.echo(f"  {name}/scripts/app.py")
        click.echo(f"  {name}/SKILL.md")

    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)
