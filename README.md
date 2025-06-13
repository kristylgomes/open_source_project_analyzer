# 🧠 Open Source Project Analyzer

A Python application with a Streamlit web interface that analyzes a GitHub organization's public repositories and generates reports with detailed with detailed metadata and health insights.

---

## 🚀 Features

- 🔍 Fetches all public repositories for a given GitHub organization
- 📊 Collects key repository metrics:
  - Stars, forks, open issues
  - Primary language, last updated date
- 🧪 Calculates a **health score** for each repository based on:
  - README presence
  - License presence
  - CI configuration
  - Recent updates
  - Recent issue activity
- 📝 Generates reports in:
  - **Markdown**
  - **CSV**
  - **HTML**

---

## 📦 Sample Output

```
repo-name: ⭐ 123 | 🍴 45 | 🐞 3 | 🗣️ Python | 🕒 2024-06-01T12:00:00Z | 💯 Health: 4/5
  🔍 README found, Recently updated, CI config found, License
  🔗 https://github.com/org/repo-name
```

---

## 📁 Project Structure

```
open_source_project_analyzer/
├── analyzer/
│   ├── github_client.py         # GitHub API calls
│   ├── metrics_calculator.py    # Repo health scoring
│   ├── report_generator.py      # Markdown, CSV, HTML reports
│   └── __init__.py
├── app.py                       # Streamlit web app
├── cli.py                       # CLI version (optional)
├── .env                         # GitHub token (not committed)
├── .gitignore
├── README.md
├── LICENSE
├── requirements.txt
```

---

## 🛠 Setup & Usage

### 1. Clone the repo and navigate into it

```bash
git clone https://github.com/your-username/open_source_project_analyzer.git
cd open_source_project_analyzer
```

### 2. Create a virtual environment

```bash
python -m venv a1-venv
source a1-venv/bin/activate  # On Windows: a1-venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Add a `.env` file with your GitHub token

```
GITHUB_TOKEN=ghp_your_token_here
```

> 🔒 Never commit your `.env` file or token to source control!

### 5. Run the CLI

```bash
python cli.py
```

You'll be prompted for a GitHub organization name. Reports will be saved in the current directory.

---

## ▶️ Run the Web App

```bash
streamlit run app.py
```

The app will launch in your default web browser at `http://localhost:8501`.

---

## 📄 Example Output Files

- `repo-name_report.md`
- `repo-name_report.csv`
- `repo-name_report.html`

---

## 👩‍💻 Author

Built by Kristyl Gomes.

---

## 📜 License

Apache-2.0 License. See `LICENSE` file for details.
