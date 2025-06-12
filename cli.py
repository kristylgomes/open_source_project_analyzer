# cli.py

import os
import time
from dotenv import load_dotenv

from analyzer.github_client import get_org_repos
from analyzer.metrics_calculator import calculate_health_score
from analyzer.report_generator import generate_markdown_report, generate_csv_report, generate_html_report

load_dotenv()
TOKEN = os.getenv("GITHUB_TOKEN")

def main():
    org = input("Enter GitHub organization name: ")
    start_time = time.time()  # Start timer
    try:
        repos = get_org_repos(org)
        results = []

        print(f"\n📦 Repositories in '{org}':\n")
        for repo in repos:
            score, reasons = calculate_health_score(repo, org, TOKEN)

            print(f"{repo['name']}: ⭐ {repo['stars']} | 🍴 {repo['forks']} | 🐞 {repo['issues']} | "
                  f"🗣️ {repo['language']} | 🕒 {repo['updated_at']} | 💯 Health: {score}/5")
            print(f"  🔍 {', '.join(reasons)}")
            print(f"  🔗 {repo['html_url']}\n")

            # Add health data to repo dictionary
            repo["health_score"] = score
            repo["health_reasons"] = reasons
            results.append(repo)

        # Generate reports
        generate_markdown_report(results, org)
        generate_csv_report(results, org)
        generate_html_report(results, org)
        print(f"✅ Reports generated for organization '{org}':")
    
    except Exception as e:
        print(f"❌ Error: {e}")

    print(f"Scored {len(repos)} repositories in organization '{org}', sorted by stars.")
    elapsed = time.time() - start_time  # End timer
    print(f"Completed Request in {elapsed:.2f} seconds.")    

if __name__ == "__main__":
    main()

