resource "google_storage_bucket" "tf-state-bucket" {
  name     = "tf-state-prasad-gcp4"
  location = "europe-west2"
}

resource "google_artifact_registry_repository" "artifact-repo" {
  location = "europe-west1"
  repository_id = "repo-prasad-gcp4"
  description   = "docker repository"
  format        = "DOCKER"
}