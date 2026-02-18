import os
import requests

GITHUB_API_BASE = "https://api.github.com"

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

def fetch_repo_tree(owner: str, repo: str, branch: str = "main"):
    url = f"{GITHUB_API_BASE}/repos/{owner}/{repo}/git/trees/{branch}?recursive=1"
    headers = {
        "Authorization": f"Bearer {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    }
    response = requests.get(url, headers=headers, timeout=10)

    if response.status_code == 404 and branch == "main":
        return fetch_repo_tree(owner, repo, branch="master")

    if response.status_code != 200:
        raise ValueError("Unable to fetch repository tree")

    data = response.json()
    return data.get("tree", []), branch
