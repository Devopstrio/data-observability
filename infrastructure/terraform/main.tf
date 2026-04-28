provider "azurerm" {
  features {}
}

provider "aws" {
  region = var.aws_region
}

resource "azurerm_resource_group" "observability" {
  name     = "rg-${var.project_name}-observability-${var.environment}"
  location = var.location
}

# --- Observability Control Plane (AKS) ---

resource "azurerm_kubernetes_cluster" "observability_k8s" {
  name                = "aks-data-obs-${var.environment}"
  location            = azurerm_resource_group.observability.location
  resource_group_name = azurerm_resource_group.observability.name
  dns_prefix          = "obs-k8s"

  default_node_pool {
    name       = "default"
    node_count = 3
    vm_size    = "Standard_D2s_v3"
  }

  identity {
    type = "SystemAssigned"
  }
}

# --- Reliability Metadata Store (Postgres) ---

resource "azurerm_postgresql_flexible_server" "metadata" {
  name                   = "psql-obs-metadata-${var.environment}"
  resource_group_name    = azurerm_resource_group.observability.name
  location               = azurerm_resource_group.observability.location
  version                = "13"
  administrator_login    = "obsadmin"
  administrator_password = var.db_password
  storage_mb             = 32768
  sku_name               = "GP_Standard_D2ds_v4"
}

# --- Telemetry Time-Series Cache (Redis) ---

resource "azurerm_redis_cache" "telemetry_cache" {
  name                = "redis-obs-telemetry-${var.environment}"
  location            = azurerm_resource_group.observability.location
  resource_group_name = azurerm_resource_group.observability.name
  capacity            = 1
  family              = "C"
  sku_name            = "Standard"
  enable_non_ssl_port = false
}

# --- Multi-Cloud Telemetry Sinks (S3/Azure Blob) ---

resource "aws_s3_bucket" "telemetry_archive" {
  bucket = "data-obs-telemetry-archive-${var.environment}"
}
