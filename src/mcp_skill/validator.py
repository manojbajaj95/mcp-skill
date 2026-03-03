import ast
import shutil
import subprocess
from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class ValidationResult:
    passed: bool
    step: str
    errors: list[str] = field(default_factory=list)


@dataclass
class ValidationReport:
    results: list[ValidationResult] = field(default_factory=list)

    @property
    def passed(self) -> bool:
        return all(r.passed for r in self.results)

    def summary(self) -> str:
        lines = []
        for r in self.results:
            icon = "✓" if r.passed else "✗"
            lines.append(f"  {icon} {r.step}")
            for err in r.errors:
                lines.append(f"    {err}")
        return "\n".join(lines)


def _run_ast_parse(file_path: Path) -> ValidationResult:
    try:
        source = file_path.read_text()
        ast.parse(source, filename=str(file_path))
        return ValidationResult(passed=True, step="ast.parse")
    except SyntaxError as e:
        return ValidationResult(
            passed=False,
            step="ast.parse",
            errors=[f"Line {e.lineno}: {e.msg}"],
        )


def _run_tool(cmd: list[str], step_name: str, file_path: Path) -> ValidationResult:
    tool_bin = cmd[0]

    if not shutil.which(tool_bin):
        uvx = shutil.which("uvx")
        if uvx:
            cmd = [uvx, *cmd]
        else:
            return ValidationResult(
                passed=True,
                step=f"{step_name} (skipped — not installed)",
            )

    try:
        result = subprocess.run(
            [*cmd, str(file_path)],
            capture_output=True,
            text=True,
            timeout=30,
        )
    except subprocess.TimeoutExpired:
        return ValidationResult(
            passed=False,
            step=step_name,
            errors=["Timed out after 30s"],
        )

    if result.returncode == 0:
        return ValidationResult(passed=True, step=step_name)

    output = (result.stdout + result.stderr).strip()
    error_lines = [line for line in output.splitlines() if line.strip()][:10]
    return ValidationResult(passed=False, step=step_name, errors=error_lines)


def validate_generated_code(file_path: Path) -> ValidationReport:
    report = ValidationReport()

    report.results.append(_run_ast_parse(file_path))
    if not report.results[-1].passed:
        return report

    report.results.append(_run_tool(["ruff", "check"], "ruff", file_path))
    report.results.append(_run_tool(["ty", "check"], "ty", file_path))

    return report
