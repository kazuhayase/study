"""MSRC (Microsoft Security Response Center) CVRF API -> bronze.vendor_advisories.

/updates lists every monthly release since 1999 (~48 KB, one request). Each release's own CVRF
document is fetched separately and its Vulnerability[] entries become one bronze row per CVE --
MSRC's natural unit is a single vulnerability, unlike AWS/Broadcom bulletins which bundle several.

`init` only walks the last config.MSRC_INIT_LOOKBACK_MONTHS: older CVEs are already covered by
NVD, and pulling all ~300 monthly documents (each up to a few MB) has no payoff here. `update`
walks releases whose CurrentReleaseDate is newer than the stored cursor -- MSRC does revise past
months' documents (score corrections etc.), which CurrentReleaseDate captures.
"""

from __future__ import annotations

import json
from datetime import datetime, timedelta, timezone

import duckdb

from .. import config, http, transform
from ..db import bulk_insert, fetch_run, get_cursor, set_cursor

_BRONZE_COLUMNS = {
    "vendor": "VARCHAR",
    "advisory_id": "VARCHAR",
    "raw_json": "VARCHAR",  # cast to the JSON column on insert
    "fetch_id": "VARCHAR",
}

# The API serves CVRF XML by default; without this header it 200s with an XML body that
# json.loads then rejects with "Expecting value: line 1 column 1" -- confirmed 2026-08-21.
_JSON_ACCEPT = {"Accept": "application/json"}


def _releases_to_sync(mode: str, cursor: str | None) -> list[dict]:
    updates = http.get_json(config.MSRC_CVRF_UPDATES_URL, headers=_JSON_ACCEPT)["value"]
    if mode == "init" or not cursor:
        cutoff = datetime.now(timezone.utc) - timedelta(days=30 * config.MSRC_INIT_LOOKBACK_MONTHS)
        cutoff_str = cutoff.strftime("%Y-%m-%d")
    else:
        cutoff_str = cursor
    return [u for u in updates if (u.get("CurrentReleaseDate") or "") > cutoff_str]


def sync(con: duckdb.DuckDBPyConnection, mode: str = "update") -> None:
    with fetch_run(con, "microsoft", mode) as result:
        cursor = get_cursor(con, "microsoft")
        releases = _releases_to_sync(mode, cursor)

        rows = []
        max_release_date = cursor or ""
        for i, release in enumerate(releases, 1):
            release_id = release["ID"]
            max_release_date = max(max_release_date, release.get("CurrentReleaseDate") or "")
            try:
                doc = http.get_json(
                    config.MSRC_CVRF_DOC_URL.format(release_id=release_id), headers=_JSON_ACCEPT
                )
            except http.FetchError:
                result["rows_skipped"] += 1
                continue

            initial_release_date = (doc.get("DocumentTracking") or {}).get("InitialReleaseDate")
            for vuln in doc.get("Vulnerability") or []:
                item = dict(vuln)
                item["_document_id"] = release_id
                item["_initial_release_date"] = initial_release_date

                parsed = transform.parse_microsoft_advisory(item)
                if parsed is None:
                    result["rows_skipped"] += 1
                    continue
                rows.append(
                    {
                        "vendor": "microsoft",
                        "advisory_id": parsed["advisory_id"],
                        "raw_json": json.dumps(item, separators=(",", ":")),
                        "fetch_id": result["fetch_id"],
                    }
                )
            if i % 10 == 0:
                print(f"    microsoft: {i}/{len(releases)} release(s)")

        result["rows_ingested"] = bulk_insert(
            con, "bronze.vendor_advisories", _BRONZE_COLUMNS, rows
        )
        result["detail"] = f"{len(releases)} release(s), {len(rows)} vulnerabilit(y/ies)"
        if max_release_date:
            set_cursor(con, "microsoft", max_release_date)
