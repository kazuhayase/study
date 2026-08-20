-- Migration 001: Meta layer — migration tracking, fetch provenance, incremental sync state
-- Target: DuckDB
-- Principle: every network fetch leaves a row here, success or failure. Nothing is silent.
--
-- Mirrors the load_log / file_registry convention from talent-mgmt-db's Bronze migration:
-- provenance is a first-class table, not a side effect of logging.

CREATE SCHEMA IF NOT EXISTS meta;

-- Applied migrations. The runner in src/vulndb/db.py consults this before each file.
CREATE TABLE IF NOT EXISTS meta.schema_migrations (
    filename    VARCHAR     NOT NULL PRIMARY KEY,
    checksum    VARCHAR     NOT NULL,   -- sha256 of the file, to detect edits after apply
    applied_at  TIMESTAMP   NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- One row per fetch attempt against an upstream feed, including failures.
CREATE TABLE IF NOT EXISTS meta.fetch_log (
    fetch_id      VARCHAR    NOT NULL PRIMARY KEY,   -- uuid4 generated at start of fetch
    source        VARCHAR    NOT NULL,               -- 'nvd' | 'kev' | 'epss' | 'vulnrichment'
    mode          VARCHAR    NOT NULL,               -- 'init' | 'update'
    status        VARCHAR    NOT NULL,               -- 'success' | 'partial' | 'failed'
    rows_ingested INTEGER,
    rows_skipped  INTEGER,                           -- items that failed to parse but did not abort the run
    detail        VARCHAR,                           -- window fetched, commit sha, score date, ...
    error_message VARCHAR,
    started_at    TIMESTAMP  NOT NULL,
    finished_at   TIMESTAMP
);

-- Resume points for incremental updates. One row per source; updated only on success.
CREATE TABLE IF NOT EXISTS meta.sync_state (
    source      VARCHAR    NOT NULL PRIMARY KEY,   -- 'nvd' | 'kev' | 'epss' | 'vulnrichment'
    -- Meaning is source-specific:
    --   nvd           -> max lastModified seen, as ISO-8601 (the lastModStartDate watermark)
    --   vulnrichment  -> git commit sha the working copy was synced to
    --   epss          -> score_date of the most recently ingested daily file
    --   kev           -> catalogVersion of the most recently ingested catalog
    cursor      VARCHAR,
    updated_at  TIMESTAMP  NOT NULL DEFAULT CURRENT_TIMESTAMP
);
