# Canonical language name -> file extensions for file_filter
LANGUAGE_EXTENSIONS = {
    "python": [".py"],
    "javascript": [".js", ".ts", ".mjs", ".cjs"],
    "cpp": [".cpp", ".hpp", ".h", ".cc", ".cxx"],
    "c": [".c", ".h"],
    "java": [".java"],
    "go": [".go"],
}

# Map common/display names to canonical name used in LANGUAGE_EXTENSIONS
LANGUAGE_ALIASES = {
    "c++": "cpp",
    "cplusplus": "cpp",
    "js": "javascript",
    "ts": "javascript",
    "typescript": "javascript",
    "py": "python",
}

IGNORED_FILENAMES = {
    "__init__.py",
    "index.js",
    "index.ts",
    "main.py",
    "main.cpp",
    "main.c",
    "main.go",
    "app.py",
    "app.js",
}

IGNORED_KEYWORDS = [
    "test",
    "tests",
    "config",
    "setup",
    "init",
    "constant",
    "env",
    "example",
    "sample",
    "mock",
    "spec",
]

# Line prefixes treated as comments (used when filtering lines)
IGNORE_LINE_PREFIXES = (
    "#",   # Python
    "//",  # C / C++ / Java / JS / Go
    "/*",
    "*",
)