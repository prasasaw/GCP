provider "google" {
  project = var.project_id
  region  = var.region
}

terraform {
  backend "gcs" {
    bucket = "terraform-state-110784"
    prefix = "terraform/streaming-dataflow/fixed-window"
  }
}