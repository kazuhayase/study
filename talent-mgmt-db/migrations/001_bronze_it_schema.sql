-- Migration 001: Bronze layer — IT entity Excel ingestion
-- Target: Snowflake (raw_it schema)
-- Principle: store everything as VARCHAR; no interpretation; append provenance only.
-- Bronze records are immutable. Re-run Silver from Bronze; never mutate Bronze.
--
-- AUDIT REQUIRED markers = columns whose names/existence must be confirmed
-- against a real IT entity Excel file before promoting this schema to production.

CREATE SCHEMA IF NOT EXISTS raw_it;

-- ---------------------------------------------------------------------------
-- File registry: one row per loaded Excel file.
-- All other raw_it tables FK to this via source_file_id.
-- ---------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS raw_it.file_registry (
    file_id         VARCHAR         NOT NULL PRIMARY KEY,  -- UUID generated at load time
    file_name       VARCHAR         NOT NULL,              -- original filename on stage
    stage_path      VARCHAR         NOT NULL,              -- @stage/path/to/file.xlsx
    entity          VARCHAR         NOT NULL DEFAULT 'it_subsidiary',
    file_vintage    VARCHAR,                               -- e.g. '2025H2', '2026Q1' — parsed from filename or manual tag
    sheet_names     VARIANT,                               -- JSON array of sheet names found in the file
    row_count       INT,                                   -- total data rows loaded across all sheets
    loaded_at       TIMESTAMP_NTZ   NOT NULL DEFAULT CURRENT_TIMESTAMP(),
    loaded_by       VARCHAR                                -- Snowflake user / SP name that ran the load
);

-- ---------------------------------------------------------------------------
-- Employee info: one row per employee per file.
-- Sourced from the header / personal info section of the Excel.
-- ---------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS raw_it.employee_info (
    row_id              VARCHAR         NOT NULL PRIMARY KEY,  -- UUID
    source_file_id      VARCHAR         NOT NULL REFERENCES raw_it.file_registry(file_id),
    source_sheet        VARCHAR,                               -- sheet name this row came from
    source_row_num      INT,                                   -- 1-based row number in sheet

    -- AUDIT REQUIRED: confirm these column names exist in your Excel
    employee_number     VARCHAR,    -- 社員番号 — Q2 blocker: is this consistent across files?
    name_kanji          VARCHAR,    -- 氏名 (kanji)
    name_kana           VARCHAR,    -- 氏名 (kana) — AUDIT REQUIRED: present?
    entity_name         VARCHAR,    -- 会社名 / 所属会社 — AUDIT REQUIRED: present in IT entity files?
    department          VARCHAR,    -- 部署名 / 所属部門
    job_title           VARCHAR,    -- 役職 / 職位 — AUDIT REQUIRED: column name varies
    hire_date           VARCHAR,    -- 入社日 (raw string; Silver parses to DATE)
    assessment_date     VARCHAR,    -- 評価日 / 提出日 — AUDIT REQUIRED: present?

    -- catch-all for any extra columns found during audit
    extra_fields        VARIANT,    -- JSON map of {column_header: raw_cell_value}

    loaded_at           TIMESTAMP_NTZ NOT NULL DEFAULT CURRENT_TIMESTAMP()
);

-- ---------------------------------------------------------------------------
-- Skill scores: one row per skill item per employee per file.
-- The ITSS/DSS grid has one skill per row with level and experience columns.
-- ---------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS raw_it.skill_scores (
    row_id              VARCHAR         NOT NULL PRIMARY KEY,
    source_file_id      VARCHAR         NOT NULL REFERENCES raw_it.file_registry(file_id),
    source_sheet        VARCHAR,
    source_row_num      INT,

    employee_number     VARCHAR,    -- 社員番号 — join key back to employee_info; AUDIT REQUIRED

    -- AUDIT REQUIRED: confirm category hierarchy depth (1 level? 2? 3?)
    skill_category_l1   VARCHAR,    -- top-level category (e.g. ITスキル標準職種)
    skill_category_l2   VARCHAR,    -- sub-category — AUDIT REQUIRED: exists?
    skill_item          VARCHAR,    -- individual skill name as written in Excel

    level_score         VARCHAR,    -- 1-5 self-assessed level (VARCHAR in Bronze; Silver casts to INT)
    experience_score    VARCHAR,    -- 1-5 self-assessed experience (VARCHAR in Bronze)

    -- AUDIT REQUIRED: some ITSS files have a manager override column
    manager_score       VARCHAR,    -- manager-assessed level — AUDIT REQUIRED: present?
    comments            VARCHAR,    -- 備考 / コメント — AUDIT REQUIRED: present?

    extra_fields        VARIANT,

    loaded_at           TIMESTAMP_NTZ NOT NULL DEFAULT CURRENT_TIMESTAMP()
);

-- ---------------------------------------------------------------------------
-- Job history: one row per raw text block from the career history section.
-- Multi-line cells land here as a single raw_text blob.
-- Silver splits this into structured records via Cortex COMPLETE().
-- ---------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS raw_it.job_history (
    row_id              VARCHAR         NOT NULL PRIMARY KEY,
    source_file_id      VARCHAR         NOT NULL REFERENCES raw_it.file_registry(file_id),
    source_sheet        VARCHAR,
    source_row_num      INT,

    employee_number     VARCHAR,    -- AUDIT REQUIRED

    -- AUDIT REQUIRED: is job history one cell per row, or a merged/multi-line cell?
    -- If a single merged cell contains multiple roles, raw_text will contain newlines.
    raw_text            VARCHAR,    -- full cell content, newlines preserved
    cell_address        VARCHAR,    -- e.g. 'B42' — helps trace back to source

    extra_fields        VARIANT,

    loaded_at           TIMESTAMP_NTZ NOT NULL DEFAULT CURRENT_TIMESTAMP()
);

-- ---------------------------------------------------------------------------
-- Load audit log: SP writes one row per load attempt (success or failure).
-- ---------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS raw_it.load_log (
    log_id          VARCHAR         NOT NULL PRIMARY KEY,
    file_id         VARCHAR,        -- NULL if load failed before file_registry insert
    file_name       VARCHAR,
    status          VARCHAR         NOT NULL,   -- 'success' | 'partial' | 'failed'
    rows_loaded     INT,
    error_message   VARCHAR,
    started_at      TIMESTAMP_NTZ   NOT NULL,
    finished_at     TIMESTAMP_NTZ
);
