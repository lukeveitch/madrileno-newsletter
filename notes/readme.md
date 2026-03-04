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
