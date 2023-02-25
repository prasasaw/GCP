resource "google_storage_bucket" "bucket" {
  name     = "fixed-window-117"
  location = "europe-west2"
}

resource "google_pubsub_topic" "topic" {
  name = "orders"
  message_retention_duration = "86600s"
}

resource "google_pubsub_subscription" "subscription" {
  name  = "orders-sub"
  topic = google_pubsub_topic.topic.orders

  labels = {
    purpose = "streaming-dataflow"
  }

  # 20 minutes
  message_retention_duration = "1200s"
  retain_acked_messages      = true

  ack_deadline_seconds = 20

  expiration_policy {
    ttl = "300000.5s"
  }
  retry_policy {
    minimum_backoff = "10s"
  }

  enable_message_ordering    = false
}