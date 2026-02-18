import re
from app.utils.code_heuristics import (
    CODE_KEYWORDS,
    COMMENT_PATTERNS,
    COMMENT_PATTERNS_BY_LANGUAGE,
)

def looks_like_real_code(code: str, min_code_lines: int = 5, language: str | None = None):
    patterns = (
        COMMENT_PATTERNS_BY_LANGUAGE.get(language.lower())
        if language
        else None
    ) or COMMENT_PATTERNS

    code_lines = []
    for line in code.splitlines():
        stripped = line.strip()
        if not stripped:
            continue
        if any(re.search(p, line) for p in patterns):
            continue
        code_lines.append(stripped)

    if len(code_lines) < min_code_lines:
        return False

    joined = " ".join(code_lines)
    return any(kw in joined for kw in CODE_KEYWORDS)
