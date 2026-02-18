from urllib.parse import urlparse

def parse_github_repo(repo_url: str):
    parsed = urlparse(repo_url)
    if "github.com" not in parsed.netloc:
        raise ValueError("Only GitHub repositories are supported")

    parts = parsed.path.strip("/").split("/")
    if len(parts) != 2:
        raise ValueError("Invalid GitHub repository URL")

    owner, repo = parts
    return owner, repo
