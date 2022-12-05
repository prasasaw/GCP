## sample batch dataflow

A very basic version of batch dataflow. 

### Input
It takes a csv file. 
When testing locally, set "RUN_LOCALLY = True" and it reads the file present locally 'local_file.csv' and all the settings in "if run_local:" section
When testing on GCP, it reads the file from GCS. Also note that the file location and other parameters are passed as templated inputs to the dataflow. 
This can be done by say a calling cloud function that send these inputs to the dataflow through an API call. 


### Processing
There are 2 processing functions,
1) CSVToFSDict: we use this parDo function to do any transformations related to firestore
2) CSVToBQDict: we use this parDo function to do any transformations related to BigQuery

### Storage
The data is written to Firestore using a custom parDo function called WriteToFirestore (there was no in built Firestore connector for apache beam python sdk at this time) 
For BigQuery however, this is done using the apache beam connector for BigQuery beam.io.gcp.bigquery.WriteToBigQuery