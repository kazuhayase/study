-- Migration 005: Seed — BOD 26-04 Appendix A, Table 1: Remediation Timelines
--
-- SOURCE OF TRUTH. Transcribed 2026-08-20 from the directive itself, not from commentary:
--   Directive : https://www.cisa.gov/news-events/directives/bod-26-04-prioritizing-security-updates-based-risk
--   Table 1   : https://www.cisa.gov/sites/default/files/2026-06/BOD_26-04_Table_1_Remediation_Timelines_0.png
-- The table is published on that page as an image, so it was read from the PNG directly.
-- Row numbers below are the directive's own numbering, preserved so a finding can cite "Table 1 row 9".
--
-- NOTE: cisa.gov rejects some automated fetchers with HTTP 403; a normal browser User-Agent
-- retrieves it fine. Re-verify this table whenever CISA revises the directive -- Appendix A commits
-- CISA to "a formal, data-driven reassessment of the prioritization timelines ... once per fiscal
-- year", so these values are expected to change. tests/test_bod2604.py fails loudly if they drift.
--
-- Directive definitions carried into the columns below:
--   Publicly Exposed : asset "accessible to unauthenticated or untrusted entities via public
--                      networks, such as the internet, regardless of its physical or logical location"
--   In the KEV       : the CVE ID has an entry in the KEV Catalog
--   Automatable      : adversary can automate all steps necessary to exploit
--   Technical Impact : 'total' = total control of the software's behaviour; 'partial' = limited
--                      control/information exposure, or only a low stochastic shot at total control
--   "& forensic triage" : remediate or mitigate within three days AND assess whether the system
--                      is already compromised
--   Days are calendar days.

DELETE FROM gold.bod2604_matrix;

INSERT INTO gold.bod2604_matrix
    (matrix_row, publicly_exposed, in_kev, automatable, technical_impact,
     remediation_days, forensic_triage_required, tier_label)
VALUES
    ( 1, TRUE,  TRUE,  TRUE,  'total',     3, TRUE,  '3 days & forensic triage'),
    ( 2, TRUE,  TRUE,  TRUE,  'partial',   3, FALSE, '3 days'),
    ( 3, TRUE,  TRUE,  FALSE, 'total',     3, TRUE,  '3 days & forensic triage'),
    ( 4, TRUE,  TRUE,  FALSE, 'partial',  14, FALSE, '14 days'),
    ( 5, TRUE,  FALSE, TRUE,  'total',     3, FALSE, '3 days'),
    ( 6, TRUE,  FALSE, TRUE,  'partial',  14, FALSE, '14 days'),
    ( 7, TRUE,  FALSE, FALSE, 'total',    14, FALSE, '14 days'),
    ( 8, TRUE,  FALSE, FALSE, 'partial',  60, FALSE, '60 days'),
    ( 9, FALSE, TRUE,  TRUE,  'total',     3, TRUE,  '3 days & forensic triage'),
    (10, FALSE, TRUE,  TRUE,  'partial',  14, FALSE, '14 days'),
    (11, FALSE, TRUE,  FALSE, 'total',    14, FALSE, '14 days'),
    (12, FALSE, TRUE,  FALSE, 'partial',  14, FALSE, '14 days'),
    (13, FALSE, FALSE, TRUE,  'total',    60, FALSE, '60 days'),
    (14, FALSE, FALSE, TRUE,  'partial',  60, FALSE, '60 days'),
    (15, FALSE, FALSE, FALSE, 'total',  NULL, FALSE, 'Fix on system upgrade'),
    (16, FALSE, FALSE, FALSE, 'partial', NULL, FALSE, 'Fix on system upgrade');
