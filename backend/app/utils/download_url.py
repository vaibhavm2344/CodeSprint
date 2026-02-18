import os
import requests

GITHUB_API_BASE = "https://api.github.com"

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

def fetch_download_urls(owner: str, repo: str, files: list, branch="main", token=None):
    download_urls = []
    headers = {
        "Authorization": f"Bearer {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    }
    for path in files:
        url = f"{GITHUB_API_BASE}/repos/{owner}/{repo}/contents/{path}?ref={branch}"
        response = requests.get(url, headers=headers, timeout=10)

        if response.status_code != 200:
            continue

        data = response.json()
        if "download_url" in data:
            download_urls.append(data["download_url"])

    return download_urls
