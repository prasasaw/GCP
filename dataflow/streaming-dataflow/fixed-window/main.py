import apache_beam as beam
from apache_beam.options.pipeline_options import PipelineOptions
from apache_beam.io.gcp.internal.clients import bigquery
import yaml
import sys
import json
import logging

CONFIG = yaml.safe_load(open("env.yaml"))
PROJECT = CONFIG["PROJECT"]
DATASET = CONFIG["PROJECT"]
BUCKET = CONFIG["BUCKET"]
TOP = CONFIG["TOPIC"]
SUB = CONFIG["SUBSCRIPTION"]
SUBSCRIPTION = "projects/{}/subscriptions/{}".format(PROJECT, SUB)
TOPIC = "projects/{}/topics/{}".format(PROJECT, TOP)


GENERATE_TEMPLATE = True if "generate-template" in sys.argv else False
SHOW_HELP = (
    True
    if [i for i in ["generate-template", "deploy"] if i in sys.argv] == []
    else False
)

with open("table_schema.json", "r") as schema_file:
    bq_schema = schema_file.read()
TABLE_SCHEMA = json.loads(bq_schema)


def generate_schema(schema_json):
    """Expecting string pipe separated for fields and comma separated
    on attributes name, type, mode"""
    local_table_schema = bigquery.TableSchema()
    for field in schema_json:
        field_schema = bigquery.TableFieldSchema()
        field_schema.name = field["name"].lower()
        field_schema.type = field["type"].lower()
        field_schema.mode = field["mode"].lower()
        local_table_schema.fields.append(field_schema)
    return local_table_schema


class BQTransformation(beam.DoFn):
    def process(self, element):
        try:
            print(element)
            return element

        except Exception as err:
            # Issues while Writing to BigQuery: Defect raised ICF-2037
            logging.info(
                {
                    "message": "Error in Customer Interactions "
                    + "Dataflow Writing to Bigquery:",
                    "Error": err,
                    "Element": elm,
                }
            )


def dataflow(run_local):
    """Run the dataflow"""
    schema = generate_schema(TABLE_SCHEMA)
    job_name = "orders-v2"
    pipeline_options = {
        "project": PROJECT,
        "staging_location": "gs://" + BUCKET + "/staging",
        "temp_location": "gs://" + BUCKET + "/temp",
        "runner": "DataflowRunner",
        "job_name": job_name,
        "disk_size_gb": 10,
        "save_main_session": True,
        "region": "europe-west1",
        "requirements_file": "requirements.txt",
        "streaming": True,
        "enable_streaming_engine": True,
        "max_num_workers": 2,
        "machine_type": "n1-standard-2",
    }

    if GENERATE_TEMPLATE:
        pipeline_options["template_location"] = "gs://" + BUCKET + "/template/DF_Orders"

    if run_local:
        print("Running Locally...")
        pipeline_options["runner"] = "DirectRunner"

    options = PipelineOptions.from_dictionary(pipeline_options)

    with beam.Pipeline(options=options) as pipe:
        order_events = pipe | "Read Topic from PubSub" >> beam.io.ReadFromPubSub(
            subscription=SUBSCRIPTION
        ).with_output_types(bytes)
        (order_events | "Transform to BQ dict" >> beam.ParDo(BQTransformation()))

        """(
            order_events
            | "Transform to BQ dict" >> beam.ParDo(BQTransformation())
            | "Write To Partitioned BigQuery Table"
            >> beam.io.gcp.bigquery.WriteToBigQuery(
                "orders",
                schema=schema,
                dataset=DATASET,
                project=PROJECT,
                insert_retry_strategy="neverRetry",
                # create_disposition=bigquery_options.BigQueryDisposition.CREATE_NEVER,
            )
        )"""


if __name__ == "__main__":
    open("terminal.log", "w").close()
    # sys.stdout = Log()
    RUN_LOCALLY = True
    print("Starting Dataflow")

    if SHOW_HELP:
        print("Configured environment:\n{}".format(CONFIG))
        print(
            """
            Please add any of the following parameters:\n
            generate-template,  to generate a new template for configured env
            deploy, to perform deployment to configured environment
            """
        )
    else:
        dataflow(RUN_LOCALLY)
