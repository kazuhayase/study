"""AWS security bulletins RSS -> bronze.vendor_advisories.

The feed is small (recent bulletins only, no historical archive), so every run refetches it
whole and upserts -- same "replace wholesale" shape as kev.py. There is no incremental mode:
`mode` is accepted for symmetry with the other sources but does not change behaviour.
"""

from __future__ import annotations

import json
import xml.etree.ElementTree as ET

import duckdb

from .. import config, http, transform
from ..db import bulk_insert, fetch_run

_BRONZE_COLUMNS = {
    "vendor": "VARCHAR",
    "advisory_id": "VARCHAR",
    "raw_json": "VARCHAR",  # cast to the JSON column on insert
    "fetch_id": "VARCHAR",
}


def _parse_items(raw_xml: bytes) -> list[dict[str, str]]:
    root = ET.fromstring(raw_xml)
    items = []
    for item in root.iter("item"):
        items.append(
            {
                "title": (item.findtext("title") or "").strip(),
                "description": (item.findtext("description") or "").strip(),
                "link": (item.findtext("link") or "").strip(),
                "pubDate": (item.findtext("pubDate") or "").strip(),
            }
        )
    return items


def sync(con: duckdb.DuckDBPyConnection, mode: str = "update") -> None:
    with fetch_run(con, "aws", mode) as result:
        items = _parse_items(http.get_bytes(config.AWS_BULLETINS_RSS_URL))

        rows = []
        for item in items:
            parsed = transform.parse_aws_advisory(item)
            if parsed is None:
                result["rows_skipped"] += 1
                continue
            rows.append(
                {
                    "vendor": "aws",
                    "advisory_id": parsed["advisory_id"],
                    "raw_json": json.dumps(item, separators=(",", ":")),
                    "fetch_id": result["fetch_id"],
                }
            )

        result["rows_ingested"] = bulk_insert(
            con, "bronze.vendor_advisories", _BRONZE_COLUMNS, rows
        )
        result["detail"] = f"{len(items)} item(s) in feed"
