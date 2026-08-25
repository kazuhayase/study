"""NVD CVE API 2.0 -> bronze.nvd_cve.

The backbone feed: CVE core data, CVSS, CWE, CPE configurations, and -- confirmed against live
responses on 2026-08-20 -- CISA's Vulnrichment SSVC mirrored into metrics.ssvcV203 plus KEV
membership in cisaExploitAdd. So a single NVD sync already supplies three of BOD 26-04's four
variables; the other feeds exist to correct NVD's lag, not to fill a void.
"""

from __future__ import annotations

import json
from datetime import datetime, timedelta, timezone
from typing import Any

import duckdb

from .. import config, http
from ..db import bulk_insert, fetch_run, get_cursor, set_cursor

_TS_FMT = "%Y-%m-%dT%H:%M:%S.000"
_BATCH = 2000


def _page(params: dict[str, Any]) -> dict[str, Any]:
    query = "&".join(f"{k}={v}" for k, v in params.items())
    return http.get_json(f"{config.NVD_API_URL}?{query}", headers=http.nvd_headers())


_BRONZE_COLUMNS = {
    "cve_id": "VARCHAR",
    "raw_json": "VARCHAR",  # cast to the JSON column on insert
    "source_last_modified": "TIMESTAMP",
    "fetch_id": "VARCHAR",
}


def _store(con: duckdb.DuckDBPyConnection, rows: list[tuple], fetch_id: str) -> None:
    """fetched_at is omitted so the column's DEFAULT now() applies."""
    if not rows:
        return
    bulk_insert(
        con,
        "bronze.nvd_cve",
        _BRONZE_COLUMNS,
        (
            {
                "cve_id": cve_id,
                "raw_json": raw,
                "source_last_modified": last_mod,
                "fetch_id": fetch_id,
            }
            for cve_id, raw, last_mod in rows
        ),
    )


def _drain(
    con: duckdb.DuckDBPyConnection,
    base_params: dict[str, Any],
    result: dict[str, Any],
    label: str,
    start_index: int = 0,
    progress_key: str | None = None,
) -> str | None:
    """Page through one query, storing as we go. Returns the max lastModified seen.

    `progress_key`, when given, persists `start_index` to meta.sync_state after every page so a
    run killed by a network error (a full corpus walk takes ~10-30 min and WinError 10054 /
    IncompleteRead do happen mid-walk -- confirmed 2026-08-21) can resume near where it left off
    on the next `init` instead of re-fetching everything. Cleared on a full, uninterrupted
    completion so a deliberate fresh run still starts at 0.
    """
    total = None
    watermark: str | None = None
    batch: list[tuple] = []

    while total is None or start_index < total:
        params = dict(base_params, resultsPerPage=config.NVD_PAGE_SIZE, startIndex=start_index)
        payload = _page(params)
        total = payload["totalResults"]
        items = payload.get("vulnerabilities") or []
        if not items:
            break

        for item in items:
            cve = item.get("cve") or {}
            cve_id = cve.get("id")
            if not cve_id:
                result["rows_skipped"] += 1
                continue
            last_mod = cve.get("lastModified")
            if last_mod and (watermark is None or last_mod > watermark):
                watermark = last_mod
            batch.append((cve_id, json.dumps(cve, separators=(",", ":")), last_mod))

        if len(batch) >= _BATCH:
            _store(con, batch, result["fetch_id"])
            result["rows_ingested"] += len(batch)
            batch = []

        start_index += len(items)
        if progress_key:
            set_cursor(con, progress_key, str(start_index))
        print(f"    {label}: {min(start_index, total):,}/{total:,}")
        if start_index < total:
            http.nvd_sleep()

    _store(con, batch, result["fetch_id"])
    result["rows_ingested"] += len(batch)
    if progress_key:
        con.execute("DELETE FROM meta.sync_state WHERE source = ?", [progress_key])
    return watermark


def fetch_ids(con: duckdb.DuckDBPyConnection, cve_ids: list[str]) -> int:
    """Pull specific CVEs into Bronze. For spot checks and for filling a known gap."""
    with fetch_run(con, "nvd", "fetch") as result:
        for cve_id in cve_ids:
            payload = _page({"cveId": cve_id})
            for item in payload.get("vulnerabilities") or []:
                cve = item.get("cve") or {}
                if not cve.get("id"):
                    result["rows_skipped"] += 1
                    continue
                _store(
                    con,
                    [(cve["id"], json.dumps(cve, separators=(",", ":")), cve.get("lastModified"))],
                    result["fetch_id"],
                )
                result["rows_ingested"] += 1
            http.nvd_sleep()
        result["detail"] = f"{len(cve_ids)} id(s) requested"
        return result["rows_ingested"]


def sync(con: duckdb.DuckDBPyConnection, mode: str = "update", pub_start: str | None = None) -> None:
    """Full load (`init`) or incremental catch-up (`update`).

    Incremental uses lastModStartDate/lastModEndDate, which NVD caps at 120-day spans, so a long
    gap since the last run is walked in chunks rather than failing outright.
    """
    with fetch_run(con, "nvd", mode) as result:
        if mode == "init" and not pub_start:
            # Whole corpus: no date filter at all, just paginate to the end.
            # Rejected CVEs are kept rather than filtered with noRejected -- Silver flags them and
            # Gold excludes them, so the corpus stays complete and the exclusion stays auditable.
            resume_at = get_cursor(con, "nvd_init_progress")
            start_index = int(resume_at) if resume_at else 0
            result["detail"] = f"init full corpus (resuming at {start_index:,})" if start_index \
                else "init full corpus"
            watermark = _drain(
                con, {}, result, "nvd init", start_index=start_index,
                progress_key="nvd_init_progress",
            )
            if watermark:
                set_cursor(con, "nvd", watermark)
            return

        now = datetime.now(timezone.utc)
        cursor = get_cursor(con, "nvd")

        if mode == "init":
            start = datetime.fromisoformat(pub_start).replace(tzinfo=timezone.utc)
            date_param = "pub"
            label = f"init since {pub_start}"
        elif cursor:
            start = datetime.fromisoformat(cursor.replace("Z", "+00:00"))
            if start.tzinfo is None:
                start = start.replace(tzinfo=timezone.utc)
            start -= timedelta(minutes=5)  # small overlap; upserts make this harmless
            date_param = "lastMod"
            label = "update"
        else:
            # No watermark yet: look back a week rather than silently pulling nothing.
            start = now - timedelta(days=7)
            date_param = "lastMod"
            label = "update (no watermark; last 7 days)"

        watermark, windows = _walk_windows(con, start, now, date_param, result)
        result["detail"] = f"{label} in {windows} window(s)"
        if watermark and (cursor is None or watermark > cursor):
            set_cursor(con, "nvd", watermark)


def _walk_windows(
    con: duckdb.DuckDBPyConnection,
    start: datetime,
    end_at: datetime,
    date_param: str,
    result: dict[str, Any],
) -> tuple[str | None, int]:
    """Walk a date range in <=120-day slices.

    NVD caps *every* date range at 120 days -- pubStartDate/pubEndDate just as much as
    lastModStartDate/lastModEndDate -- so a request spanning more than that is rejected outright
    rather than truncated. Chunking here is what lets `init --pub-start 2020-01-01` work at all.
    """
    watermark: str | None = None
    windows = 0
    while start < end_at:
        stop = min(start + timedelta(days=config.NVD_MAX_WINDOW_DAYS - 1), end_at)
        params = {
            f"{date_param}StartDate": start.strftime(_TS_FMT),
            f"{date_param}EndDate": stop.strftime(_TS_FMT),
        }
        got = _drain(con, params, result, f"nvd {start:%Y-%m-%d}..{stop:%Y-%m-%d}")
        if got and (watermark is None or got > watermark):
            watermark = got
        windows += 1
        start = stop
        if start < end_at:
            http.nvd_sleep()
    return watermark, windows
