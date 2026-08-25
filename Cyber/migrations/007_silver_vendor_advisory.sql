-- Migration 007: Silver layer — vendor advisories parsed and linked to CVE IDs
-- Target: DuckDB
-- Principle: fully re-derivable from bronze.vendor_advisories, same as 003.
--            Not part of the BOD 26-04 Gold views (out of scope here) -- this is a landing
--            point for downstream systems to join against on cve_id.

CREATE SCHEMA IF NOT EXISTS silver;

CREATE TABLE IF NOT EXISTS silver.vendor_advisory (
    vendor          VARCHAR    NOT NULL,
    advisory_id     VARCHAR    NOT NULL,
    title           VARCHAR,
    url             VARCHAR,
    published_date  DATE,
    severity        VARCHAR,   -- vendor's own severity label, verbatim (not normalised across vendors)
    cve_ids         VARCHAR[],
    PRIMARY KEY (vendor, advisory_id)
);

-- One row per (advisory, CVE) pair -- the join key for linking against silver.cve or an
-- external database.
CREATE OR REPLACE VIEW silver.vendor_advisory_cve AS
SELECT vendor, advisory_id, unnest(cve_ids) AS cve_id
FROM silver.vendor_advisory;
