# dbt Staging Layer Setup Guide

## 1. Create the staging model file

**Open/Create:** `dbt/madrileno_newsletter_dbt/models/staging/news/stg_news_articles.sql`

This file transforms your raw bronze data into cleaned silver data. It:
- Selects from your `bronze.newsdata_raw` table
- Renames columns to be clearer (e.g., `link` → `article_url`)
- Casts timestamps to proper types
- Filters out duplicates and null titles

---

## 2. Verify your dbt profile

**Open:** `~/.dbt/profiles.yml` (in your home directory)

This file tells dbt how to connect to BigQuery. You need a profile named `madrileno_newsletter_dbt` that matches your `dbt_project.yml`. It should look something like:

```yaml
madrileno_newsletter_dbt:
  target: dev
  outputs:
    dev:
      type: bigquery
      method: service-account
      project: madrid-newsletter
      dataset: silver
      keyfile: /path/to/your/madrid-newsletter-key.json
      location: US
```

---

## 3. Test dbt connection

**Run from terminal:**
```bash
cd dbt/madrileno_newsletter_dbt
dbt debug
```

This checks if dbt can connect to BigQuery.

---

## 4. Run the model

**Run from terminal:**
```bash
dbt run --select stg_news_articles
```

This creates a view in your `silver` dataset in BigQuery.

---

## What to understand

| File | Purpose |
|------|---------|
| `sources.yml` | Tells dbt where your bronze tables are |
| `stg_news_articles.sql` | The actual transformation logic |
| `profiles.yml` | BigQuery connection credentials |

---

## Session Notes: 2024-03-04 — Project Structure & Cleanup

**Where we are:** Bronze layer is complete (4 tables in BigQuery). Starting to build dbt staging models (silver layer). Reviewed project structure against best practices.

### Standard Data Engineering Project Structure

A well-organized DE project separates concerns clearly:

```
project-root/
├── .github/workflows/          # CI/CD pipelines
├── airflow/dags/               # Orchestration DAGs
├── dbt/
│   ├── models/
│   │   ├── staging/            # Silver layer (1:1 with sources, cleaning)
│   │   ├── intermediate/       # Optional: complex joins
│   │   └── marts/              # Gold layer (business entities)
│   ├── macros/
│   ├── tests/
│   ├── seeds/
│   └── dbt_project.yml
├── infrastructure/terraform/   # IaC for cloud resources
├── src/
│   ├── extractors/             # API clients, data fetching
│   └── loaders/                # Upload to warehouse
├── tests/                      # Python unit tests
├── config/                     # Config files (secrets gitignored)
├── .env.example                # Template for environment variables
├── .gitignore
├── requirements.txt
├── Makefile                    # Common commands
└── README.md
```

**Why this matters (Separation of Concerns):**
- Each folder has one job
- Easier to onboard new team members
- CI/CD can target specific folders
- Debugging is simpler (you know where to look)
- Project scales cleanly

### Medallion Architecture (Bronze → Silver → Gold)

| Layer | Purpose | Materialization | Your Tables |
|-------|---------|-----------------|-------------|
| **Bronze** | Raw data exactly as ingested | Tables | `newsdata_raw`, `cultural_events_raw`, `general_events_raw`, `news_articles_raw` |
| **Silver** | Cleaned, typed, deduplicated, 1:1 with source | Views or Tables | `stg_news_articles`, `stg_cultural_events`, `stg_general_events` |
| **Gold** | Business-ready aggregations, joins, metrics | Tables | `newsletter_content`, `weekly_events`, etc. |

**Key principle:** Each layer builds on the previous. Bronze is your "source of truth" backup. Silver is your clean foundation. Gold answers business questions.

### Cleanup Tasks Identified

| Issue | Location | Fix |
|-------|----------|-----|
| Duplicate scripts | `scripts/upload_to_bronze*.py` (4 versions) | Keep only `_final.py`, delete others |
| Nested dbt folder | `dbt/madrileno_newsletter_dbt/` | Flatten to `dbt/` at root |
| Broken .gitignore | Contains `mkdir` commands (lines 31-36) | Remove those lines |
| Hardcoded API key | `src/sample_data.py` | Move to `.env` file |
| Empty directories | `docs/`, `data/processed/` | Remove or use |
| No requirements.txt | Missing | Add Python dependencies |
| Vague naming | `src/sample_data.py` | Rename to `src/extractors/fetch_sources.py` |

---

## Session Notes: 2024-03-04 — Environment Isolation (WSL vs Windows)

**Context:** Tried to run `dbt debug` in PowerShell and got "dbt is not recognized" error, even though dbt works in WSL.

### DE Concept: Environment Isolation

WSL (Windows Subsystem for Linux) and Windows are **separate environments** that share a filesystem but have independent package installations:

| Environment | Python/packages | Terminal | File paths |
|-------------|-----------------|----------|------------|
| **WSL (Linux)** | Installed separately | Ubuntu, WSL Bash | `/mnt/c/...` |
| **Windows** | Installed separately | PowerShell, CMD | `C:\...` |

**What this means:**
- Installing `dbt` in WSL doesn't make it available in PowerShell
- Each environment has its own `pip`, `python`, virtual environments
- They access the same files, but through different path formats

**Best practice:** Pick one environment and stick with it for consistency. For this project, **WSL** is the primary environment because:
- GCP credentials are configured there
- dbt profile (`~/.dbt/profiles.yml`) is set up there
- Linux is the standard for production data engineering

**VS Code tip:** Set WSL as your default terminal:
1. `Ctrl+Shift+P` → "Terminal: Select Default Profile"
2. Choose "Ubuntu (WSL)" or "WSL Bash"

### Cleanup Tasks Completed

| Task | Status |
|------|--------|
| Remove duplicate scripts | ✅ Done |
| Fix .gitignore | ✅ Done |
| Move API key to .env | ✅ Done |
| Add requirements.txt | ✅ Done |
| Add .env.example | ✅ Done |
