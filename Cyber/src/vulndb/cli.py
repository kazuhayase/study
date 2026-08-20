"""Command line interface.

Non-interactive throughout so the same entry points serve a terminal and a scheduled CI run.
A failure in one feed is reported and does not abort the others -- a Vulnrichment outage should
not cost you the day's KEV and EPSS updates.
"""

from __future__ import annotations

import argparse
import sys

from . import config, db, rebuild
from .sources import epss, kev, nvd, vulnrichment

SOURCES = {
    "nvd": nvd.sync,
    "kev": kev.sync,
    "epss": epss.sync,
    "vulnrichment": vulnrichment.sync,
}


def _run_sources(con, mode: str, names: list[str], pub_start: str | None = None) -> int:
    failures = 0
    for name in names:
        print(f"[{name}] {mode}")
        try:
            if name == "nvd":
                SOURCES[name](con, mode=mode, pub_start=pub_start)
            else:
                SOURCES[name](con, mode=mode)
        except Exception as exc:  # noqa: BLE001 - logged to meta.fetch_log, other feeds continue
            failures += 1
            print(f"[{name}] FAILED: {type(exc).__name__}: {exc}", file=sys.stderr)
    return failures


def cmd_init(args) -> int:
    con = db.connect()
    print("migrations:")
    db.migrate(con)
    failures = _run_sources(con, "init", args.sources, args.pub_start)
    print("rebuild:")
    rebuild.rebuild_all(con)
    con.close()
    return 1 if failures else 0


def cmd_update(args) -> int:
    con = db.connect()
    db.migrate(con, verbose=False)
    failures = _run_sources(con, "update", args.sources)
    print("rebuild:")
    rebuild.rebuild_all(con)
    con.close()
    return 1 if failures else 0


def cmd_rebuild(args) -> int:
    con = db.connect()
    db.migrate(con, verbose=False)
    rebuild.rebuild_all(con)
    con.close()
    return 0


def cmd_fetch(args) -> int:
    con = db.connect()
    db.migrate(con, verbose=False)
    n = nvd.fetch_ids(con, [c.upper() for c in args.cve_ids])
    print(f"fetched {n} CVE(s) from NVD")
    rebuild.rebuild_all(con)
    con.close()
    return 0 if n else 1


def cmd_status(args) -> int:
    con = db.connect(read_only=True)

    print("== row counts ==")
    for table in (
        "bronze.nvd_cve", "bronze.kev", "bronze.vulnrichment", "bronze.epss",
        "silver.cve", "silver.kev", "silver.ssvc", "silver.epss_current",
    ):
        n = con.execute(f"SELECT count(*) FROM {table}").fetchone()[0]
        print(f"  {table:<24} {n:>10,}")

    print("\n== BOD 26-04 coverage ==")
    row = con.execute(
        """
        SELECT count(*) AS total,
               sum(CASE WHEN ssvc_known THEN 1 ELSE 0 END) AS with_ssvc,
               sum(CASE WHEN in_kev THEN 1 ELSE 0 END) AS in_kev,
               sum(CASE WHEN in_kev AND NOT ssvc_known THEN 1 ELSE 0 END) AS kev_no_ssvc
        FROM gold.cve_bod2604
        """
    ).fetchone()
    total, with_ssvc, in_kev, kev_no_ssvc = row
    if total:
        print(f"  CVEs (excl. rejected)  {total:>10,}")
        print(f"  with SSVC              {with_ssvc:>10,}  ({with_ssvc / total * 100:.1f}%)")
        print(f"  in KEV                 {in_kev:>10,}")
        print(f"  KEV lacking SSVC       {kev_no_ssvc:>10,}  <- assess these first")

    print("\n== SSVC coverage by year (recent) ==")
    for year, tot, _ws, pct, kev_n, _we, _kns in con.execute(
        "SELECT * FROM gold.coverage_stats LIMIT 8"
    ).fetchall():
        print(f"  {year}  {tot:>8,} CVEs   SSVC {pct:>5.1f}%   KEV {kev_n:>4,}")

    print("\n== last fetch per source ==")
    for source, status, rows_n, detail, finished in con.execute(
        """
        SELECT source, status, rows_ingested, detail, finished_at
        FROM (SELECT *, row_number() OVER (PARTITION BY source ORDER BY started_at DESC) rn
              FROM meta.fetch_log)
        WHERE rn = 1 ORDER BY source
        """
    ).fetchall():
        stamp = finished.strftime("%Y-%m-%d %H:%M") if finished else "-"
        print(f"  {source:<14} {status:<8} {rows_n or 0:>8,} rows  {stamp}  {detail or ''}")

    con.close()
    return 0


def cmd_query(args) -> int:
    con = db.connect(read_only=True)
    row = con.execute(
        "SELECT * FROM gold.cve_bod2604 WHERE cve_id = ?", [args.cve_id.upper()]
    ).fetchone()
    if not row:
        print(f"{args.cve_id}: not found")
        con.close()
        return 1
    cols = [d[0] for d in con.description]
    width = max(len(c) for c in cols)
    for col, value in zip(cols, row):
        print(f"  {col:<{width}}  {value}")
    con.close()
    return 0


def cmd_triage(args) -> int:
    """The CVEs CISA has not scored, in the order they should be assessed."""
    con = db.connect(read_only=True)
    rows = con.execute(
        """
        SELECT cve_id, in_kev, round(epss, 5) AS epss, round(epss_percentile, 4) AS pctl,
               cvss_v31_base_score AS cvss, gap
        FROM gold.ssvc_gap_triage LIMIT ?
        """,
        [args.limit],
    ).fetchall()
    print(f"{'CVE':<18} {'KEV':<5} {'EPSS':>9} {'PCTL':>8} {'CVSS':>5}  GAP")
    for cve_id, in_kev, epss_v, pctl, cvss, gap in rows:
        print(
            f"{cve_id:<18} {'yes' if in_kev else '-':<5} "
            f"{epss_v if epss_v is not None else '-':>9} "
            f"{pctl if pctl is not None else '-':>8} "
            f"{cvss if cvss is not None else '-':>5}  {gap}"
        )
    con.close()
    return 0


def cmd_export(args) -> int:
    con = db.connect(read_only=True)
    outdir = config.DATA_DIR / "export"
    outdir.mkdir(parents=True, exist_ok=True)
    for name in ("gold.cve_bod2604", "gold.ssvc_gap_triage", "gold.coverage_stats",
                 "silver.cve", "silver.kev", "silver.ssvc", "silver.epss_current"):
        target = outdir / f"{name.replace('.', '_')}.parquet"
        con.execute(f"COPY (SELECT * FROM {name}) TO '{target}' (FORMAT PARQUET)")
        print(f"  wrote {target}")
    con.close()
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="vulndb", description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)

    all_sources = list(SOURCES)

    p_init = sub.add_parser("init", help="full initial load of every feed")
    p_init.add_argument("--sources", nargs="+", choices=all_sources, default=all_sources)
    p_init.add_argument(
        "--pub-start",
        metavar="YYYY-MM-DD",
        help="limit the NVD load to CVEs published on or after this date (smoke tests)",
    )
    p_init.set_defaults(func=cmd_init)

    p_update = sub.add_parser("update", help="incremental update from the last sync point")
    p_update.add_argument("--sources", nargs="+", choices=all_sources, default=all_sources)
    p_update.set_defaults(func=cmd_update)

    sub.add_parser("rebuild", help="rebuild Silver from Bronze without fetching").set_defaults(
        func=cmd_rebuild
    )
    sub.add_parser("status", help="row counts, coverage and last fetch per source").set_defaults(
        func=cmd_status
    )

    p_fetch = sub.add_parser("fetch", help="pull specific CVEs from NVD into the database")
    p_fetch.add_argument("cve_ids", nargs="+", metavar="CVE-ID")
    p_fetch.set_defaults(func=cmd_fetch)

    p_query = sub.add_parser("query", help="show the BOD 26-04 evaluation for one CVE")
    p_query.add_argument("cve_id")
    p_query.set_defaults(func=cmd_query)

    p_triage = sub.add_parser("triage", help="CVEs lacking SSVC, ranked for manual assessment")
    p_triage.add_argument("--limit", type=int, default=25)
    p_triage.set_defaults(func=cmd_triage)

    sub.add_parser("export", help="write Gold and Silver tables to Parquet").set_defaults(
        func=cmd_export
    )

    args = parser.parse_args(argv)
    return args.func(args)
