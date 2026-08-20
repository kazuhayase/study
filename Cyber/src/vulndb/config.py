"""Configuration, resolved from environment variables with sensible local defaults."""

from __future__ import annotations

import os
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]

# NVD issues free API keys at https://nvd.nist.gov/developers/request-an-api-key
# Without one the public rate limit is 5 requests / 30s; with one it is 50 / 30s.
# A full 380k-CVE load is ~191 pages, so the key is the difference between minutes and an hour.
NVD_API_KEY: str | None = os.environ.get("NVD_API_KEY") or None

DB_PATH = Path(os.environ.get("VULNDB_PATH", PROJECT_ROOT / "data" / "cyber.duckdb"))
DATA_DIR = Path(os.environ.get("VULNDB_DATA_DIR", PROJECT_ROOT / "data"))
MIGRATIONS_DIR = PROJECT_ROOT / "migrations"

# --- Upstream endpoints ------------------------------------------------------
# All verified reachable on 2026-08-20.

NVD_API_URL = "https://services.nvd.nist.gov/rest/json/cves/2.0"
NVD_PAGE_SIZE = 2000  # API maximum
NVD_MAX_WINDOW_DAYS = 120  # API maximum span for lastModStartDate/lastModEndDate

KEV_URL = "https://www.cisa.gov/sites/default/files/feeds/known_exploited_vulnerabilities.json"

# Daily full-corpus scores, refreshed shortly after 13:30 UTC.
EPSS_CSV_URL = "https://epss.empiricalsecurity.com/epss_scores-current.csv.gz"

VULNRICHMENT_REPO = "cisagov/vulnrichment"
VULNRICHMENT_BRANCH = "develop"
# ~85 MB, versus ~331 MB for a git clone of the same content.
VULNRICHMENT_TARBALL_URL = (
    f"https://codeload.github.com/{VULNRICHMENT_REPO}/tar.gz/refs/heads/{VULNRICHMENT_BRANCH}"
)
GITHUB_API = "https://api.github.com"

# cisa.gov returns 403 to default urllib/curl agents; a browser UA is served normally.
USER_AGENT = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"
)

HTTP_TIMEOUT = 120


def ensure_dirs() -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
