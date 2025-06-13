# app.py

import os
import time
import streamlit as st
from dotenv import load_dotenv

from analyzer.github_client import get_org_repos
from analyzer.metrics_calculator import calculate_health_score
from analyzer.report_generator import generate_csv_report, generate_markdown_report, generate_html_report

import pandas as pd

load_dotenv()
TOKEN = os.getenv("GITHUB_TOKEN")

st.set_page_config(page_title="GitHub Project Analyzer", layout="wide")

st.title("🔍 Open Source Project Analyzer")

org = st.text_input("Enter a GitHub organization name (e.g., liquibase, apache):")
start_time = time.time()  # Start timer
if org:
    with st.spinner("Fetching and analyzing repositories..."):
        try:
            repos = get_org_repos(org)
            results = []

            for repo in repos:
                score, reasons = calculate_health_score(repo, org, TOKEN)
                repo["health_score"] = score
                repo["health_reasons"] = ", ".join(reasons)
                results.append(repo)

            df = pd.DataFrame(results)

            st.success(f"Found {len(results)} repositories.")
            st.dataframe(df[[
                "name", "stars", "forks", "issues", "language",
                "updated_at", "health_score", "health_reasons", "html_url"
            ]])

            st.download_button(
                label="⬇️ Download CSV Report",
                data=df.to_csv(index=False).encode('utf-8'),
                file_name=f"{org}_report.csv",
                mime='text/csv'
            )

            # Optional HTML and Markdown generation (saved to file system)
            generate_markdown_report(results, org)
            generate_html_report(results, org)
            st.info("Markdown and HTML reports saved to local disk.")

        except Exception as e:
            st.error(f"Error: {e}")

        # print(f"Scored {len(repos)} repositories in organization '{org}', sorted by stars.")
        elapsed = time.time() - start_time  # End timer
        st.info(f"Completed Request in {elapsed:.2f} seconds.")        