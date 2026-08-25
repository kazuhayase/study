"""Broadcom security advisories API -> bronze.vendor_advisories.

segment="" spans every Broadcom division (VMware, Symantec, CA mainframe) in one feed, sorted
newest-first by notificationId -- confirmed 2026-08-21 against the live API, no per-division
enumeration needed. `update` mode stops paging as soon as it reaches a notificationId already
seen on a previous run.
"""

from __future__ import annotations

import json

import duckdb

from .. import config, http, transform
from ..db import bulk_insert, fetch_run, get_cursor, set_cursor

_BRONZE_COLUMNS = {
    "vendor": "VARCHAR",
    "advisory_id": "VARCHAR",
    "raw_json": "VARCHAR",  # cast to the JSON column on insert
    "fetch_id": "VARCHAR",
}


def _fetch_page(page_number: int) -> list[dict]:
    payload = {
        "pageNumber": page_number,
        "pageSize": config.BROADCOM_PAGE_SIZE,
        "searchVal": "",
        "segment": "",
        "sortInfo": {"column": "", "order": ""},
    }
    resp = http.post_json(config.BROADCOM_ADVISORY_API_URL, payload)
    return (resp.get("data") or {}).get("list") or []


def sync(con: duckdb.DuckDBPyConnection, mode: str = "update") -> None:
    with fetch_run(con, "broadcom", mode) as result:
        cursor = int(get_cursor(con, "broadcom") or 0) if mode != "init" else 0

        rows = []
        max_notification_id = cursor
        page = 0
        stop = False
        while not stop:
            items = _fetch_page(page)
            if not items:
                break
            for item in items:
                notification_id = item.get("notificationId") or 0
                if mode != "init" and notification_id <= cursor:
                    stop = True
                    break
                max_notification_id = max(max_notification_id, notification_id)

                parsed = transform.parse_broadcom_advisory(item)
                if parsed is None:
                    result["rows_skipped"] += 1
                    continue
                rows.append(
                    {
                        "vendor": "broadcom",
                        "advisory_id": parsed["advisory_id"],
                        "raw_json": json.dumps(item, separators=(",", ":")),
                        "fetch_id": result["fetch_id"],
                    }
                )
            if len(items) < config.BROADCOM_PAGE_SIZE:
                break
            page += 1
            if page % 10 == 0:
                print(f"    broadcom: page {page}, {len(rows)} row(s) so far")

        result["rows_ingested"] = bulk_insert(
            con, "bronze.vendor_advisories", _BRONZE_COLUMNS, rows
        )
        result["detail"] = f"{page + 1} page(s)"
        if max_notification_id > cursor or mode == "init":
            set_cursor(con, "broadcom", str(max_notification_id))
