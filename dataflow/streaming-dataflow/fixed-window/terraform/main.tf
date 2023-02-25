resource "google_storage_bucket" "bucket" {
  name     = "fixed-window-117"
  location = "europe-west2"
}

resource "google_pubsub_topic" "orders" {
  name = "orders"
  message_retention_duration = "86600s"
}