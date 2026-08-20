"""CISA KEV catalog -> bronze.kev.

Authoritative for BOD 26-04's "In the KEV?" variable, and the only feed carrying
knownRansomwareCampaignUse. Small (~1,700 entries, 1.6 MB), so it is replaced wholesale each run.
"""

from __future__ import annotations

import json

import duckdb

from .. import config, http
from ..db import bulk_insert, fetch_run, set_cursor


def sync(con: duckdb.DuckDBPyConnection, mode: str = "update") -> None:
    with fetch_run(con, "kev", mode) as result:
        catalog = http.get_json(config.KEV_URL)
        version = catalog.get("catalogVersion")
        entries = catalog.get("vulnerabilities") or []

        rows = []
        for entry in entries:
            cve_id = entry.get("cveID")
            if not cve_id:
                result["rows_skipped"] += 1
                continue
            rows.append(
                {
                    "cve_id": cve_id,
                    "raw_json": json.dumps(entry, separators=(",", ":")),
                    "catalog_version": version,
                    "fetch_id": result["fetch_id"],
                }
            )

        # Entries are only ever added to the catalog, but a removal upstream must not linger here.
        con.execute("DELETE FROM bronze.kev")
        result["rows_ingested"] = bulk_insert(
            con,
            "bronze.kev",
            {
                "cve_id": "VARCHAR",
                "raw_json": "VARCHAR",
                "catalog_version": "VARCHAR",
                "fetch_id": "VARCHAR",
            },
            rows,
        )
        result["detail"] = f"catalogVersion={version}, count={catalog.get('count')}"
        if version:
            set_cursor(con, "kev", version)
