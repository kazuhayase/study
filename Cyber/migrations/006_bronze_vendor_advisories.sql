-- Migration 006: Bronze layer — vendor security advisories (AWS, Microsoft, Broadcom, IBM)
-- Target: DuckDB
-- Principle: store the payload verbatim, same as 002. raw_json is a single advisory record
--            in whatever shape that vendor's feed returns (RSS item, CVRF vulnerability,
--            API list entry) -- see transform.py for the per-vendor parsers.

CREATE SCHEMA IF NOT EXISTS bronze;

CREATE TABLE IF NOT EXISTS bronze.vendor_advisories (
    vendor        VARCHAR    NOT NULL,   -- 'aws' | 'microsoft' | 'broadcom' | 'ibm'
    advisory_id   VARCHAR    NOT NULL,   -- AWS: Bulletin ID; MSRC: CVE ID; Broadcom: documentId; IBM: nid
    raw_json      JSON       NOT NULL,
    fetched_at    TIMESTAMP  NOT NULL DEFAULT CURRENT_TIMESTAMP,
    fetch_id      VARCHAR    NOT NULL,
    PRIMARY KEY (vendor, advisory_id)
);
