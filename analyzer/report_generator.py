# analyzer/report_generator.py

import pandas as pd

def generate_markdown_report(repos_with_scores, org_name):
    md_lines = [f"# GitHub Report for `{org_name}`\n"]

    for repo in repos_with_scores:
        md_lines.append(f"## [{repo['name']}]({repo['html_url']})")
        md_lines.append(f"- ⭐ Stars: {repo['stars']}")
        md_lines.append(f"- 🍴 Forks: {repo['forks']}")
        md_lines.append(f"- 🐞 Open Issues: {repo['issues']}")
        md_lines.append(f"- 🧑‍💻 Language: {repo['language']}")
        md_lines.append(f"- 🕒 Last Updated: {repo['updated_at']}")
        md_lines.append(f"- 💯 Health Score: {repo['health_score']}/5")
        md_lines.append(f"- 🔍 Reasons: {', '.join(repo['health_reasons'])}")
        md_lines.append("")  # blank line

    report = "\n".join(md_lines)
    with open(f"{org_name}_report.md", "w") as f:
        f.write(report)
    print(f"✅ Markdown report written to {org_name}_report.md")


def generate_csv_report(repos_with_scores, org_name):
    df = pd.DataFrame(repos_with_scores)
    df.to_csv(f"{org_name}_report.csv", index=False)
    print(f"✅ CSV report written to {org_name}_report.csv")


def generate_html_report(repos_with_scores, org_name):
    df = pd.DataFrame(repos_with_scores)

    # Simplify health reasons into a string
    df["health_reasons"] = df["health_reasons"].apply(lambda x: ", ".join(x) if isinstance(x, list) else x)

    html_content = df.to_html(
        index=False,
        border=0,
        justify="center",
        classes="table table-striped",
        render_links=True,
        escape=False
    )

    full_html = f"""
    <html>
    <head>
        <title>GitHub Report for {org_name} sorted by # of stars</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                margin: 40px;
                background-color: #f9f9f9;
            }}
            h1 {{
                text-align: center;
                color: #2962FF; /* Liquibase blue */
            }}
            h3 {{
                text-align: center;
                color: #333333; /* Darker gray */
            }}
            .table {{
                width: 100%;
                border-collapse: collapse;
            }}
            .table th, .table td {{
                border: 1px solid #ccc;
                padding: 8px;
                text-align: left;
            }}
            .table th {{
                background-color: #eaeaea;
            }}
        </style>
    </head>
    <body>
        <h1>GitHub Report for {org_name}</h1>
        <h3>List sorted by # of stars in descending order</h3>
        {html_content}
    </body>
    </html>
    """

    file_name = f"{org_name}_report.html"
    with open(file_name, "w", encoding="utf-8") as f:
        f.write(full_html)

    print(f"✅ HTML report written to {file_name}")    