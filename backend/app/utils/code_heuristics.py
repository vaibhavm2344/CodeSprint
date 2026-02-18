import re

# Patterns that identify comment-only lines (any language)
COMMENT_PATTERNS = [
    r"^\s*#",        # Python
    r"^\s*//",       # C++ / Java / JavaScript / Go
    r"^\s*/\*",      # Block comment start (C/Java/JS)
    r"^\s*\*",       # Block comment continuation
    r"^\s*<!--",     # HTML
]

# Per-language comment patterns for stricter filtering when needed
COMMENT_PATTERNS_BY_LANGUAGE = {
    "python": [r"^\s*#"],
    "java": [r"^\s*//", r"^\s*/\*", r"^\s*\*"],
    "cpp": [r"^\s*//", r"^\s*/\*", r"^\s*\*"],
    "c": [r"^\s*//", r"^\s*/\*", r"^\s*\*"],
    "javascript": [r"^\s*//", r"^\s*/\*", r"^\s*\*"],
    "go": [r"^\s*//", r"^\s*/\*", r"^\s*\*"],
}

# Keywords that indicate real code (at least one should appear)
CODE_KEYWORDS = [
    # Universal / C-style
    "class ",
    "struct ",
    "def ",
    "function ",
    "func ",
    "public ",
    "private ",
    "protected ",
    "static ",
    "void ",
    "int ",
    "float ",
    "double ",
    "return ",
    "if ",
    "for ",
    "while ",
    "import ",
    "package ",
    "var ",
    "const ",
    "type ",
    # Java
    "extends ",
    "implements ",
    "new ",
    # JavaScript/TypeScript
    "export ",
    "const ",
    "let ",
    "=>",
    "async ",
    "await ",
    # Go
    "func ",
    "package ",
    "range ",
    "select ",
    "defer ",
    "go ",
]
