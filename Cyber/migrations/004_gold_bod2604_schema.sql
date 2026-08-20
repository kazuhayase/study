-- Migration 004: Gold layer — BOD 26-04 remediation timelines
-- Target: DuckDB
-- Principle: Gold is views over Silver wherever possible, so it recomputes on every run
--            and can never drift from its inputs. Only the directive's own lookup table
--            is materialised, because it is legislation, not derived data.

CREATE SCHEMA IF NOT EXISTS gold;

-- Appendix A, Table 1 of BOD 26-04. Seeded by 005; see that file for provenance.
CREATE TABLE IF NOT EXISTS gold.bod2604_matrix (
    matrix_row               INTEGER   NOT NULL PRIMARY KEY,  -- 1-16, as numbered in the directive
    publicly_exposed         BOOLEAN   NOT NULL,
    in_kev                   BOOLEAN   NOT NULL,
    automatable              BOOLEAN   NOT NULL,
    technical_impact         VARCHAR   NOT NULL,   -- 'total' | 'partial'
    remediation_days         INTEGER,              -- NULL means "fix on system upgrade"
    forensic_triage_required BOOLEAN   NOT NULL,
    tier_label               VARCHAR   NOT NULL
);

-- Per-CVE evaluation against the directive.
--
-- Asset exposure is the one variable CISA does not publish -- it is a property of an agency's
-- asset, not of the CVE (directive: "Agencies should follow CISA's Internet Exposure Reduction
-- Guidance"). With no asset inventory in scope yet, this view resolves BOTH branches so the
-- answer is ready the moment a findings table lands: *_if_exposed and *_if_internal.
--
-- matrix_row_* is carried through deliberately. The directive requires agencies to "explain why
-- certain vulnerabilities were remediated first", and citing row N of Table 1 is that explanation.
CREATE OR REPLACE VIEW gold.cve_bod2604 AS
WITH base AS (
    SELECT
        c.cve_id,
        c.published,
        c.last_modified,
        c.vuln_status,
        c.cvss_v31_base_score,
        c.cvss_v31_severity,
        (k.cve_id IS NOT NULL)          AS in_kev,
        k.date_added                    AS kev_date_added,
        k.known_ransomware_campaign_use,
        s.exploitation,
        s.automatable,
        s.technical_impact,
        s.source                        AS ssvc_source,
        e.epss,
        e.percentile                    AS epss_percentile
    FROM silver.cve c
    LEFT JOIN silver.kev          k ON k.cve_id = c.cve_id
    LEFT JOIN silver.ssvc         s ON s.cve_id = c.cve_id
    LEFT JOIN silver.epss_current e ON e.cve_id = c.cve_id
    WHERE c.is_rejected = FALSE
)
SELECT
    b.cve_id,
    b.published,
    b.last_modified,
    b.vuln_status,
    b.cvss_v31_base_score,
    b.cvss_v31_severity,
    b.in_kev,
    b.kev_date_added,
    b.known_ransomware_campaign_use,
    b.exploitation,
    b.automatable,
    b.technical_impact,
    b.ssvc_source,
    b.epss,
    b.epss_percentile,
    -- Both SSVC variables must be present for the directive's matrix to resolve at all.
    (b.automatable IS NOT NULL AND b.technical_impact IS NOT NULL) AS ssvc_known,

    mx.matrix_row               AS matrix_row_if_exposed,
    mx.remediation_days         AS days_if_exposed,
    mx.forensic_triage_required AS triage_if_exposed,
    mx.tier_label               AS tier_if_exposed,

    mi.matrix_row               AS matrix_row_if_internal,
    mi.remediation_days         AS days_if_internal,
    mi.forensic_triage_required AS triage_if_internal,
    mi.tier_label               AS tier_if_internal,

    -- Directive, Appendix A: "The timelines defined in Table 1 begin when either (1) CISA adds
    -- the vulnerability to the KEV Catalog, or (2) ... the agency enumerates or identifies the
    -- vulnerability on an asset ... Whichever event occurs first starts the remediation timeline."
    -- Event (2) requires an asset inventory, so only event (1) is knowable here. Deadlines are
    -- therefore computable only for KEV entries; everything else waits on detection data.
    -- AUDIT REQUIRED: once a findings table exists, this becomes LEAST(kev_date_added, detected_at).
    b.kev_date_added AS clock_start,
    CASE WHEN b.kev_date_added IS NOT NULL AND mx.remediation_days IS NOT NULL
         THEN b.kev_date_added + CAST(mx.remediation_days AS INTEGER) END AS due_date_if_exposed,
    CASE WHEN b.kev_date_added IS NOT NULL AND mi.remediation_days IS NOT NULL
         THEN b.kev_date_added + CAST(mi.remediation_days AS INTEGER) END AS due_date_if_internal
FROM base b
LEFT JOIN gold.bod2604_matrix mx
       ON mx.publicly_exposed = TRUE
      AND mx.in_kev           = b.in_kev
      AND mx.automatable      = (b.automatable = 'yes')
      AND mx.technical_impact = b.technical_impact
LEFT JOIN gold.bod2604_matrix mi
       ON mi.publicly_exposed = FALSE
      AND mi.in_kev           = b.in_kev
      AND mi.automatable      = (b.automatable = 'yes')
      AND mi.technical_impact = b.technical_impact;

-- The working queue this database exists to produce.
--
-- CISA enriches only part of the CVE corpus, so for the remainder an agency must determine
-- Automatable and Technical Impact itself. That is a large manual backlog and the directive
-- gives no order to work it in. EPSS does: it estimates probability of exploitation in the next
-- 30 days, which is exactly the axis that decides whether an un-triaged CVE can wait.
-- KEV entries missing SSVC rank first regardless -- they are already on the clock.
CREATE OR REPLACE VIEW gold.ssvc_gap_triage AS
SELECT
    cve_id,
    published,
    in_kev,
    kev_date_added,
    cvss_v31_base_score,
    cvss_v31_severity,
    epss,
    epss_percentile,
    exploitation,
    automatable,
    technical_impact,
    CASE
        WHEN automatable IS NULL AND technical_impact IS NULL THEN 'both_missing'
        WHEN automatable IS NULL                              THEN 'automatable_missing'
        ELSE 'technical_impact_missing'
    END AS gap
FROM gold.cve_bod2604
WHERE ssvc_known = FALSE
ORDER BY in_kev DESC, epss_percentile DESC NULLS LAST, cvss_v31_base_score DESC NULLS LAST;

-- Coverage by CVE year. Measured 2026-08-20: a 2,000-CVE sample of recent IDs showed 82% SSVC
-- coverage against ~46% corpus-wide, so a single headline number hides where the gap actually is.
CREATE OR REPLACE VIEW gold.coverage_stats AS
SELECT
    CAST(SUBSTR(cve_id, 5, 4) AS INTEGER)                       AS cve_year,
    COUNT(*)                                                    AS total_cves,
    SUM(CASE WHEN ssvc_known    THEN 1 ELSE 0 END)              AS with_ssvc,
    ROUND(100.0 * SUM(CASE WHEN ssvc_known THEN 1 ELSE 0 END) / COUNT(*), 1) AS ssvc_pct,
    SUM(CASE WHEN in_kev        THEN 1 ELSE 0 END)              AS in_kev,
    SUM(CASE WHEN epss IS NOT NULL THEN 1 ELSE 0 END)           AS with_epss,
    SUM(CASE WHEN in_kev AND NOT ssvc_known THEN 1 ELSE 0 END)  AS kev_without_ssvc
FROM gold.cve_bod2604
GROUP BY 1
ORDER BY 1 DESC;
