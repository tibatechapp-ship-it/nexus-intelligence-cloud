"""Static-only evaluation primitives for coding model responses.

Generated code is parsed but never executed by this module.
"""

from __future__ import annotations

import ast
import re
from dataclasses import asdict, dataclass

_FENCE = re.compile(r"```(?:python|py)?\s*\n(.*?)```", re.IGNORECASE | re.DOTALL)


@dataclass(frozen=True)
class StaticCodeScore:
    has_code: bool
    syntax_valid: bool
    line_count: int
    syntax_error: str | None = None

    def to_dict(self) -> dict[str, object]:
        return asdict(self)


def extract_code(text: str) -> str:
    """Prefer a Python fenced block; otherwise treat the complete response as code."""
    match = _FENCE.search(text)
    candidate = match.group(1) if match else text
    return candidate.strip()


def score_code_response(text: str) -> StaticCodeScore:
    """Check presence and Python syntax without importing or executing generated code."""
    code = extract_code(text)
    if not code:
        return StaticCodeScore(False, False, 0, "No code returned")
    try:
        ast.parse(code, mode="exec")
    except SyntaxError as exc:
        message = f"{exc.msg} at line {exc.lineno}"
        return StaticCodeScore(True, False, len(code.splitlines()), message)
    return StaticCodeScore(True, True, len(code.splitlines()))
