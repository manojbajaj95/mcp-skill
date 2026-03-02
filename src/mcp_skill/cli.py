"""CLI entry point for mcp-skill."""
import click


@click.group()
def main():
    """Convert any MCP server into an Agent Skill."""


@main.command()
@click.option("--url", help="MCP server URL")
@click.option("--auth", type=click.Choice(["none", "api-key", "oauth"]), default="none")
@click.option("--name", help="Skill name")
@click.option("--api-key", "api_key", help="API key for auth=api-key")
@click.option("--force", is_flag=True, help="Overwrite existing directory")
@click.option("--non-interactive", is_flag=True, help="Skip interactive prompts")
def create(url, auth, name, api_key, force, non_interactive):
    """Create an Agent Skill from an MCP server."""
    click.echo("mcp-skill create (not yet implemented)")
