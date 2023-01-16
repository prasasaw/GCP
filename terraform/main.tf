resource "google_storage_bucket" "bucket" {
  name     = "test-bucket-random-110784"
  location = "europe-west2"
}


resource "google_storage_bucket" "anay_bucket" {
  name     = "test-bucket-random-anay"
  location = "europe-west2"
}