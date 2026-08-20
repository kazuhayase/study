-- Migration 002: Bronze layer — raw upstream payloads, stored as fetched
-- Target: DuckDB
-- Principle: store the payload verbatim; no interpretation. Silver is rebuilt from here,
--            so a parser bug never requires re-downloading 380k CVEs from NVD.
--
-- Deviation from talent-mgmt-db Bronze (documented deliberately): these tables keep only the
-- CURRENT version of each record rather than every generation. Upstream feeds are themselves
-- append-mostly and re-fetchable, and 380k CVEs x full history would run to tens of GB.
-- The exception is EPSS, where the daily time series IS the data, so it accumulates.

CREATE SCHEMA IF NOT EXISTS bronze;

-- NVD CVE API 2.0 records. raw_json is vulnerabilities[].cve verbatim.
-- Measured 2026-08-20: avg 5,468 B/CVE over a 2,000-CVE sample; ~2.08 GB across all 380,688.
-- `configurations` is 26% of that and is retained: re-pulling 380k CVEs later to recover CPE
-- data for asset matching would cost far more than the storage.
CREATE TABLE IF NOT EXISTS bronze.nvd_cve (
    cve_id               VARCHAR    NOT NULL PRIMARY KEY,
    raw_json             JSON       NOT NULL,
    source_last_modified TIMESTAMP,                    -- cve.lastModified; drives incremental upsert
    fetched_at           TIMESTAMP  NOT NULL DEFAULT CURRENT_TIMESTAMP,
    fetch_id             VARCHAR    NOT NULL
);

-- CISA KEV catalog entries. raw_json is one element of the catalog's vulnerabilities[].
CREATE TABLE IF NOT EXISTS bronze.kev (
    cve_id          VARCHAR    NOT NULL PRIMARY KEY,
    raw_json        JSON       NOT NULL,
    catalog_version VARCHAR,                           -- e.g. '2026.08.19'
    fetched_at      TIMESTAMP  NOT NULL DEFAULT CURRENT_TIMESTAMP,
    fetch_id        VARCHAR    NOT NULL
);

-- CISA Vulnrichment ADP records. raw_json is the full CVE record file from the repo,
-- from which the CISA-ADP container is extracted in Silver.
CREATE TABLE IF NOT EXISTS bronze.vulnrichment (
    cve_id      VARCHAR    NOT NULL PRIMARY KEY,
    raw_json    JSON       NOT NULL,
    commit_sha  VARCHAR,                               -- repo commit this file was read at
    fetched_at  TIMESTAMP  NOT NULL DEFAULT CURRENT_TIMESTAMP,
    fetch_id    VARCHAR    NOT NULL
);

-- EPSS daily scores. Append-only time series -- this is the one Bronze table that keeps history.
CREATE TABLE IF NOT EXISTS bronze.epss (
    cve_id      VARCHAR    NOT NULL,
    score_date  DATE       NOT NULL,
    epss        DOUBLE     NOT NULL,                   -- probability of exploitation in next 30 days
    percentile  DOUBLE     NOT NULL,
    model_version VARCHAR,                             -- from the CSV's leading '#model_version:' line
    fetched_at  TIMESTAMP  NOT NULL DEFAULT CURRENT_TIMESTAMP,
    fetch_id    VARCHAR    NOT NULL,
    PRIMARY KEY (cve_id, score_date)
);
