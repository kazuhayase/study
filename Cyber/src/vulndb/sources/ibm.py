"""IBM PSIRT security bulletin search API -> bronze.vendor_advisories.

There is no full-listing or date-range endpoint (confirmed 2026-08-21 by inspecting the site's
own network traffic while driving its UI) -- search is the only public, unauthenticated access
point, and it requires a query term. Coverage is therefore bounded by
config.IBM_PRODUCT_SEARCH_TERMS: bulletins for products not in that list are not collected.

`limit`/`offset` query params are accepted but ignored server-side -- each term always returns
up to 2,000 results regardless (some over 20MB), so on a flaky connection a single `init` often
can't get through the whole list in one run (confirmed repeatedly, 2026-08-25). Two things make
that survivable:
  - Each term is written to bronze immediately after it succeeds, not batched to the end -- a
    crash partway through never loses an already-fetched term's rows.
  - `init` records a per-term completion marker in meta.sync_state and skips terms already
    marked done, so re-running `init` after a failure only retries what's still missing instead
    of refetching everything from term 1. `update` ignores these markers and always refetches
    every term -- IBM has no incremental/date-filtered endpoint to do better, and daily runs
    should still pick up new bulletins for already-covered terms.
"""

from __future__ import annotations

import json
import urllib.parse

import duckdb

from .. import config, http, transform
from ..db import bulk_insert, fetch_run, get_cursor, set_cursor

_BRONZE_COLUMNS = {
    "vendor": "VARCHAR",
    "advisory_id": "VARCHAR",
    "raw_json": "VARCHAR",  # cast to the JSON column on insert
    "fetch_id": "VARCHAR",
}


def _term_marker(term: str) -> str:
    return f"ibm_term_done:{term}"


def sync(con: duckdb.DuckDBPyConnection, mode: str = "update") -> None:
    with fetch_run(con, "ibm", mode) as result:
        fetched, already_done = 0, 0
        for term in config.IBM_PRODUCT_SEARCH_TERMS:
            if mode == "init" and get_cursor(con, _term_marker(term)):
                already_done += 1
                continue

            url = f"{config.IBM_SEARCH_API_URL}?{urllib.parse.urlencode({'q': term})}"
            try:
                resp = http.get_json(url)
            except http.FetchError as exc:
                print(f"    ibm: {term!r} FAILED, skipping: {exc}")
                result["rows_skipped"] += 1
                continue

            rows = []
            for item in resp.get("results") or []:
                parsed = transform.parse_ibm_advisory(item)
                if parsed is None:
                    result["rows_skipped"] += 1
                    continue
                rows.append(
                    {
                        "vendor": "ibm",
                        "advisory_id": parsed["advisory_id"],
                        "raw_json": json.dumps(item, separators=(",", ":")),
                        "fetch_id": result["fetch_id"],
                    }
                )
            result["rows_ingested"] += bulk_insert(
                con, "bronze.vendor_advisories", _BRONZE_COLUMNS, rows
            )
            if mode == "init":
                set_cursor(con, _term_marker(term), "done")
            fetched += 1
            print(f"    ibm: {term!r} -> {resp.get('items_count', 0)} result(s)")

        result["detail"] = (
            f"{fetched} term(s) fetched, {already_done} already done, "
            f"{len(config.IBM_PRODUCT_SEARCH_TERMS)} total"
        )
