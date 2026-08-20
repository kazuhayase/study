#!/usr/bin/env python3
"""Verify the BOD 26-04 decision matrix and the Gold view that applies it.

The 16 rows below are transcribed independently of migrations/005 -- both come from Appendix A,
Table 1 of the directive, and this test exists to catch the day they stop agreeing. CISA has
committed to reassessing those timelines annually, so drift is expected eventually, and it must
fail loudly rather than quietly re-prioritise someone's patching queue.

Run: python3 tests/test_bod2604.py
"""

import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from vulndb import db  # noqa: E402

# (row, publicly_exposed, in_kev, automatable, technical_impact, days, forensic_triage)
# Source: https://www.cisa.gov/sites/default/files/2026-06/BOD_26-04_Table_1_Remediation_Timelines_0.png
EXPECTED_MATRIX = [
    ( 1, True,  True,  True,  "total",      3, True),
    ( 2, True,  True,  True,  "partial",    3, False),
    ( 3, True,  True,  False, "total",      3, True),
    ( 4, True,  True,  False, "partial",   14, False),
    ( 5, True,  False, True,  "total",      3, False),
    ( 6, True,  False, True,  "partial",   14, False),
    ( 7, True,  False, False, "total",     14, False),
    ( 8, True,  False, False, "partial",   60, False),
    ( 9, False, True,  True,  "total",      3, True),
    (10, False, True,  True,  "partial",   14, False),
    (11, False, True,  False, "total",     14, False),
    (12, False, True,  False, "partial",   14, False),
    (13, False, False, True,  "total",     60, False),
    (14, False, False, True,  "partial",   60, False),
    (15, False, False, False, "total",   None, False),
    (16, False, False, False, "partial", None, False),
]

failures = []


def check(name, cond, detail=""):
    if cond:
        print(f"  ok   {name}")
    else:
        print(f"  FAIL {name} {detail}")
        failures.append(name)


def main():
    tmp = Path(tempfile.mkdtemp()) / "test.duckdb"
    con = db.connect(tmp)
    db.migrate(con, verbose=False)

    print("matrix seed")
    rows = con.execute(
        """
        SELECT matrix_row, publicly_exposed, in_kev, automatable, technical_impact,
               remediation_days, forensic_triage_required
        FROM gold.bod2604_matrix ORDER BY matrix_row
        """
    ).fetchall()
    check("16 rows seeded", len(rows) == 16, f"got {len(rows)}")
    for expected in EXPECTED_MATRIX:
        actual = next((r for r in rows if r[0] == expected[0]), None)
        check(f"row {expected[0]:>2}", tuple(actual) == expected if actual else False,
              f"expected {expected}, got {tuple(actual) if actual else None}")

    # Every combination must resolve to exactly one row, or the view's join silently drops CVEs.
    distinct = con.execute(
        "SELECT count(DISTINCT (publicly_exposed, in_kev, automatable, technical_impact)) "
        "FROM gold.bod2604_matrix"
    ).fetchone()[0]
    check("all 16 variable combinations distinct", distinct == 16, f"got {distinct}")

    print("\ndirective invariants")
    triage = con.execute(
        "SELECT count(*) FROM gold.bod2604_matrix WHERE forensic_triage_required"
    ).fetchone()[0]
    check("forensic triage on exactly 3 rows", triage == 3, f"got {triage}")
    check(
        "forensic triage implies KEV + total control + 3 days",
        con.execute(
            """
            SELECT count(*) FROM gold.bod2604_matrix
            WHERE forensic_triage_required
              AND NOT (in_kev AND technical_impact = 'total' AND remediation_days = 3)
            """
        ).fetchone()[0] == 0,
    )
    check(
        "fix-on-upgrade only when no criterion is met",
        con.execute(
            """
            SELECT count(*) FROM gold.bod2604_matrix
            WHERE remediation_days IS NULL
              AND (publicly_exposed OR in_kev OR automatable)
            """
        ).fetchone()[0] == 0,
    )
    check(
        "exposure never relaxes a deadline",
        con.execute(
            """
            SELECT count(*) FROM gold.bod2604_matrix e
            JOIN gold.bod2604_matrix i
              ON i.publicly_exposed = FALSE AND e.publicly_exposed = TRUE
             AND i.in_kev = e.in_kev AND i.automatable = e.automatable
             AND i.technical_impact = e.technical_impact
            WHERE coalesce(e.remediation_days, 99999) > coalesce(i.remediation_days, 99999)
            """
        ).fetchone()[0] == 0,
    )

    print("\ngold.cve_bod2604 view")
    # One synthetic CVE per matrix row, plus one with no SSVC at all.
    for row, _exposed, in_kev, automatable, impact, _days, _triage in EXPECTED_MATRIX:
        cve_id = f"CVE-2026-{9000 + row}"
        con.execute(
            "INSERT INTO silver.cve (cve_id, published, vuln_status, is_rejected) "
            "VALUES (?, '2026-01-01', 'Analyzed', FALSE)", [cve_id]
        )
        con.execute(
            "INSERT INTO silver.ssvc (cve_id, automatable, technical_impact, source) "
            "VALUES (?, ?, ?, 'test')",
            [cve_id, "yes" if automatable else "no", impact],
        )
        if in_kev:
            con.execute(
                "INSERT OR IGNORE INTO silver.kev (cve_id, date_added, source) "
                "VALUES (?, '2026-06-10', 'test')", [cve_id]
            )

    con.execute(
        "INSERT INTO silver.cve (cve_id, published, vuln_status, is_rejected) "
        "VALUES ('CVE-2026-9999', '2026-01-01', 'Analyzed', FALSE)"
    )
    con.execute(
        "INSERT INTO silver.cve (cve_id, published, vuln_status, is_rejected) "
        "VALUES ('CVE-2026-8888', '2026-01-01', 'Rejected', TRUE)"
    )

    for row, exposed, _kev, _auto, _impact, days, triage in EXPECTED_MATRIX:
        cve_id = f"CVE-2026-{9000 + row}"
        got = con.execute(
            """
            SELECT days_if_exposed, triage_if_exposed, days_if_internal, triage_if_internal,
                   matrix_row_if_exposed, matrix_row_if_internal, ssvc_known
            FROM gold.cve_bod2604 WHERE cve_id = ?
            """,
            [cve_id],
        ).fetchone()
        # Each synthetic CVE pins one branch of the view; the matrix row says which.
        actual_days = got[0] if exposed else got[2]
        actual_triage = got[1] if exposed else got[3]
        actual_row = got[4] if exposed else got[5]
        check(
            f"view row {row:>2} ({'exposed' if exposed else 'internal'})",
            actual_days == days and actual_triage == triage and actual_row == row and got[6],
            f"expected days={days} triage={triage} row={row}, got {got}",
        )

    no_ssvc = con.execute(
        "SELECT ssvc_known, days_if_exposed, days_if_internal FROM gold.cve_bod2604 "
        "WHERE cve_id = 'CVE-2026-9999'"
    ).fetchone()
    check("missing SSVC -> ssvc_known false, no deadline invented",
          no_ssvc == (False, None, None), f"got {no_ssvc}")
    check("missing SSVC appears in the triage queue",
          con.execute("SELECT count(*) FROM gold.ssvc_gap_triage WHERE cve_id='CVE-2026-9999'"
                      ).fetchone()[0] == 1)
    check("rejected CVEs excluded from Gold",
          con.execute("SELECT count(*) FROM gold.cve_bod2604 WHERE cve_id='CVE-2026-8888'"
                      ).fetchone()[0] == 0)

    # Clock start: the directive starts the timeline at the KEV add date (or asset detection,
    # which we do not have). Row 1 is exposed+KEV+automatable+total = 3 days from 2026-06-10.
    due = con.execute(
        "SELECT clock_start, due_date_if_exposed FROM gold.cve_bod2604 WHERE cve_id='CVE-2026-9001'"
    ).fetchone()
    check("due date = KEV date_added + remediation days",
          str(due[0]) == "2026-06-10" and str(due[1]) == "2026-06-13", f"got {due}")
    no_kev_due = con.execute(
        "SELECT clock_start, due_date_if_exposed FROM gold.cve_bod2604 WHERE cve_id='CVE-2026-9005'"
    ).fetchone()
    check("no KEV entry -> no clock start, no due date",
          no_kev_due == (None, None), f"got {no_kev_due}")

    con.close()
    print()
    if failures:
        print(f"FAILED: {len(failures)} check(s): {', '.join(failures)}")
        return 1
    print("All checks passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
