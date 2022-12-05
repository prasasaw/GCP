1. Create environment
  python3 -m venv dbt-env
2. Activate environment
dbt-env\Scripts\activate
--3. Install dbt
--pip install dbt-bigquery
4. Check the dbt has been installed correctly
dbt --version
dbt docs serve --port 8001
dbt docs generate
dbt source freshness