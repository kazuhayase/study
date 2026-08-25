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

# --- Vendor security advisories -----------------------------------------------
# Verified reachable, unauthenticated, on 2026-08-21.

AWS_BULLETINS_RSS_URL = "https://aws.amazon.com/security/security-bulletins/rss/feed/"

# Auth/API-key requirement was dropped in 2021. /updates lists every monthly release since
# 1999 (~48 KB); init only walks the recent window below, since older CVEs are already
# covered by NVD.
MSRC_CVRF_UPDATES_URL = "https://api.msrc.microsoft.com/cvrf/v3.0/updates"
MSRC_CVRF_DOC_URL = "https://api.msrc.microsoft.com/cvrf/v3.0/cvrf/{release_id}"
MSRC_INIT_LOOKBACK_MONTHS = 24

# segment="" spans every Broadcom division (VMware, Symantec, CA mainframe) in one feed,
# sorted newest-first -- confirmed 2026-08-21, no per-division enumeration needed.
BROADCOM_ADVISORY_API_URL = (
    "https://support.broadcom.com/web/ecx/security-advisory/-/securityadvisory/"
    "getSecurityAdvisoryList"
)
BROADCOM_PAGE_SIZE = 100

# Public, unauthenticated, but query-only: there is no full-listing or date-range endpoint
# (confirmed by inspecting the site's own network traffic), so coverage is bounded by this
# term list. `limit`/`offset` query params are accepted but ignored -- each term returns up
# to 2,000 results (~24 MB) regardless, sorted by field_pub_date descending.
IBM_SEARCH_API_URL = "https://www.ibm.com/support/pages/securityapp/api/search"
IBM_PRODUCT_SEARCH_TERMS = [
    # "MQ" alone returns 0 results (confirmed 2026-08-21) -- the search engine needs the
    # fuller product name, not every short/generic term works standalone.
    # "WebSphere" alone hit the 2,000-result cap (~24MB) and kept failing on this connection
    # (confirmed 2026-08-25). Split the same way as Db2 below. Coverage is imperfect --
    # "WebSphere Application Server" (no further qualifier) timed out even alone and is
    # dropped rather than chased further; "IBM WebSphere" is the broad catch-all replacement.
    "IBM WebSphere", "WebSphere Application Server Liberty",
    "WebSphere Application Server Network Deployment", "WebSphere Hybrid Edition",
    "WebSphere Portal", "WebSphere Commerce", "WebSphere Application Server for z/OS",
    "AIX",
    # "Db2" alone hit the API's 2,000-result cap (truncated) and its ~24MB response kept
    # failing with IncompleteRead on flaky connections (confirmed 2026-08-21). Split into
    # narrower product-line terms: smaller responses survive a bad connection, and the split
    # terms' combined count (2,509) exceeds the capped total, recovering previously-truncated
    # results too. The same 2,000-cap likely affects QRadar/Cognos/Cloud Pak/InfoSphere/Guardium
    # below -- not yet split, lower priority since they haven't caused failures.
    # NOTE: the API's response size for a *fixed* query is not stable -- "Db2 Warehouse" measured
    # 3.6MB, then 21MB, on identical repeated calls (confirmed 2026-08-21). Splitting narrower
    # lowers the ceiling but doesn't guarantee a small response every time; treat this as
    # harm reduction, not a full fix.
    "Db2 for Linux", "Db2 for z/OS", "IBM Db2 Warehouse", "Db2 Warehouse Integrated Analytics",
    "Db2 Connect", "Db2 Big SQL",
    "QRadar", "Cognos", "IBM MQ", "Cloud Pak", "Maximo",
    "Tivoli", "Netezza", "InfoSphere", "Guardium", "Sterling", "z/OS", "CICS",
]

# cisa.gov returns 403 to default urllib/curl agents; a browser UA is served normally.
USER_AGENT = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"
)

# This is a socket inactivity timeout (per urllib semantics), not a total-transfer deadline --
# a slow-but-flowing download of any size is unaffected. It only fires when a connection stalls
# with no bytes at all. 120s was too generous on a flaky connection: confirmed 2026-08-21 that
# most retries were spent waiting out the full 120s on a hung socket before the retry loop even
# got a chance to try again, collapsing throughput far more than the retry backoff itself does.
HTTP_TIMEOUT = 20


def ensure_dirs() -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
