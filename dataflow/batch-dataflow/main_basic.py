"""
sample batch dataflow

"""
import datetime
import json
import re
import csv
import apache_beam as beam
from apache_beam.options.pipeline_options import PipelineOptions
from apache_beam.io.gcp.internal.clients import bigquery
from csv import reader
import sys

import yaml
from apache_beam import pvalue

"""environment variables"""
CONFIG = yaml.safe_load(open('env.yaml'))
PROJECT = CONFIG['BQ_Project']
BUCKET = CONFIG['bucket']

# better to implement below schema as a json schema in a separate file
table_schema = 'orderId:STRING,orderType:STRING,orderDateTime:DATETIME,customerId:STRING,country:STRING,insertDateTime:DATETIME'

GENERATE_TEMPLATE = True if "generate-template" in sys.argv else False

SHOW_HELP = False
"""(
    True
    if [i for i in ["generate-template"] if i in sys.argv] == []
    else False
)"""

RUN_LOCALLY = True

class UserOptions(PipelineOptions):
    @classmethod
    def _add_argparse_args(cls, parser):
        parser.add_value_provider_argument('--templated_input', type=str)
        parser.add_value_provider_argument('--templated_header', type=str)
        parser.add_value_provider_argument('--templated_RU', type=str)


""" Does transformations for BigQuery"""
class CSVToBQDict(beam.DoFn):
    
    def process(self, element, header, RU):

        for line in reader([element]):
            row=line
        row=map(str,row)
        #head = header.get().split(',')
        # for local testing : 
        head = header
        import pdb
        pdb.set_trace()
        dict_full=dict(zip(head, row))
        dict_full['country'] = RU.get()
        dict_full['insertDateTime'] = str(datetime.datetime.utcnow().replace(microsecond=0))
        return [dict_full]


def dataflow(run_local):
    
    JOB_NAME = 'my-batch-dataflow-{}'.format(datetime.datetime.now().strftime('%Y-%m-%d-%H%M%S'))
    pipeline_options = {
        'project': PROJECT,
        'staging_location': 'gs://' + BUCKET + '/staging',
        'temp_location': 'gs://' + BUCKET + '/temp',
        'runner': 'DataflowRunner',
        'job_name': JOB_NAME,
        'disk_size_gb': 100,
        'save_main_session': True,
        'region':'europe-west1',
        'requirements_file':'requirements.txt'
         }  

    if GENERATE_TEMPLATE:
        pipeline_options["template_location"] = (
            'gs://'+ BUCKET +'/template/my_dataflow_template'
        )

    options = PipelineOptions.from_dictionary(pipeline_options)
    user_options = options.view_as(UserOptions)
    input_file_path = user_options.templated_input
    header = user_options.templated_header
    RU = user_options.templated_RU
    dataset = 'my_dataset'
    
    if run_local:
        print("Running Locally...")
        pipeline_options['runner'] = 'DirectRunner'
        input_file_path = 'local_file.csv'
        RU = 'CA'
        Dataset = 'my_dataset'
        head = 'orderId,orderType,orderDateTime,customerId,country,insertDateTime'
        header = head.split(',')
        options = PipelineOptions.from_dictionary(pipeline_options)
       
    with beam.Pipeline(options=options) as p:
        
        lines = (p | beam.io.ReadFromText(input_file_path, skip_header_lines=1))
        
        BQ = (lines | 'CSV row to BQ dict' >> beam.ParDo(CSVToBQDict(), header, RU)
        | 'Write To BigQuery' >> beam.io.gcp.bigquery.WriteToBigQuery('order_table', schema=table_schema,dataset=dataset, project=PROJECT))
        


if __name__ == "__main__":

    print("Starting Dataflow")

    if SHOW_HELP:
        print("CONFIGured environment:\n{}".format(CONFIG))
        print(
            """
Please add the following parameters:\n
    generate-template,  to generate a new template for configured env
    """
        )
    else:
        dataflow(RUN_LOCALLY)
