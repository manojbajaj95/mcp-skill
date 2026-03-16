"""Code generation for app.py and SKILL.md via Jinja2 templates."""
from pathlib import Path
from typing import Any

from jinja2 import Environment, FileSystemLoader

from mcp_skill.type_mapper import (
    schema_to_python_type,
    to_python_identifier,
    extract_params,
)

_TEMPLATE_DIR = Path(__file__).parent / "templates"
_env = Environment(
    loader=FileSystemLoader(str(_TEMPLATE_DIR)),
    keep_trailing_newline=True,
    lstrip_blocks=True,
    trim_blocks=True,
)


def _generate_tags(tool_name: str) -> str:
    words = tool_name.replace("-", "_").split("_")
    skip = {"get", "set", "the", "a", "an", "is", "to", "for", "of", "in", "on", "by"}
    tags = [w.lower() for w in words if w.lower() not in skip and len(w) > 1]
    return ", ".join(tags) if tags else tool_name


def _build_method_signature(method_name: str, params: list[dict]) -> str:
    parts = ["self"]
    for p in params:
        if p["required"]:
            parts.append(f"{p['name']}: {p['type']}")
        else:
            parts.append(f"{p['name']}: {p['type']} = None")
    return ", ".join(parts)


def _build_example_args(properties: dict[str, Any]) -> str:
    example_args = []
    for pn in list(properties.keys())[:3]:
        ps = properties[pn]
        pt = ps.get("type", "string")
        if pt == "string":
            example_args.append(f'{pn}="example"')
        elif pt == "integer":
            example_args.append(f"{pn}=1")
        elif pt == "number":
            example_args.append(f"{pn}=1.0")
        elif pt == "boolean":
            example_args.append(f"{pn}=True")
        else:
            example_args.append(f'{pn}="value"')
    return ", ".join(example_args)


def _prepare_methods(tools: list) -> tuple[list[dict], str]:
    existing_names: set[str] = set()
    methods = []

    for tool in tools:
        method_name = to_python_identifier(tool.name, existing_names)
        params = extract_params(tool.inputSchema or {})

        methods.append({
            "name": method_name,
            "tool_name": tool.name,
            "signature": _build_method_signature(method_name, params),
            "description": tool.description or "Execute this tool.",
            "params": [
                {
                    "name": p["name"],
                    "type": p["type"],
                    "doc": p.get("description") or "No description",
                    "required": p["required"],
                }
                for p in params
            ],
            "tags": _generate_tags(tool.name),
        })

    method_refs = ", ".join(f"self.{m['name']}" for m in methods)
    return methods, method_refs


def _prepare_tool_docs(tools: list) -> list[dict]:
    docs = []
    for tool in tools:
        input_schema = tool.inputSchema or {}
        properties = input_schema.get("properties", {})
        required = input_schema.get("required", [])
        safe_method = tool.name.replace("-", "_").replace(".", "_")

        docs.append({
            "name": tool.name,
            "description": tool.description or "No description available.",
            "safe_method": safe_method,
            "example_args": _build_example_args(properties),
            "params": [
                {
                    "name": pn,
                    "type": schema_to_python_type(ps),
                    "required": pn in required,
                    "description": ps.get("description", ""),
                }
                for pn, ps in properties.items()
            ],
        })
    return docs


def _python_literal(value: Any) -> str:
    return repr(value)


def generate_app_py(
    class_name: str,
    server_url: str,
    tools: list,
    auth_type: str = "none",
    auth_header: str | None = None,
    oauth_client_id: str | None = None,
    oauth_scopes: str | list[str] | None = None,
    oauth_client_metadata_url: str | None = None,
    skill_name: str | None = None,
    module_name: str | None = None,
) -> str:
    methods, method_refs = _prepare_methods(tools)

    if tools:
        tool_summary = ", ".join(t.name for t in tools[:5])
        if len(tools) > 5:
            tool_summary += f" and {len(tools) - 5} more"
        brief = f"interact with tools: {tool_summary}"
    else:
        brief = "interact with the MCP server"

    template = _env.get_template("app.py.j2")
    code = template.render(
        class_name=class_name,
        base_name=class_name.replace("App", ""),
        server_url=server_url,
        auth_type=auth_type,
        auth_header=auth_header,
        oauth_client_id_literal=_python_literal(oauth_client_id),
        oauth_scopes_literal=_python_literal(oauth_scopes),
        oauth_client_metadata_url_literal=_python_literal(oauth_client_metadata_url),
        skill_name=skill_name,
        module_name=module_name or skill_name,
        brief=brief,
        methods=methods,
        method_refs=method_refs,
    )

    return code


def _compute_dependencies(auth_type: str) -> list[str]:
    return ["mcp-skill"]


def generate_skill_md(
    skill_name: str,
    description: str,
    tools: list,
    class_name: str = "App",
    auth_type: str = "none",
    auth_header: str | None = None,
    oauth_client_id: str | None = None,
    oauth_scopes: str | list[str] | None = None,
    oauth_client_metadata_url: str | None = None,
    module_name: str | None = None,
    short_description: str | None = None,
) -> str:
    if len(description) > 1024:
        description = description[:1021] + "..."

    tool_docs = _prepare_tool_docs(tools)
    dependencies = _compute_dependencies(auth_type)

    template = _env.get_template("skill.md.j2")
    content = template.render(
        skill_name=skill_name,
        module_name=module_name or skill_name,
        description=description,
        short_description=short_description or skill_name,
        class_name=class_name,
        auth_type=auth_type,
        auth_header=auth_header,
        oauth_client_id=oauth_client_id,
        oauth_scopes=oauth_scopes,
        oauth_client_metadata_url=oauth_client_metadata_url,
        tools=tool_docs,
        dependencies=dependencies,
    )

    content_lines = content.split("\n")
    if len(content_lines) > 498:
        content = "\n".join(content_lines[:498])
        content += "\n\n*...additional tools omitted for brevity*\n"

    return content
