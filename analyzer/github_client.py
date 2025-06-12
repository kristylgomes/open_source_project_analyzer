# github_client.py
import os
import requests
from dotenv import load_dotenv

load_dotenv()

GITHUB_API_URL = "https://api.github.com"
TOKEN = os.getenv("GITHUB_TOKEN")

HEADERS = {
    "Authorization": f"Bearer {TOKEN}",
    "Accept": "application/vnd.github+json"
}

def get_org_repos(org_name):
    all_repos = []
    page = 1
    while True:
        url = f"{GITHUB_API_URL}/orgs/{org_name}/repos?per_page=100&page={page}" # Support pagination
        response = requests.get(url, headers=HEADERS)
        if response.status_code != 200:
            raise Exception(f"GitHub API error: {response.status_code} - {response.text}")
        repos = response.json()
        if not repos:
            break
        for repo in repos:
            all_repos.append({
                "name": repo["name"],
                "stars": repo["stargazers_count"],
                "forks": repo["forks_count"],
                "issues": repo["open_issues_count"],
                "language": repo["language"],
                "updated_at": repo["updated_at"],
                "default_branch": repo["default_branch"],
                "html_url": repo["html_url"]
            })
        page += 1
        all_repos.sort(key=lambda r: r["stars"], reverse=True)
    print(f"Found {len(all_repos)} repositories in organization '{org_name}'.")
    return all_repos

