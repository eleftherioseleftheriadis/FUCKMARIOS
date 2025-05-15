# Vault Backup and Recovery Guide

This document provides guidance on how to restore the Vault database and KMS configuration in case of failures.

## Table of Contents

- [Introduction](#introduction)
- [Restoring the Database](#restoring-the-database)
- [Restoring KMS Configuration](#restoring-kms-configuration)

## Introduction

In the event of an issue with the Vault's database or KMS, follow the procedures outlined below to restore functionality. 

## Restoring the Database

Vault is deployed on a highly available (HA) PostgreSQL RDS. If there is a problem with this RDS, you can restore a snapshot into another availability zone and update the Vault connection string in the Vault config map, and restart pods or stateful set

### Configuration Example

Here is an example of the configuration you might use in your Vault setup:

```hcl
storage "postgresql" {
  connection_url = "postgres://xxx:xxx@postgre-dev-rds-ew1-01.czwe8eg2u3zm.eu-west-1.rds.amazonaws.com:5432/vault"
  table          = "vault_kv_store"
  ha_enabled     = true
  ha_table       = "vault_ha_locks"
}
```

## Restoring KMS Configuration
In case something goes wrong with the KMS, we are using a regional KMS. You can simply change the region in the Vault config map.

### Configuration Example
Below is an example of the KMS configuration in your Vault setup:

```hcl
seal "awskms" {
  region     = "eu-central-1"
  kms_key_id = "alias/vault_dev"
  disabled   = "false"
}
```