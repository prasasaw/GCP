resource "google_storage_bucket" "tf-state-bucket" {
  name     = "tf-state-prasad-gcp4"
  location = "europe-west2"
}
