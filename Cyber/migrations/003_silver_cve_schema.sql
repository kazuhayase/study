-- Migration 003: Silver layer — typed, deduplicated, one row per CVE per concern
-- Target: DuckDB
-- Principle: Silver is fully re-derivable from Bronze. Never patch Silver by hand;
--            fix the transform and re-run `python -m vulndb rebuild`.

CREATE SCHEMA IF NOT EXISTS silver;

CREATE TABLE IF NOT EXISTS silver.cve (
    cve_id               VARCHAR   NOT NULL PRIMARY KEY,
    published            TIMESTAMP,
    last_modified        TIMESTAMP,
    vuln_status          VARCHAR,          -- Analyzed | Modified | Awaiting Analysis | Rejected ...
    description_en       VARCHAR,
    cvss_v31_base_score  DOUBLE,
    cvss_v31_severity    VARCHAR,
    cvss_v31_vector      VARCHAR,
    cvss_v40_base_score  DOUBLE,
    cvss_v40_severity    VARCHAR,
    cvss_v40_vector      VARCHAR,
    cwe_ids              VARCHAR[],
    source_identifier    VARCHAR,
    -- BOD 26-04 scopes remediation by CVE ID, so rejected records must be excluded from
    -- the Gold views rather than silently counted. Kept here for auditability.
    is_rejected          BOOLEAN   NOT NULL DEFAULT FALSE
);

-- KEV membership. The catalog feed is authoritative and overrides NVD's cisaExploitAdd,
-- because NVD's copy lags the catalog and lacks knownRansomwareCampaignUse entirely.
CREATE TABLE IF NOT EXISTS silver.kev (
    cve_id                        VARCHAR   NOT NULL PRIMARY KEY,
    date_added                    DATE,     -- starts the BOD 26-04 remediation clock (see gold)
    due_date                      DATE,     -- CISA's own due date; BOD 22-01 era, informational now
    known_ransomware_campaign_use VARCHAR,  -- 'Known' | 'Unknown'
    vendor_project                VARCHAR,
    product                       VARCHAR,
    vulnerability_name            VARCHAR,
    required_action               VARCHAR,
    notes                         VARCHAR,
    source                        VARCHAR   NOT NULL   -- 'kev_catalog' | 'nvd'
);

-- SSVC decision points supplying two of BOD 26-04's four variables.
--
-- Two upstream shapes feed this table and their key casing differs -- verified against live
-- data on 2026-08-20:
--   NVD API 2.0 : cve.metrics.ssvcV203[].ssvcData.options[] -> {"exploitation","automatable","technicalImpact"}
--   Vulnrichment: containers.adp[].metrics[].content.options[] -> {"Exploitation","Automatable","Technical Impact"}
-- Vulnrichment wins on conflict: it is the origin of the data and NVD's copy can lag.
CREATE TABLE IF NOT EXISTS silver.ssvc (
    cve_id           VARCHAR   NOT NULL PRIMARY KEY,
    exploitation     VARCHAR,            -- 'none' | 'poc' | 'active'  (context, not a BOD variable)
    automatable      VARCHAR,            -- 'yes' | 'no'               (BOD variable 3)
    technical_impact VARCHAR,            -- 'partial' | 'total'        (BOD variable 4)
    ssvc_version     VARCHAR,            -- e.g. '2.0.3'
    role             VARCHAR,            -- e.g. 'CISA Coordinator'
    decided_at       TIMESTAMP,          -- the SSVC record's own timestamp
    source           VARCHAR   NOT NULL  -- 'vulnrichment' | 'nvd'
);

-- Latest EPSS score per CVE. Not a BOD 26-04 variable: used to rank the CVEs that have NO
-- SSVC coverage, so manual assessment happens in a defensible order (see gold.ssvc_gap_triage).
CREATE TABLE IF NOT EXISTS silver.epss_current (
    cve_id      VARCHAR   NOT NULL PRIMARY KEY,
    epss        DOUBLE    NOT NULL,
    percentile  DOUBLE    NOT NULL,
    score_date  DATE      NOT NULL
);
