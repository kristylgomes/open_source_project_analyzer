import os
import time
import streamlit as st
import pandas as pd
import plotly.express as px
from dotenv import load_dotenv

from analyzer.github_client import get_org_repos
from analyzer.metrics_calculator import calculate_health_score
from analyzer.report_generator import generate_csv_report, generate_markdown_report, generate_html_report

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

            # Create clickable repo links
            df["repo_link"] = df.apply(lambda row: f'<a href="{row["html_url"]}" target="_blank">{row["name"]}</a>', axis=1)

            # Add color-coded health scores
            def score_badge(score):
                if score >= 4:
                    color = "green"
                elif score == 3:
                    color = "orange"
                else:
                    color = "red"
                return f'<span style="color:{color}; font-weight:bold;">{score}/5</span>'

            df["health_display"] = df["health_score"].apply(score_badge)

            st.success(f"Found {len(results)} repositories.")

            # Render styled HTML table
            st.markdown("### 🧠 Repository Summary")
            # Custom CSS to center table headers and content
            st.markdown("""
                <style>
                th, td {
                    text-align: center !important;
                }
                </style>
            """, unsafe_allow_html=True)
            st.markdown(df.to_html(
                escape=False,
                columns=["repo_link", "stars", "forks", "issues", "language", "updated_at", "health_display", "health_reasons"],
                index=False
            ), unsafe_allow_html=True)

            # Download CSV
            st.download_button(
                label="⬇️ Download CSV Report",
                data=df.to_csv(index=False).encode('utf-8'),
                file_name=f"{org}_report.csv",
                mime='text/csv'
            )

            # Optional: generate local Markdown & HTML reports
            generate_markdown_report(results, org)
            generate_html_report(results, org)
            st.info("Markdown and HTML reports saved to local disk.")

            # Charts
            st.markdown("### 📊 Metrics Visualization")

            fig_stars = px.bar(df.sort_values("stars", ascending=False), x="name", y="stars", title="⭐ Stars per Repository")
            st.plotly_chart(fig_stars, use_container_width=True)

            fig_health = px.histogram(df, x="health_score", nbins=6, title="💯 Health Score Distribution")
            st.plotly_chart(fig_health, use_container_width=True)

            # Top Repos Table
            top_repos = df.sort_values("stars", ascending=False).head(5)
            st.markdown("### 🌟 Top 5 Most Starred Repos")
            st.table(top_repos[["name", "stars", "language", "health_score"]])

        except Exception as e:
            st.error(f"Error: {e}")

        elapsed = time.time() - start_time  # End timer
        st.info(f"Completed Request in {elapsed:.2f} seconds.")      