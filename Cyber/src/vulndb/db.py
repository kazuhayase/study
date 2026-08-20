"""DuckDB connection, migration runner, and fetch provenance helpers."""

from __future__ import annotations

import hashlib
import json
import os
import tempfile
import uuid
from contextlib import contextmanager
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable

import duckdb

from . import config


def bulk_insert(
    con: duckdb.DuckDBPyConnection,
    table: str,
    columns: dict[str, str],
    rows: Iterable[dict[str, Any]],
    mode: str = "REPLACE",
) -> int:
    """Insert dicts into `table` via a temporary JSONL file.

    DuckDB's executemany binds one row at a time and manages ~1,800 rows/s, which turns a
    rebuild of the 173k-row SSVC table into minutes. Staging through JSONL and letting DuckDB
    read the file itself measured 0.38s for the same data -- roughly 500x -- and JSON Lines
    handles quoting, newlines and NULLs correctly without any escaping of our own.

    `columns` maps column name to DuckDB type and defines both the read schema and the insert
    order. `mode` is REPLACE (overwrite on key conflict) or IGNORE (keep the existing row).
    """
    fd, tmp_path = tempfile.mkstemp(suffix=".jsonl", dir=str(config.DATA_DIR))
    written = 0
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as fh:
            for row in rows:
                fh.write(json.dumps({c: row.get(c) for c in columns}, default=str))
                fh.write("\n")
                written += 1
        if written == 0:
            return 0
        col_list = ", ".join(columns)
        schema = ", ".join(f"'{name}': '{dtype}'" for name, dtype in columns.items())
        con.execute(
            f"INSERT OR {mode} INTO {table} ({col_list}) "
            f"SELECT {col_list} FROM read_json(?, columns={{{schema}}})",
            [tmp_path],
        )
        return written
    finally:
        Path(tmp_path).unlink(missing_ok=True)


def connect(path: Path | None = None, read_only: bool = False) -> duckdb.DuckDBPyConnection:
    config.ensure_dirs()
    return duckdb.connect(str(path or config.DB_PATH), read_only=read_only)


def migrate(con: duckdb.DuckDBPyConnection, verbose: bool = True) -> list[str]:
    """Apply pending migrations in filename order. Returns the files applied.

    A file whose checksum changed is re-applied. That is what makes correcting the directive's
    lookup table a one-file edit: 005 is DELETE + INSERT, so editing it and running any command
    reseeds it. The same is true of 004, whose views are CREATE OR REPLACE.

    It does NOT extend to structural changes: 002 and 003 use CREATE TABLE IF NOT EXISTS, which
    is a no-op against an existing table. Adding or altering a column needs a new numbered
    migration file with explicit ALTER statements.
    """
    # Bootstrap the ledger itself. 001 declares these too, identically and idempotently;
    # doing it here first means the very first run can already record what it applied.
    con.execute("CREATE SCHEMA IF NOT EXISTS meta")
    con.execute(
        """
        CREATE TABLE IF NOT EXISTS meta.schema_migrations (
            filename VARCHAR NOT NULL PRIMARY KEY,
            checksum VARCHAR NOT NULL,
            applied_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
        )
        """
    )

    applied: list[str] = []
    for sql_file in sorted(config.MIGRATIONS_DIR.glob("*.sql")):
        body = sql_file.read_text(encoding="utf-8")
        checksum = hashlib.sha256(body.encode("utf-8")).hexdigest()

        row = con.execute(
            "SELECT checksum FROM meta.schema_migrations WHERE filename = ?", [sql_file.name]
        ).fetchone()
        if row and row[0] == checksum:
            continue

        if verbose:
            print(f"  {'re-applying (changed)' if row else 'applying'} {sql_file.name}")
        con.execute(body)
        con.execute("DELETE FROM meta.schema_migrations WHERE filename = ?", [sql_file.name])
        con.execute(
            "INSERT INTO meta.schema_migrations (filename, checksum) VALUES (?, ?)",
            [sql_file.name, checksum],
        )
        applied.append(sql_file.name)
    return applied


@contextmanager
def fetch_run(con: duckdb.DuckDBPyConnection, source: str, mode: str):
    """Record one fetch attempt in meta.fetch_log, whatever the outcome.

    Yields a mutable dict the caller fills in (rows_ingested, rows_skipped, detail). A raised
    exception is logged as 'failed' and re-raised -- the log is never lost to the traceback.
    """
    fetch_id = str(uuid.uuid4())
    started = datetime.now(timezone.utc)
    result = {"fetch_id": fetch_id, "rows_ingested": 0, "rows_skipped": 0, "detail": None}
    try:
        yield result
    except Exception as exc:
        con.execute(
            """
            INSERT INTO meta.fetch_log (fetch_id, source, mode, status, rows_ingested,
                                        rows_skipped, detail, error_message, started_at, finished_at)
            VALUES (?, ?, ?, 'failed', ?, ?, ?, ?, ?, ?)
            """,
            [fetch_id, source, mode, result["rows_ingested"], result["rows_skipped"],
             result["detail"], f"{type(exc).__name__}: {exc}"[:2000], started,
             datetime.now(timezone.utc)],
        )
        raise
    status = "partial" if result["rows_skipped"] else "success"
    con.execute(
        """
        INSERT INTO meta.fetch_log (fetch_id, source, mode, status, rows_ingested,
                                    rows_skipped, detail, started_at, finished_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        [fetch_id, source, mode, status, result["rows_ingested"], result["rows_skipped"],
         result["detail"], started, datetime.now(timezone.utc)],
    )


def get_cursor(con: duckdb.DuckDBPyConnection, source: str) -> str | None:
    row = con.execute("SELECT cursor FROM meta.sync_state WHERE source = ?", [source]).fetchone()
    return row[0] if row else None


def set_cursor(con: duckdb.DuckDBPyConnection, source: str, cursor: str) -> None:
    con.execute("DELETE FROM meta.sync_state WHERE source = ?", [source])
    con.execute(
        "INSERT INTO meta.sync_state (source, cursor, updated_at) VALUES (?, ?, ?)",
        [source, cursor, datetime.now(timezone.utc)],
    )
