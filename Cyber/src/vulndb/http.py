"""HTTP helpers: stdlib only, with the timeout/retry/rate-limit behaviour these feeds need.

The repo had no retry convention to inherit -- existing callers use bare `requests.get` with no
timeout -- so it is established here. NVD in particular returns 403/503 under load rather than
429, and retrying those is the difference between a full load completing and dying at page 140.
"""

from __future__ import annotations

import gzip
import http.client
import json
import shutil
import time
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any

from . import config

# NVD's documented ceilings are 5 requests / 30s anonymous and 50 / 30s with a key. Pacing at
# 6.0s / 0.7s stays under both with margin; NVD explicitly asks clients to sleep between requests.
NVD_SLEEP_WITH_KEY = 0.7
NVD_SLEEP_NO_KEY = 6.0

RETRY_STATUS = {403, 429, 500, 502, 503, 504}
MAX_ATTEMPTS = 5


class FetchError(RuntimeError):
    """A request that failed after exhausting retries."""


def _request(
    url: str,
    headers: dict[str, str] | None = None,
    data: bytes | None = None,
) -> urllib.request.Request:
    hdrs = {"User-Agent": config.USER_AGENT}
    if headers:
        hdrs.update(headers)
    return urllib.request.Request(url, headers=hdrs, data=data)


def _fetch(
    url: str, headers: dict[str, str] | None = None, data: bytes | None = None
) -> bytes:
    """Shared GET/POST retry loop with exponential backoff. `data` present -> POST."""
    last_error: Exception | None = None
    for attempt in range(MAX_ATTEMPTS):
        try:
            with urllib.request.urlopen(
                _request(url, headers, data), timeout=config.HTTP_TIMEOUT
            ) as resp:
                return resp.read()
        except urllib.error.HTTPError as exc:
            last_error = exc
            if exc.code not in RETRY_STATUS:
                raise FetchError(f"{url} -> HTTP {exc.code} {exc.reason}") from exc
        except (
            urllib.error.URLError,
            TimeoutError,
            ConnectionError,
            http.client.HTTPException,  # e.g. IncompleteRead when the server drops mid-response
        ) as exc:
            last_error = exc
        if attempt < MAX_ATTEMPTS - 1:
            backoff = 2.0 * (2**attempt)  # 2, 4, 8, 16 seconds
            print(f"    retry {attempt + 1}/{MAX_ATTEMPTS - 1} in {backoff:.0f}s ({last_error})")
            time.sleep(backoff)
    raise FetchError(f"{url} failed after {MAX_ATTEMPTS} attempts: {last_error}")


def get_bytes(url: str, headers: dict[str, str] | None = None) -> bytes:
    """GET with exponential backoff. Raises FetchError once retries are exhausted."""
    return _fetch(url, headers)


def _fetch_json(
    url: str, headers: dict[str, str] | None = None, data: bytes | None = None
) -> Any:
    """`_fetch` plus JSON parsing, with parsing inside the retry loop.

    A dropped connection does not always surface as IncompleteRead -- a response cut off right
    at a chunk boundary can make `resp.read()` return successfully with a truncated body, which
    `json.loads` then rejects with JSONDecodeError (confirmed 2026-08-25, mid-response cutoff on
    a ~7MB IBM payload). That error happened outside `_fetch`'s retry loop, so it aborted the
    whole sync instead of retrying like every other transient failure here.
    """
    last_error: Exception | None = None
    for attempt in range(MAX_ATTEMPTS):
        raw = _fetch(url, headers, data)
        try:
            return json.loads(raw)
        except json.JSONDecodeError as exc:
            last_error = exc
            if attempt < MAX_ATTEMPTS - 1:
                backoff = 2.0 * (2**attempt)
                print(
                    f"    retry {attempt + 1}/{MAX_ATTEMPTS - 1} in {backoff:.0f}s "
                    f"(truncated JSON: {exc})"
                )
                time.sleep(backoff)
    raise FetchError(f"{url} returned malformed JSON after {MAX_ATTEMPTS} attempts: {last_error}")


def get_json(url: str, headers: dict[str, str] | None = None) -> Any:
    return _fetch_json(url, headers)


def post_json(url: str, payload: Any, headers: dict[str, str] | None = None) -> Any:
    """POST a JSON body and parse a JSON response, with the same retry/backoff as GET."""
    hdrs = {"Content-Type": "application/json", "Accept": "application/json"}
    if headers:
        hdrs.update(headers)
    data = json.dumps(payload).encode("utf-8")
    return _fetch_json(url, hdrs, data)


def download(url: str, dest: Path, headers: dict[str, str] | None = None) -> Path:
    """Stream a URL to disk. Used for payloads too large to hold in memory comfortably."""
    dest.parent.mkdir(parents=True, exist_ok=True)
    tmp = dest.with_suffix(dest.suffix + ".part")
    last_error: Exception | None = None
    for attempt in range(MAX_ATTEMPTS):
        try:
            with urllib.request.urlopen(
                _request(url, headers), timeout=config.HTTP_TIMEOUT
            ) as resp, tmp.open("wb") as fh:
                shutil.copyfileobj(resp, fh, length=1 << 20)
            tmp.replace(dest)  # atomic: a partial download never masquerades as complete
            return dest
        except Exception as exc:  # noqa: BLE001 - retried below, re-raised as FetchError
            last_error = exc
            tmp.unlink(missing_ok=True)
            if attempt < MAX_ATTEMPTS - 1:
                time.sleep(2.0 * (2**attempt))
    raise FetchError(f"download {url} failed after {MAX_ATTEMPTS} attempts: {last_error}")


def open_maybe_gzip(path: Path):
    """Open a file as text, transparently handling gzip."""
    with path.open("rb") as fh:
        magic = fh.read(2)
    if magic == b"\x1f\x8b":
        return gzip.open(path, "rt", encoding="utf-8")
    return path.open("r", encoding="utf-8")


def nvd_headers() -> dict[str, str]:
    return {"apiKey": config.NVD_API_KEY} if config.NVD_API_KEY else {}


def nvd_sleep() -> None:
    time.sleep(NVD_SLEEP_WITH_KEY if config.NVD_API_KEY else NVD_SLEEP_NO_KEY)
