"""FIRST EPSS daily scores -> bronze.epss.

Not one of BOD 26-04's four variables. EPSS earns its place by ordering the CVEs that CISA has
not scored: it estimates probability of exploitation in the next 30 days, which is the question
an analyst is implicitly answering when deciding whether an un-triaged CVE can wait.

The full corpus (~362k rows, ~2.5 MB gzipped) is published daily just after 13:30 UTC.
"""

from __future__ import annotations

from datetime import date

import duckdb

from .. import config, http
from ..db import fetch_run, get_cursor, set_cursor


def _parse_header(line: str) -> tuple[str | None, date | None]:
    """The CSV opens with e.g. '#model_version:v2026.06.15,score_date:2026-08-19T12:03:07Z'."""
    model_version = score_date = None
    for part in line.lstrip("#").strip().split(","):
        key, _, value = part.partition(":")
        if key == "model_version":
            model_version = value
        elif key == "score_date":
            score_date = date.fromisoformat(value.split("T")[0])
    return model_version, score_date


def sync(con: duckdb.DuckDBPyConnection, mode: str = "update", force: bool = False) -> None:
    with fetch_run(con, "epss", mode) as result:
        path = http.download(config.EPSS_CSV_URL, config.DATA_DIR / "epss_scores-current.csv.gz")

        with http.open_maybe_gzip(path) as fh:
            model_version, score_date = _parse_header(fh.readline())
        if score_date is None:
            score_date = date.today()

        if not force and get_cursor(con, "epss") == score_date.isoformat():
            result["detail"] = f"score_date={score_date} already ingested; skipped"
            return

        # DuckDB reads the gzipped CSV itself. Handing it the file rather than looping in Python
        # takes this from minutes to well under a second for the full ~362k-row corpus.
        # skip=1 steps over the leading '#model_version:...' comment so header=true sees the
        # real column names.
        con.execute(
            """
            INSERT OR REPLACE INTO bronze.epss
                (cve_id, score_date, epss, percentile, model_version, fetched_at, fetch_id)
            SELECT cve, CAST($score_date AS DATE), epss, percentile,
                   $model_version, now(), $fetch_id
            FROM read_csv($path, skip=1, header=true,
                          columns={'cve': 'VARCHAR', 'epss': 'DOUBLE', 'percentile': 'DOUBLE'})
            """,
            {
                "score_date": score_date.isoformat(),
                "model_version": model_version,
                "fetch_id": result["fetch_id"],
                "path": str(path),
            },
        )
        result["rows_ingested"] = con.execute(
            "SELECT count(*) FROM bronze.epss WHERE score_date = ?", [score_date]
        ).fetchone()[0]
        result["detail"] = f"score_date={score_date}, model={model_version}"
        set_cursor(con, "epss", score_date.isoformat())
