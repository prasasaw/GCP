from google.cloud import bigquery
from datetime import datetime
import json


# Construct a BigQuery client object.
client = bigquery.Client()

# Set dataset_id to the ID of the dataset that contains
dataset_id = "ingka-csr-dccloud-dev.sample_data_daily_test_results"
DQ_summary_table = "ingka-csr-dccloud-dev.sample_data_daily_test_results.DQ_Summary"

# This script goes through all tables listed in the dataset that stores dbt test results


def get_row_count(table):
    query = "SELECT * FROM `{}".format(dataset_id) + ".{}`".format(table)
    query_job = client.query(query)
    rows = query_job.result()
    return rows.total_rows


def get_n_records(table):
    query = "SELECT SUM(n_records) FROM `{}".format(dataset_id) + ".{}`".format(table)
    query_job = client.query(query)
    rows = query_job.result()
    for r in rows:
        n_records = dict(r.items())["f0_"]
    return n_records


def bq_insert(rows_to_insert):

    errors = client.insert_rows_json(
        DQ_summary_table, rows_to_insert
    )  # Make an API request.
    if errors == []:
        print("New rows have been added.")
    else:
        print("Encountered errors while inserting rows: {}".format(errors))


def get_current_time():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")


class result:
    def __init__(self, rule_id, failed_rows, execution_time):
        self.rule_id = rule_id
        self.failed_rows = failed_rows
        self.execution_time = execution_time


def process_dq_results():
    tables = client.list_tables(dataset_id)
    obj_lst = []
    execution_time = get_current_time()
    for table in tables:
        rows = None
        table_name = table.table_id
        row_count = get_row_count(table_name)
        if row_count > 0:
            if "not_null" in table_name:
                rows = row_count
            if "assert" in table_name:
                rows = 1
            if "accepted_values" in table_name:
                rows = get_n_records(table_name)
            if "unique" in table_name:
                rows = get_n_records(table_name)
            obj = {}
            obj = result(table_name, rows, execution_time)
            obj_lst.append(obj.__dict__)

    bq_insert(obj_lst)


if __name__ == "__main__":
    process_dq_results()
