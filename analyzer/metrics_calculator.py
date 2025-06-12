# analyzer/metrics_calculator.py

import requests
from datetime import datetime, timedelta, timezone

def calculate_health_score(repo, org_name, token):
    score = 0
    reasons = []

    # Check for LICENSE
    if repo.get("license"):
        score += 1
        reasons.append("✅ License")

    # Check for recent update (within 30 days)
    now = datetime.now(timezone.utc)
    updated_at = datetime.fromisoformat(repo["updated_at"].replace("Z", "+00:00"))
    if updated_at > now - timedelta(days=30):
        score += 1
        reasons.append("🕒 Recently updated")

    # Check if README exists
    readme_url = f"https://api.github.com/repos/{org_name}/{repo['name']}/contents/README.md"
    r = requests.get(readme_url, headers={"Authorization": f"Bearer {token}"})
    if r.status_code == 200:
        score += 1
        reasons.append("📘 README found")

    # Check if CI config exists in .github/workflows
    ci_url = f"https://api.github.com/repos/{org_name}/{repo['name']}/contents/.github/workflows"
    r = requests.get(ci_url, headers={"Authorization": f"Bearer {token}"})
    if r.status_code == 200 and isinstance(r.json(), list) and len(r.json()) > 0:
        score += 1
        reasons.append("⚙️ CI config found")

    # Check if there are recent issues (within last 30 days)
    since_date = (now - timedelta(days=30)).isoformat()
    issues_url = f"https://api.github.com/repos/{org_name}/{repo['name']}/issues?since={since_date}Z"
    r = requests.get(issues_url, headers={"Authorization": f"Bearer {token}"})
    if r.status_code == 200 and len(r.json()) > 0:
        score += 1
        reasons.append("🐞 Active issues found")

    return score, reasons