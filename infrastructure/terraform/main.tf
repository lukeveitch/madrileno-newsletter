terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 4.51"
    }
  }
}

provider "google" {
  project = "madrid-newsletter"
  region  = "us-central1"
}

# GCS Bucket for data lake (bronze/silver layers)
resource "google_storage_bucket" "data_lake" {
  name          = "madrid-newsletter-data-lake"
  location      = "US"
  storage_class = "STANDARD"
  
  uniform_bucket_level_access = true
  
  versioning {
    enabled = true
  }
  
  lifecycle_rule {
    action {
      type = "Delete"
    }
    condition {
      age = 30  # days
    }
  }
  
  force_destroy = true
}

# BigQuery dataset for raw data (bronze layer)
resource "google_bigquery_dataset" "bronze" {
  dataset_id = "bronze"
  project    = "madrid-newsletter"
  location   = "US"
  
  description = "Raw data from APIs - bronze layer"
}

# BigQuery dataset for processed data (silver layer)
resource "google_bigquery_dataset" "silver" {
  dataset_id = "silver"
  project    = "madrid-newsletter" 
  location   = "US"
  
  description = "Cleaned and processed data - silver layer"
}

# BigQuery dataset for analytics (gold layer)
resource "google_bigquery_dataset" "gold" {
  dataset_id = "gold"
  project    = "madrid-newsletter"
  location   = "US"
  
  description = "Analytics-ready data - gold layer"
}
