"""Local skill catalog and inspection helpers for the CLI."""

from __future__ import annotations

import ast
import warnings
from dataclasses import dataclass
from pathlib import Path


@dataclass(slots=True)
class MethodInfo:
    """Metadata for an app method parsed from app.py."""

    name: str
    signature: str
    docstring: str
    line: int


@dataclass(slots=True)
class AppInfo:
    """Metadata for a discovered app."""

    name: str
    class_name: str
    app_path: Path
    source_root: Path
    methods: list[MethodInfo]

    @property
    def source_label(self) -> str:
        if self.source_root == Path("skills"):
            return "built-in"
        if self.source_root == Path(".agents") / "skills":
            return "generated"
        return str(self.source_root)


def discover_apps(base_dir: Path | None = None) -> dict[str, AppInfo]:
    """Discover app.py classes from versioned and generated skill directories."""

    root_dir = (base_dir or Path.cwd()).resolve()
    app_roots = [root_dir / "skills", root_dir / ".agents" / "skills"]
    apps: dict[str, AppInfo] = {}

    for app_root in app_roots:
        if not app_root.exists():
            continue

        for app_path in sorted(app_root.glob("*/app.py")):
            app_info = _parse_app(app_path, root_dir)
            if app_info is not None:
                apps[app_info.name] = app_info

    return apps


def get_app(app_name: str, base_dir: Path | None = None) -> AppInfo | None:
    """Return a discovered app by module name."""

    return discover_apps(base_dir).get(app_name.replace("-", "_"))


def find_method(app: AppInfo, function_name: str) -> MethodInfo | None:
    """Find a method by exact name or by hyphen/underscore-normalized name."""

    normalized = function_name.replace("-", "_")
    for method in app.methods:
        if method.name == function_name or method.name == normalized:
            return method
    return None


def _parse_app(app_path: Path, root_dir: Path) -> AppInfo | None:
    try:
        source = app_path.read_text()
    except OSError:
        return None

    try:
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", SyntaxWarning)
            module = ast.parse(source, filename=str(app_path))
    except SyntaxError:
        return None

    class_node = next(
        (
            node
            for node in module.body
            if isinstance(node, ast.ClassDef) and node.name.endswith("App")
        ),
        None,
    )
    if class_node is None:
        return None

    methods = [
        MethodInfo(
            name=node.name,
            signature=_format_signature(node),
            docstring=ast.get_docstring(node) or "No description available.",
            line=node.lineno,
        )
        for node in class_node.body
        if isinstance(node, ast.AsyncFunctionDef) and not node.name.startswith("_")
    ]

    return AppInfo(
        name=app_path.parent.name,
        class_name=class_node.name,
        app_path=app_path,
        source_root=app_path.parent.parent.relative_to(root_dir),
        methods=methods,
    )


def _format_signature(node: ast.AsyncFunctionDef) -> str:
    positional = _format_positional_args(node.args)
    kwonly = _format_kwonly_args(node.args)
    parts = positional.copy()

    if node.args.vararg is not None:
        parts.append(_format_arg(node.args.vararg))

    if kwonly:
        if node.args.vararg is None:
            parts.append("*")
        parts.extend(kwonly)

    if node.args.kwarg is not None:
        parts.append(_format_arg(node.args.kwarg, prefix="**"))

    return f"{node.name}({', '.join(parts)})"


def _format_positional_args(args: ast.arguments) -> list[str]:
    positional_args = [*args.posonlyargs, *args.args]
    positional_defaults = [None] * (len(positional_args) - len(args.defaults)) + list(
        args.defaults
    )

    rendered: list[str] = []
    for index, (arg, default) in enumerate(zip(positional_args, positional_defaults)):
        rendered.append(_format_arg(arg, default=default))
        if args.posonlyargs and index == len(args.posonlyargs) - 1:
            rendered.append("/")
    return rendered


def _format_kwonly_args(args: ast.arguments) -> list[str]:
    return [
        _format_arg(arg, default=default)
        for arg, default in zip(args.kwonlyargs, args.kw_defaults)
    ]


def _format_arg(
    arg: ast.arg, default: ast.expr | None = None, prefix: str = ""
) -> str:
    annotation = ""
    if arg.annotation is not None:
        annotation = f": {ast.unparse(arg.annotation)}"

    rendered = f"{prefix}{arg.arg}{annotation}"
    if default is not None:
        rendered += f" = {ast.unparse(default)}"
    return rendered
