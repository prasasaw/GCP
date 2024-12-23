terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 4.0"
    }
  }
}

provider "google" {
  project     = "prasad-gcp4-project"
  region      = "europe-west1" # Replace with your desired region
}