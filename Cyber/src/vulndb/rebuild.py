"""Rebuild Silver from Bronze.

Always a full rebuild, never an incremental patch. Silver is cheap to recompute from local data
and the guarantee that it cannot drift from Bronze is worth more than the seconds it costs.

Source precedence is expressed by the order the passes run. The authoritative feeds go first
with INSERT OR REPLACE; the NVD pass follows with INSERT OR IGNORE, so its mirrored copies of
KEV and SSVC only ever fill gaps and never overwrite the originals:

    silver.kev   KEV catalog  >  Vulnrichment  >  NVD
    silver.ssvc  Vulnrichment >  NVD

The NVD corpus is scanned exactly once: cve / kev / ssvc rows all come out of that single pass.
Every write goes through db.bulk_insert -- see that function for why executemany is avoided.
"""

from __future__ import annotations

import json

import duckdb

from . import transform
from .db import bulk_insert

_READ_CHUNK = 20000

CVE_COLUMNS = {
    "cve_id": "VARCHAR",
    "published": "TIMESTAMP",
    "last_modified": "TIMESTAMP",
    "vuln_status": "VARCHAR",
    "description_en": "VARCHAR",
    "cvss_v31_base_score": "DOUBLE",
    "cvss_v31_severity": "VARCHAR",
    "cvss_v31_vector": "VARCHAR",
    "cvss_v40_base_score": "DOUBLE",
    "cvss_v40_severity": "VARCHAR",
    "cvss_v40_vector": "VARCHAR",
    "cwe_ids": "VARCHAR[]",
    "source_identifier": "VARCHAR",
    "is_rejected": "BOOLEAN",
}

KEV_COLUMNS = {
    "cve_id": "VARCHAR",
    "date_added": "DATE",
    "due_date": "DATE",
    "known_ransomware_campaign_use": "VARCHAR",
    "vendor_project": "VARCHAR",
    "product": "VARCHAR",
    "vulnerability_name": "VARCHAR",
    "required_action": "VARCHAR",
    "notes": "VARCHAR",
    "source": "VARCHAR",
}

SSVC_COLUMNS = {
    "cve_id": "VARCHAR",
    "exploitation": "VARCHAR",
    "automatable": "VARCHAR",
    "technical_impact": "VARCHAR",
    "ssvc_version": "VARCHAR",
    "role": "VARCHAR",
    "decided_at": "TIMESTAMP",
    "source": "VARCHAR",
}

VENDOR_ADVISORY_COLUMNS = {
    "vendor": "VARCHAR",
    "advisory_id": "VARCHAR",
    "title": "VARCHAR",
    "url": "VARCHAR",
    "published_date": "DATE",
    "severity": "VARCHAR",
    "cve_ids": "VARCHAR[]",
}

_VENDOR_PARSERS = {
    "aws": transform.parse_aws_advisory,
    "microsoft": transform.parse_microsoft_advisory,
    "broadcom": transform.parse_broadcom_advisory,
    "ibm": transform.parse_ibm_advisory,
}


def _iter_bronze(con: duckdb.DuckDBPyConnection, table: str):
    cur = con.execute(f"SELECT raw_json FROM {table}")
    while True:
        rows = cur.fetchmany(_READ_CHUNK)
        if not rows:
            return
        for (raw,) in rows:
            try:
                yield json.loads(raw)
            except (json.JSONDecodeError, TypeError):
                continue


def rebuild_all(con: duckdb.DuckDBPyConnection, verbose: bool = True) -> dict[str, int]:
    for table in (
        "silver.cve", "silver.kev", "silver.ssvc", "silver.epss_current",
        "silver.vendor_advisory",
    ):
        con.execute(f"DELETE FROM {table}")

    counts = {"silver.cve": 0, "silver.cve_skipped": 0}

    # --- Pass 1: KEV catalog (authoritative) --------------------------------
    bulk_insert(
        con, "silver.kev", KEV_COLUMNS,
        (
            transform.parse_kev_entry(entry)
            for entry in _iter_bronze(con, "bronze.kev")
            if entry.get("cveID")
        ),
        mode="REPLACE",
    )

    # --- Pass 2: Vulnrichment (authoritative for SSVC, fallback for KEV) ----
    # Materialised because the records feed two tables and Bronze is read once.
    vr_ssvc: list[dict] = []
    vr_kev: list[dict] = []
    for record in _iter_bronze(con, "bronze.vulnrichment"):
        parsed = transform.parse_vulnrichment_ssvc(record)
        if parsed:
            vr_ssvc.append(parsed)
        parsed_kev = transform.parse_vulnrichment_kev(record)
        if parsed_kev:
            vr_kev.append(parsed_kev)
    bulk_insert(con, "silver.ssvc", SSVC_COLUMNS, vr_ssvc, mode="REPLACE")
    bulk_insert(con, "silver.kev", KEV_COLUMNS, vr_kev, mode="IGNORE")
    del vr_ssvc, vr_kev

    # --- Pass 3: NVD, one scan feeding all three tables ---------------------
    nvd_cve: list[dict] = []
    nvd_kev: list[dict] = []
    nvd_ssvc: list[dict] = []
    for cve in _iter_bronze(con, "bronze.nvd_cve"):
        try:
            nvd_cve.append(transform.parse_nvd_cve(cve))
        except (KeyError, TypeError, ValueError):
            counts["silver.cve_skipped"] += 1
            continue
        kev_row = transform.parse_nvd_kev(cve)
        if kev_row:
            nvd_kev.append(kev_row)
        ssvc_row = transform.parse_nvd_ssvc(cve)
        if ssvc_row:
            nvd_ssvc.append(ssvc_row)

    counts["silver.cve"] = bulk_insert(con, "silver.cve", CVE_COLUMNS, nvd_cve, mode="REPLACE")
    bulk_insert(con, "silver.kev", KEV_COLUMNS, nvd_kev, mode="IGNORE")
    bulk_insert(con, "silver.ssvc", SSVC_COLUMNS, nvd_ssvc, mode="IGNORE")
    del nvd_cve, nvd_kev, nvd_ssvc

    # --- Pass 4: latest EPSS score per CVE (pure SQL; Bronze is already typed)
    con.execute(
        """
        INSERT INTO silver.epss_current (cve_id, epss, percentile, score_date)
        SELECT cve_id, epss, percentile, score_date
        FROM (
            SELECT *, row_number() OVER (PARTITION BY cve_id ORDER BY score_date DESC) AS rn
            FROM bronze.epss
        )
        WHERE rn = 1
        """
    )

    # --- Pass 5: vendor security advisories (AWS, Microsoft, Broadcom, IBM) -------------
    # Independent of the CVE/KEV/SSVC passes above: no precedence to preserve, each vendor's
    # bronze rows map 1:1 to its own silver rows via that vendor's parser.
    vendor_rows: list[dict] = []
    vendor_skipped = 0
    for vendor, raw_json in con.execute(
        "SELECT vendor, raw_json FROM bronze.vendor_advisories"
    ).fetchall():
        parser = _VENDOR_PARSERS.get(vendor)
        if parser is None:
            vendor_skipped += 1
            continue
        try:
            item = json.loads(raw_json)
        except (json.JSONDecodeError, TypeError):
            vendor_skipped += 1
            continue
        parsed = parser(item)
        if parsed is None:
            vendor_skipped += 1
            continue
        vendor_rows.append(parsed)
    counts["silver.vendor_advisory"] = bulk_insert(
        con, "silver.vendor_advisory", VENDOR_ADVISORY_COLUMNS, vendor_rows, mode="REPLACE"
    )
    counts["silver.vendor_advisory_skipped"] = vendor_skipped

    for table in ("silver.kev", "silver.ssvc", "silver.epss_current"):
        counts[table] = con.execute(f"SELECT count(*) FROM {table}").fetchone()[0]

    if verbose:
        for name in ("silver.cve", "silver.cve_skipped", "silver.kev", "silver.ssvc",
                     "silver.epss_current", "silver.vendor_advisory",
                     "silver.vendor_advisory_skipped"):
            print(f"  {name}: {counts[name]:,}")
    return counts
