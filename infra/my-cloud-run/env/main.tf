locals {
  # If pr tf workspace, add suffix, like <resource_name>_PR-123, e.g. my_dataset_PR-123
  suffix = terraform.workspace == "default" ? "" : "_${terraform.workspace}"

  # Service name can only contain lowercase, digits, and hyphens, e.g. my-cr-PR-123
  cloud_run_suffix = replace(local.suffix, "_", "-")
}
