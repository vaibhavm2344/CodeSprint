
import re
from app.utils.code_heuristics import COMMENT_PATTERNS_BY_LANGUAGE


def strip_comments_in_block(block: str, language: str) -> str:
    
    if not block.strip():
        return block
    patterns = COMMENT_PATTERNS_BY_LANGUAGE.get(language)
    if not patterns:
        return block

    lines = block.splitlines()
    out = []
    in_block_comment = False
    block_start = re.compile(r"^\s*/\*")
    block_end = re.compile(r"\*/")
    line_comment = re.compile(r"^\s*//")
    inline_line = re.compile(r"//.*$")
    hash_comment = re.compile(r"#.*$")  # Python

    for line in lines:
        if language == "python":
            # Python: strip # to EOL
            stripped = re.sub(hash_comment, "", line)
            if stripped.strip():
                out.append(stripped.rstrip())
            continue

        # C-style: handle /* */ and //
        if in_block_comment:
            if block_end.search(line):
                in_block_comment = False
                
                rest = re.sub(r"^.*?\*/", "", line, count=1)
                rest = re.sub(inline_line, "", rest).strip()
                if rest:
                    out.append(rest)
            continue

        if block_start.search(line):
            if block_end.search(line):
                # Same-line block comment: remove /* ... */ only, keep rest
                line = re.sub(r"/\*.*?\*/", "", line)
                line = re.sub(inline_line, "", line).strip()
                if line:
                    out.append(line)
            else:
                in_block_comment = True
                before = re.sub(r"/\*.*", "", line).strip()
                if before:
                    out.append(before)
            continue

        if line_comment.match(line):
            continue
        # Remove inline // (and skip full-line // already)
        line = re.sub(inline_line, "", line)
        # Block comment continuation: line that is only whitespace + * + optional space (not *ptr)
        if re.match(r"^\s*\*\s*$", line) or re.match(r"^\s*\*\s+", line):
            continue
        if line.strip():
            out.append(line.rstrip())

    return "\n".join(out)


def _find_matching_brace(text: str, start: int) -> int:
    
    depth = 0
    i = start
    in_double = False
    in_single = False
    escape = False
    while i < len(text):
        c = text[i]
        if escape:
            escape = False
            i += 1
            continue
        if c == "\\" and (in_double or in_single):
            escape = True
            i += 1
            continue
        if not in_double and not in_single:
            if c == "{":
                depth += 1
            elif c == "}":
                depth -= 1
                if depth == 0:
                    return i
            elif c == '"':
                in_double = True
            elif c == "'":
                in_single = True
        elif c == '"' and in_double:
            in_double = False
        elif c == "'" and in_single:
            in_single = False
        i += 1
    return -1


def _extract_python(code: str) -> list[str]:
    blocks = []
    lines = code.splitlines()
    i = 0
    while i < len(lines):
        line = lines[i]
        m = re.match(r"^(\s*)def\s+\w+\s*\(", line)
        if m:
            base_indent = len(m.group(1))
            block_lines = [line]
            j = i + 1
            while j < len(lines):
                next_line = lines[j]
                if not next_line.strip():
                    block_lines.append(next_line)
                    j += 1
                    continue
                leading = len(next_line) - len(next_line.lstrip())
                if leading <= base_indent and next_line.strip():
                    break
                block_lines.append(next_line)
                j += 1
            blocks.append("\n".join(block_lines))
            i = j
            continue
        i += 1
    return blocks


def _line_offset_to_pos(lines: list[str], line_idx: int, offset_in_line: int) -> int:
    total = 0
    for k in range(line_idx):
        total += len(lines[k]) + 1
    return total + offset_in_line


def _extract_brace_block_from(full_text: str, open_brace_index: int, start_line_pos: int) -> str | None:
    
    end = _find_matching_brace(full_text, open_brace_index)
    if end == -1:
        return None
    return full_text[start_line_pos : end + 1]


def _extract_brace_language(code: str, language: str) -> list[str]:
   
    blocks = []
    lines = code.splitlines()
    i = 0
    while i < len(lines):
        line = lines[i]
        stripped = line.strip()
        if stripped.startswith("//") or stripped.startswith("/*") or (stripped.startswith("*") and not stripped.startswith("**")):
            i += 1
            continue
        if ")" in line and "{" in line:
            brace_pos = line.index("{")
            start_pos = _line_offset_to_pos(lines, i, 0)
            block = _extract_brace_block_from(code, _line_offset_to_pos(lines, i, brace_pos), start_pos)
            if block and 3 <= block.count("\n") + 1 <= 200:
                blocks.append(block)
            i += 1
            continue
        if ")" in line:
            j = i + 1
            while j < len(lines) and not lines[j].strip():
                j += 1
            if j < len(lines) and lines[j].strip().startswith("{"):
                brace_pos = lines[j].index("{")
                start_pos = _line_offset_to_pos(lines, i, 0)
                block = _extract_brace_block_from(code, _line_offset_to_pos(lines, j, brace_pos), start_pos)
                if block and 3 <= block.count("\n") + 1 <= 200:
                    blocks.append(block)
            i = j + 1 if j > i else i + 1
            continue
        i += 1
    return blocks


def extract_functions(code: str, language: str, max_blocks: int = 5) -> list[str]:
    
    lang = (language or "").lower()
    if lang == "python":
        raw_blocks = _extract_python(code)
    elif lang in ("java", "cpp", "c", "javascript", "go"):
        raw_blocks = _extract_brace_language(code, lang)
    else:
        return []

    result = []
    for block in raw_blocks[:max_blocks]:
        cleaned = strip_comments_in_block(block, lang)
        if cleaned.strip() and cleaned.count("\n") >= 2:
            result.append(cleaned)
    return result
