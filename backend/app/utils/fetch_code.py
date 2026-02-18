import os
import random
import requests

from app.utils.good_code import looks_like_real_code
from app.utils.language_extensions import IGNORE_LINE_PREFIXES
from app.utils.function_extractor import extract_functions

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

def fetch_code_from_urls(download_urls: list, max_lines: int = 40, language: str | None = None):
    code_files = []
    headers = {}
    if GITHUB_TOKEN:
        headers["Authorization"] = f"Bearer {GITHUB_TOKEN}"
    headers["Accept"] = "application/vnd.github.v3.raw"

    for url in download_urls:
        try:
            response = requests.get(url, headers=headers, timeout=15)
        except requests.RequestException:
            continue
        if response.status_code != 200:
            continue

        full_code = response.text
        if not full_code.strip():
            continue

        if not looks_like_real_code(full_code, min_code_lines=4, language=language):
            continue

        
        if language:
            blocks = extract_functions(full_code, language, max_blocks=10)
            if blocks:
                block = random.choice(blocks)
                lines = block.splitlines()
                if len(lines) > max_lines:
                    block = "\n".join(lines[:max_lines])
                if len(lines) >= 3:
                    code_files.append({"url": url, "code": block})
                    continue
        
        filtered_lines = []
        for line in full_code.splitlines():
            stripped = line.lstrip()
            if not stripped:
                continue
            if stripped.startswith(IGNORE_LINE_PREFIXES):
                continue
            filtered_lines.append(line)
            if len(filtered_lines) >= max_lines:
                break

        if len(filtered_lines) < 3:
            continue

        code_files.append({
            "url": url,
            "code": "\n".join(filtered_lines)
        })

    return code_files
