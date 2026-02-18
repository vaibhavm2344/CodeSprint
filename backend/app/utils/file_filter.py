from app.utils.language_extensions import (
    IGNORED_FILENAMES,
    IGNORED_KEYWORDS,
    LANGUAGE_ALIASES,
    LANGUAGE_EXTENSIONS,
)

def filter_code_files(tree: list, language_name: str, limit: int = 5):
    canonical = LANGUAGE_ALIASES.get(language_name.lower(), language_name.lower())
    extensions = LANGUAGE_EXTENSIONS.get(canonical)

    if not extensions:
        raise ValueError("Unsupported language")

    files = []

    for item in tree:
        if item["type"] != "blob":
            continue

        path = item["path"].lower()
        filename = path.split("/")[-1]

        if filename in IGNORED_FILENAMES:
            continue

        if any(keyword in filename for keyword in IGNORED_KEYWORDS):
            continue

        for ext in extensions:
            if path.endswith(ext):
                files.append(item["path"])
                if len(files) >= limit:
                    return files

    return files
