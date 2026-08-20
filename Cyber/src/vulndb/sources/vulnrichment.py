"""CISA Vulnrichment -> bronze.vulnrichment.

The origin of the SSVC decision points that answer two of BOD 26-04's four variables. NVD mirrors
this data but can lag it, so Vulnrichment overrides NVD in Silver.

Initial load pulls the branch tarball (~85 MB, versus ~331 MB for a git clone). Daily updates ask
the GitHub compare API which files changed since the last synced commit, which is normally a few
dozen -- so the steady state costs a handful of small requests, not a re-download.

Only the CISA-ADP container is retained. The rest of each record is CNA data that NVD already
supplies in full, and keeping all of it would add gigabytes that nothing reads.
"""

from __future__ import annotations

import json
import os
import re
import tarfile
from typing import Any, Iterator

import duckdb

from .. import config, http
from ..db import bulk_insert, fetch_run, get_cursor, set_cursor

CVE_FILE_RE = re.compile(r"CVE-\d{4}-\d+\.json$")

# GitHub's compare API caps the `files` array at 300 entries per response. A response holding
# exactly that many is indistinguishable from a truncated one, so it cannot be trusted as a
# complete diff -- acting on it would advance the cursor past changes we never fetched, losing
# them permanently. Treat a full page as "unknown" and reload the tarball instead.
COMPARE_FILE_PAGE_LIMIT = 300

# Below this, per-file fetches win; above it, the 85 MB tarball is faster. Measured 2026-08-21:
# 300 sequential file fetches took ~4 minutes against ~2.5 minutes for a full tarball reload.
TARBALL_BREAKEVEN_FILES = 150


def _gh_headers() -> dict[str, str]:
    token = os.environ.get("GITHUB_TOKEN")
    headers = {"Accept": "application/vnd.github+json"}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    return headers


def _head_sha() -> str:
    url = f"{config.GITHUB_API}/repos/{config.VULNRICHMENT_REPO}/commits/{config.VULNRICHMENT_BRANCH}"
    return http.get_json(url, headers=_gh_headers())["sha"]


def _cisa_adp(record: dict[str, Any]) -> dict[str, Any] | None:
    """Return the CISA-ADP container if it carries anything we consume."""
    for adp in (record.get("containers") or {}).get("adp") or []:
        if (adp.get("providerMetadata") or {}).get("shortName") != "CISA-ADP":
            continue
        types = {
            (m.get("other") or {}).get("type")
            for m in adp.get("metrics") or []
        }
        if types & {"ssvc", "kev"}:
            return adp
    return None


def _rows_from_tarball(path, result: dict[str, Any]) -> Iterator[tuple]:
    with tarfile.open(path, "r:gz") as tar:
        for member in tar:
            if not member.isfile() or not CVE_FILE_RE.search(member.name):
                continue
            try:
                fh = tar.extractfile(member)
                if fh is None:
                    continue
                record = json.load(fh)
            except (json.JSONDecodeError, OSError, tarfile.TarError):
                result["rows_skipped"] += 1
                continue
            yield from _row_for(record, result)


def _row_for(record: dict[str, Any], result: dict[str, Any]) -> Iterator[tuple]:
    cve_id = (record.get("cveMetadata") or {}).get("cveId")
    adp = _cisa_adp(record)
    if not cve_id or adp is None:
        return
    payload = {"cveMetadata": {"cveId": cve_id}, "containers": {"adp": [adp]}}
    yield (cve_id, json.dumps(payload, separators=(",", ":")))


_BRONZE_COLUMNS = {
    "cve_id": "VARCHAR",
    "raw_json": "VARCHAR",  # cast to the JSON column on insert
    "commit_sha": "VARCHAR",
    "fetch_id": "VARCHAR",
}


def _store(con: duckdb.DuckDBPyConnection, rows: list[tuple], sha: str, fetch_id: str) -> None:
    if not rows:
        return
    bulk_insert(
        con,
        "bronze.vulnrichment",
        _BRONZE_COLUMNS,
        (
            {"cve_id": cve_id, "raw_json": raw, "commit_sha": sha, "fetch_id": fetch_id}
            for cve_id, raw in rows
        ),
    )


def _full_load(con: duckdb.DuckDBPyConnection, sha: str, result: dict[str, Any]) -> None:
    path = http.download(
        config.VULNRICHMENT_TARBALL_URL, config.DATA_DIR / "vulnrichment.tar.gz"
    )
    batch: list[tuple] = []
    for row in _rows_from_tarball(path, result):
        batch.append(row)
        if len(batch) >= 5000:
            _store(con, batch, sha, result["fetch_id"])
            result["rows_ingested"] += len(batch)
            print(f"    vulnrichment: {result['rows_ingested']:,} enriched records")
            batch = []
    _store(con, batch, sha, result["fetch_id"])
    result["rows_ingested"] += len(batch)


def _changed_files(base: str, head: str) -> list[str] | None:
    """Filenames touched between two commits.

    Returns None whenever the diff cannot be trusted or enumerated, which the caller treats as
    "reload the tarball" -- a slow correct answer beats a fast wrong one.
    """
    url = (
        f"{config.GITHUB_API}/repos/{config.VULNRICHMENT_REPO}/compare/{base}...{head}"
        f"?per_page={COMPARE_FILE_PAGE_LIMIT}"
    )
    try:
        payload = http.get_json(url, headers=_gh_headers())
    except http.FetchError:
        # Most often a 404: the stored base commit no longer exists because history was
        # rewritten or the branch was pruned.
        return None
    if payload.get("status") == "diverged":
        # History was rewritten upstream; a diff from our old base is meaningless.
        return None
    files = payload.get("files") or []
    if len(files) >= COMPARE_FILE_PAGE_LIMIT:
        # Possibly truncated -- see COMPARE_FILE_PAGE_LIMIT.
        return None
    return [f["filename"] for f in files if f.get("status") != "removed"
            and CVE_FILE_RE.search(f.get("filename", ""))]


def sync(con: duckdb.DuckDBPyConnection, mode: str = "update") -> None:
    with fetch_run(con, "vulnrichment", mode) as result:
        head = _head_sha()
        cursor = get_cursor(con, "vulnrichment")

        if mode == "init" or not cursor:
            result["detail"] = f"tarball @ {head[:8]}"
            _full_load(con, head, result)
            set_cursor(con, "vulnrichment", head)
            return

        if cursor == head:
            result["detail"] = f"already at {head[:8]}"
            return

        changed = _changed_files(cursor, head)
        if changed is None:
            result["detail"] = f"range {cursor[:8]}..{head[:8]} too large; full tarball reload"
            _full_load(con, head, result)
            set_cursor(con, "vulnrichment", head)
            return

        # Files are fetched one at a time over the network. Past a few hundred that is slower
        # than simply re-reading the 85 MB tarball, so hand off rather than grinding through.
        if len(changed) > TARBALL_BREAKEVEN_FILES:
            result["detail"] = (
                f"{cursor[:8]}..{head[:8]}, {len(changed)} file(s) changed; tarball is cheaper"
            )
            print(f"    vulnrichment: {len(changed):,} changed files -> reloading tarball")
            _full_load(con, head, result)
            set_cursor(con, "vulnrichment", head)
            return

        base_raw = f"https://raw.githubusercontent.com/{config.VULNRICHMENT_REPO}/{head}/"
        batch: list[tuple] = []
        for i, filename in enumerate(changed, 1):
            try:
                record = json.loads(http.get_bytes(base_raw + filename))
            except (http.FetchError, json.JSONDecodeError):
                result["rows_skipped"] += 1
                continue
            batch.extend(_row_for(record, result))
            if i % 50 == 0:
                print(f"    vulnrichment: {i:,}/{len(changed):,} changed files")
        _store(con, batch, head, result["fetch_id"])
        result["rows_ingested"] = len(batch)
        result["detail"] = f"{cursor[:8]}..{head[:8]}, {len(changed)} file(s) changed"
        set_cursor(con, "vulnrichment", head)
