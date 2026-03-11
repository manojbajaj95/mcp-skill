"""JSON Schema to Python type string conversion."""
from typing import Any
from urllib.parse import urlparse
import re
import keyword


_SIMPLE_TYPE_MAP: dict[str, str] = {
    "string": "str",
    "integer": "int",
    "number": "float",
    "boolean": "bool",
    "null": "None",
}


def schema_to_python_type(schema: dict[str, Any]) -> str:
    """Convert a JSON Schema to a Python type annotation string."""
    if not schema:
        return "Any"

    if "$ref" in schema:
        return "dict[str, Any]"

    if "enum" in schema:
        return "str"

    for key in ("anyOf", "oneOf"):
        if key in schema:
            variants = schema[key]
            null_types = [v for v in variants if v.get("type") == "null"]
            non_null = [v for v in variants if v.get("type") != "null"]
            has_none = len(null_types) > 0

            if not non_null:
                return "None"

            parts = [schema_to_python_type(v) for v in non_null]
            seen: set[str] = set()
            unique: list[str] = []
            for p in parts:
                if p not in seen:
                    seen.add(p)
                    unique.append(p)

            if has_none:
                unique.append("None")

            return " | ".join(unique)

    schema_type = schema.get("type")

    if isinstance(schema_type, list):
        null_types = [t for t in schema_type if t == "null"]
        non_null = [t for t in schema_type if t != "null"]
        has_none = len(null_types) > 0

        if not non_null:
            return "None"

        parts = [_SIMPLE_TYPE_MAP.get(t, "Any") for t in non_null]
        if has_none:
            parts.append("None")
        return " | ".join(parts)

    if isinstance(schema_type, str):
        if schema_type in _SIMPLE_TYPE_MAP:
            return _SIMPLE_TYPE_MAP[schema_type]

        if schema_type == "object":
            return "dict[str, Any]"

        if schema_type == "array":
            items = schema.get("items")
            if isinstance(items, dict):
                item_type = items.get("type")
                if isinstance(item_type, str) and item_type in _SIMPLE_TYPE_MAP:
                    return f"list[{_SIMPLE_TYPE_MAP[item_type]}]"
                return "list[Any]"
            return "list[Any]"

    return "Any"


def to_python_identifier(name: str, existing: set[str]) -> str:
    """Convert a name to a valid Python identifier."""
    safe = re.sub(r"[^a-zA-Z0-9_]", "_", name)
    if safe and safe[0].isdigit():
        safe = f"_{safe}"
    safe = safe or "_unnamed"
    if keyword.iskeyword(safe):
        safe = f"{safe}_"
    base = safe
    counter = 2
    while safe in existing:
        safe = f"{base}_{counter}"
        counter += 1
    existing.add(safe)
    return safe


def extract_params(input_schema: dict[str, Any]) -> list[dict]:
    """Extract parameter info from a tool's inputSchema."""
    properties = input_schema.get("properties", {})
    required = input_schema.get("required", [])

    params: list[dict] = []
    for prop_name, prop_schema in properties.items():
        is_required = prop_name in required
        param: dict[str, Any] = {
            "name": prop_name,
            "type": schema_to_python_type(prop_schema),
            "description": prop_schema.get("description", ""),
            "required": is_required,
        }
        if not is_required:
            param["default"] = None
        params.append(param)

    params.sort(key=lambda p: (not p["required"], p["name"]))
    return params


def derive_class_name(server_name: str) -> str:
    """Convert server name to PascalCase class name."""
    if not server_name or not server_name.strip():
        return "McpApp"
    
    words = re.split(r'[\s\-_\.]+', server_name.strip())
    words = [word.capitalize() for word in words if word]
    
    if not words:
        return "McpApp"
    
    name = ''.join(words) + "App"
    # Ensure the name is a valid Python identifier (can't start with a digit)
    if name and name[0].isdigit():
        name = "Mcp" + name
    return name


def derive_module_name(skill_name: str) -> str:
    """Convert a skill name to a valid Python module/folder name."""
    if not skill_name or not skill_name.strip():
        return "mcp_skill"

    name = re.sub(r'[^a-zA-Z0-9_]', '_', skill_name.strip())
    name = re.sub(r'_+', '_', name)
    name = name.strip('_').lower()

    if not name:
        return "mcp_skill"
    if name[0].isdigit():
        name = f"mcp_{name}"
    if keyword.iskeyword(name):
        name = f"{name}_"

    return name


def derive_skill_name(server_name: str) -> str:
    """Convert server name to agentskills.io-compliant skill name."""
    if not server_name or not server_name.strip():
        return "mcp-skill"
    
    name = server_name.lower()
    name = re.sub(r'[\s_\.]+', '-', name)
    name = re.sub(r'[^a-z0-9-]', '', name)
    name = re.sub(r'-+', '-', name)
    name = name.strip('-')
    
    if len(name) > 64:
        name = name[:64].rstrip('-')
    
    if not name:
        return "mcp-skill"
    
    return name


def derive_skill_name_from_url(url: str) -> str:
    """Derive a skill name from an MCP server URL."""
    try:
        parsed = urlparse(url)
        # Use the hostname, stripping common prefixes like "api." or "mcp."
        host = parsed.hostname or ""
        host = re.sub(r"^(api|mcp|www)\.", "", host)
        # Strip TLD (last segment)
        parts = host.split(".")
        base = parts[0] if parts else host
        if parsed.path and parsed.path.strip("/"):
            path_segment = parsed.path.strip("/").split("/")[0]
            base = f"{base}-{path_segment}"
        return derive_skill_name(base)
    except Exception:
        return "mcp-skill"


def generate_skill_description(server_name: str, tools: list) -> str:
    """Generate a description for the skill."""
    if not tools:
        return f"MCP skill for {server_name}. No tools available."
    
    tool_names = [tool.name for tool in tools]
    tool_count = len(tool_names)
    
    base = f"MCP skill for {server_name}. Provides {tool_count} tools: "
    tools_str = ", ".join(tool_names)
    full_desc = base + tools_str
    
    if len(full_desc) > 1024:
        max_tools_len = 1024 - len(base) - 3
        if max_tools_len <= 0:
            return full_desc[:1021] + "..."
        
        tools_list = []
        current_len = 0
        for name in tool_names:
            sep_len = 2 if tools_list else 0
            if current_len + sep_len + len(name) <= max_tools_len:
                tools_list.append(name)
                current_len += sep_len + len(name)
            else:
                break
        
        tools_str = ", ".join(tools_list) + "..."
        full_desc = base + tools_str
    
    return full_desc
