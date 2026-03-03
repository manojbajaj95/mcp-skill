"""CLI entry point for mcp-skill."""
import asyncio
import os
import sys

import click

from pathlib import Path

from mcp_skill.introspector import connect_and_list_tools
from mcp_skill.generator import generate_app_py, generate_skill_md
from mcp_skill.type_mapper import derive_class_name, derive_skill_name, generate_skill_description
from mcp_skill.validator import validate_generated_code


@click.group()
def main():
    """Convert any MCP server into an Agent Skill."""


@main.command()
@click.option("--url", help="MCP server URL")
@click.option("--auth", type=click.Choice(["none", "api-key", "oauth"]), default="none", help="Authentication type")
@click.option("--name", help="Skill name (auto-detected if not provided)")
@click.option("--api-key", "api_key", help="API key (when auth=api-key)")
@click.option("--auth-header", "auth_header", default=None, help="Header name for API key (e.g. 'x-api-key'). Omit for Bearer token.")
@click.option("--force", is_flag=True, help="Overwrite existing directory")
@click.option("--non-interactive", is_flag=True, help="Skip interactive prompts")
@click.option("--app-name", "app_name", default=None, help="App class base name (e.g. 'Fetch' → FetchApp)")
def create(url, auth, name, api_key, auth_header, force, non_interactive, app_name):
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

        click.echo(f"Connecting to {url}...")
        try:
            server_name, tools = asyncio.run(
                connect_and_list_tools(url, auth_str, headers=headers)
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

        output_dir = os.path.join(".agents", "skills", name)
        if os.path.exists(output_dir):
            if not force:
                if non_interactive:
                    click.echo(f"Error: Directory '{output_dir}' already exists. Use --force to overwrite.", err=True)
                    sys.exit(1)
                if not click.confirm(f"Directory '{output_dir}' exists. Overwrite?"):
                    click.echo("Aborted.")
                    sys.exit(0)

        # Generate class name and description
        class_name = derive_class_name(app_name)
        description = generate_skill_description(server_name, tools)

        click.echo("Generating skill...")

        app_code = generate_app_py(
            class_name, url, tools,
            auth_type=auth_type, auth_header=auth_header,
        )
        skill_md = generate_skill_md(
            name, description, tools, class_name,
            auth_type=auth_type, auth_header=auth_header,
        )

        scripts_dir = os.path.join(output_dir, "scripts")
        os.makedirs(scripts_dir, exist_ok=True)

        with open(os.path.join(scripts_dir, "__init__.py"), "w") as f:
            f.write("")

        with open(os.path.join(scripts_dir, "app.py"), "w") as f:
            f.write(app_code)

        with open(os.path.join(output_dir, "SKILL.md"), "w") as f:
            f.write(skill_md)

        app_py_path = Path(scripts_dir) / "app.py"
        click.echo("Validating generated code...")
        report = validate_generated_code(app_py_path)
        click.echo(report.summary())

        if not report.passed:
            click.echo("\nWarning: Validation found issues. The skill was still generated but may need fixes.", err=True)

        click.echo(f"\nSkill generated at ./{output_dir}/")
        click.echo(f"  {output_dir}/scripts/app.py")
        click.echo(f"  {output_dir}/SKILL.md")

    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)
