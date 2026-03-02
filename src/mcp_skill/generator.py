"""Code generation for app.py and SKILL.md."""
import ast
from typing import Any

from mcp_skill.type_mapper import (
    schema_to_python_type,
    to_python_identifier,
    extract_params,
)


def _generate_tags(tool_name: str) -> str:
    """Generate comma-separated tags from tool name."""
    words = tool_name.replace("-", "_").split("_")
    skip = {"get", "set", "the", "a", "an", "is", "to", "for", "of", "in", "on", "by"}
    tags = [w.lower() for w in words if w.lower() not in skip and len(w) > 1]
    return ", ".join(tags) if tags else tool_name


def _build_method_signature(method_name: str, params: list[dict]) -> str:
    """Build method signature string."""
    parts = ["self"]
    for p in params:
        if p["required"]:
            parts.append(f"{p['name']}: {p['type']}")
        else:
            parts.append(f"{p['name']}: {p['type']} = None")
    return ", ".join(parts)


def _build_call_args(params: list[dict]) -> str:
    """Build the dict argument for call_tool."""
    if not params:
        return "{}"
    lines = []
    for p in params:
        lines.append(f'            "{p["name"]}": {p["name"]},')
    return "{\n" + "\n".join(lines) + "\n        }"


def _build_docstring(description: str, params: list[dict], tags: str, indent: str = "        ") -> str:
    """Build a method docstring."""
    lines = [f'{indent}"""']
    lines.append(f"{indent}{description or 'Execute this tool.'}")
    lines.append(f"{indent}")
    if params:
        lines.append(f"{indent}Args:")
        for p in params:
            desc = p.get("description", "") or "No description"
            lines.append(f"{indent}    {p['name']}: {desc}")
        lines.append(f"{indent}")
    lines.append(f"{indent}Returns:")
    lines.append(f"{indent}    Tool execution result")
    lines.append(f"{indent}")
    lines.append(f"{indent}Tags:")
    lines.append(f"{indent}    {tags}")
    lines.append(f'{indent}"""')
    return "\n".join(lines)


def generate_app_py(class_name: str, server_url: str, tools: list) -> str:
    """Generate app.py source code."""
    existing_names: set[str] = set()
    methods = []
    method_names = []

    for tool in tools:
        method_name = to_python_identifier(tool.name, existing_names)
        method_names.append(method_name)
        params = extract_params(tool.inputSchema or {})
        sig = _build_method_signature(method_name, params)
        tags = _generate_tags(tool.name)
        docstring = _build_docstring(tool.description or "", params, tags)
        call_args = _build_call_args(params)

        # Build call_args dict, filtering out None values for optional params
        call_args_lines = ["        call_args = {}"]
        for p in params:
            param_name = p["name"]
            if p["required"]:
                call_args_lines.append(f'        call_args["{param_name}"] = {param_name}')
            else:
                call_args_lines.append(f'        if {param_name} is not None: call_args["{param_name}"] = {param_name}')

        method_lines = [
            f"    async def {method_name}({sig}) -> dict[str, Any]:",
            docstring,
        ]
        method_lines.extend(call_args_lines)
        method_lines.extend([
            f'        result = await self._client.call_tool("{tool.name}", call_args)',
            "        texts = []",
            "        for block in result.content:",
            '            if hasattr(block, "text"):',
            "                texts.append(block.text)",
            '        text = "\\n".join(texts)',
            "        try:",
            "            return json.loads(text)",
            "        except (json.JSONDecodeError, TypeError):",
            '            return {"result": text}',
        ])
        methods.append("\n".join(method_lines))

    if method_names:
        tool_refs = ", ".join(f"self.{name}" for name in method_names)
        list_tools_method = f"    def list_tools(self):\n        return [{tool_refs}]"
    else:
        list_tools_method = "    def list_tools(self):\n        return []"

    if tools:
        tool_summary = ", ".join(t.name for t in tools[:5])
        if len(tools) > 5:
            tool_summary += f" and {len(tools) - 5} more"
        brief = f"interact with tools: {tool_summary}"
    else:
        brief = "interact with the MCP server"

    lines = [
        f'"""Application for interacting with {class_name.replace("App", "")} via MCP."""',
        "from typing import Any",
        "from fastmcp import Client",
        "import json",
        "",
        "",
        f"class {class_name}:",
        '    """',
        f"    Application for interacting with {class_name.replace('App', '')} via MCP.",
        f"    Provides tools to {brief}.",
        '    """',
        "",
        f'    def __init__(self, url: str = "{server_url}", auth: str | None = None) -> None:',
        "        self.url = url",
        "        self.auth = auth",
        "        self._client: Client | None = None",
        "",
        "    async def __aenter__(self):",
        '        if self.auth and self.auth.lower() not in ("none", ""):',
        "            self._client = Client(self.url, auth=self.auth)",
        "        else:",
        "            self._client = Client(self.url)",
        "        await self._client.__aenter__()",
        "        return self",
        "",
        "    async def __aexit__(self, *args):",
        "        if self._client:",
        "            await self._client.__aexit__(*args)",
        "        self._client = None",
        "",
    ]

    for method in methods:
        lines.append(method)
        lines.append("")

    lines.append(list_tools_method)
    lines.append("")

    code = "\n".join(lines)

    try:
        ast.parse(code)
    except SyntaxError as e:
        raise ValueError(f"Generated code has syntax error: {e}") from e

    return code


def generate_skill_md(skill_name: str, description: str, tools: list) -> str:
    """Generate SKILL.md content."""
    from mcp_skill.type_mapper import schema_to_python_type

    if len(description) > 1024:
        description = description[:1021] + "..."

    lines = []
    safe_desc = description.replace('"', '\\"')
    lines.append("---")
    lines.append(f"name: {skill_name}")
    lines.append(f'description: "{safe_desc}"')
    lines.append("---")
    lines.append("")

    lines.append(f"# {skill_name}")
    lines.append("")
    lines.append(description)
    lines.append("")

    lines.append("## Quick Start")
    lines.append("")
    lines.append("```python")
    lines.append("from scripts.app import *")
    lines.append("")
    lines.append("# Use as async context manager")
    lines.append("async with App() as app:")
    lines.append("    tools = app.list_tools()")
    lines.append("    # Call any tool method")
    lines.append("```")
    lines.append("")

    if tools:
        lines.append("## Available Tools")
        lines.append("")
        for tool in tools:
            tool_name = tool.name
            tool_desc = tool.description or "No description available."
            lines.append(f"### {tool_name}")
            lines.append("")
            lines.append(tool_desc)
            lines.append("")
            input_schema = tool.inputSchema or {}
            properties = input_schema.get("properties", {})
            required = input_schema.get("required", [])
            if properties:
                lines.append("| Parameter | Type | Required | Description |")
                lines.append("|-----------|------|----------|-------------|")
                for param_name, param_schema in properties.items():
                    param_type = schema_to_python_type(param_schema)
                    is_req = "Yes" if param_name in required else "No"
                    param_desc = param_schema.get("description", "")
                    lines.append(f"| {param_name} | `{param_type}` | {is_req} | {param_desc} |")
                lines.append("")
            lines.append("**Example:**")
            lines.append("```python")
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
            safe_method = tool_name.replace("-", "_").replace(".", "_")
            args_str = ", ".join(example_args)
            lines.append(f"result = await app.{safe_method}({args_str})")
            lines.append("```")
            lines.append("")
    else:
        lines.append("## Available Tools")
        lines.append("")
        lines.append("No tools available.")
        lines.append("")

    content = "\n".join(lines)
    if content.count("\n") > 498:
        content_lines = content.split("\n")
        content = "\n".join(content_lines[:498])
        content += "\n\n*...additional tools omitted for brevity*\n"

    return content
