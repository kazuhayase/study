#!/usr/bin/env python3
"""Verify Bronze -> Silver parsing against fixtures captured from the live feeds.

The fixtures are real records, trimmed only of bulk (CPE lists, reference lists). The case that
matters most is SSVC: NVD and Vulnrichment publish the same decision points under different key
casing ("technicalImpact" vs "Technical Impact"), and a parser that handles one but not the other
would silently halve BOD 26-04 coverage instead of failing.

Run: python3 tests/test_parsers.py
"""

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from vulndb import transform  # noqa: E402

FIXTURES = Path(__file__).resolve().parent / "fixtures"

failures = []


def check(name, cond, detail=""):
    if cond:
        print(f"  ok   {name}")
    else:
        print(f"  FAIL {name} {detail}")
        failures.append(name)


def load(name):
    return json.loads((FIXTURES / name).read_text(encoding="utf-8"))


def main():
    enriched = load("nvd_cve_2024_3400.json")
    bare = load("nvd_cve_1999_0001.json")
    vr = load("vulnrichment_2024_3400.json")
    kev_entry = load("kev_entry_2024_3400.json")

    print("parse_nvd_cve")
    cve = transform.parse_nvd_cve(enriched)
    check("cve_id", cve["cve_id"] == "CVE-2024-3400", cve["cve_id"])
    check("description in English", (cve["description_en"] or "").startswith("A command injection"),
          repr(cve["description_en"])[:80])
    check("CVSS v3.1 base score", cve["cvss_v31_base_score"] == 10.0, cve["cvss_v31_base_score"])
    check("CVSS v3.1 severity", cve["cvss_v31_severity"] == "CRITICAL", cve["cvss_v31_severity"])
    check("CVSS vector present", (cve["cvss_v31_vector"] or "").startswith("CVSS:3.1/"),
          cve["cvss_v31_vector"])
    # NVD carries a weakness entry per assigning source, so one CVE legitimately maps to several
    # CWEs (here CWE-20 from the CNA and CWE-77 from NVD's own analysis). All are kept, deduped.
    check("CWE ids extracted from every source", cve["cwe_ids"] == ["CWE-20", "CWE-77"],
          cve["cwe_ids"])
    check("not rejected", cve["is_rejected"] is False)
    check("timestamps carried", bool(cve["published"]) and bool(cve["last_modified"]))

    print("\nparse_nvd_ssvc (lowerCamelCase keys)")
    ssvc = transform.parse_nvd_ssvc(enriched)
    check("ssvc found", ssvc is not None)
    check("exploitation", ssvc["exploitation"] == "active", ssvc["exploitation"])
    check("automatable", ssvc["automatable"] == "yes", ssvc["automatable"])
    check("technical_impact", ssvc["technical_impact"] == "total", ssvc["technical_impact"])
    check("version", ssvc["ssvc_version"] == "2.0.3", ssvc["ssvc_version"])
    check("source tagged nvd", ssvc["source"] == "nvd")
    check("absent ssvc returns None", transform.parse_nvd_ssvc(bare) is None)

    print("\nparse_vulnrichment_ssvc (Title Case keys, metrics[].other.content)")
    vssvc = transform.parse_vulnrichment_ssvc(vr)
    check("ssvc found", vssvc is not None)
    check("cve_id", vssvc["cve_id"] == "CVE-2024-3400", vssvc["cve_id"])
    check("exploitation", vssvc["exploitation"] == "active", vssvc["exploitation"])
    check("automatable", vssvc["automatable"] == "yes", vssvc["automatable"])
    check("technical_impact", vssvc["technical_impact"] == "total", vssvc["technical_impact"])
    check("source tagged vulnrichment", vssvc["source"] == "vulnrichment")

    print("\nboth feeds agree after normalisation")
    check(
        "NVD and Vulnrichment yield identical decision points",
        (ssvc["exploitation"], ssvc["automatable"], ssvc["technical_impact"])
        == (vssvc["exploitation"], vssvc["automatable"], vssvc["technical_impact"]),
        f"nvd={ssvc} vulnrichment={vssvc}",
    )

    print("\nparse_vulnrichment_kev")
    vkev = transform.parse_vulnrichment_kev(vr)
    check("kev block found", vkev is not None)
    check("date_added", vkev["date_added"] == "2024-04-12", vkev["date_added"])
    check("no CISA-ADP container -> None", transform.parse_vulnrichment_kev(
        {"cveMetadata": {"cveId": "CVE-2026-0001"}, "containers": {"adp": []}}) is None)

    print("\nparse_kev_entry (catalog feed)")
    kv = transform.parse_kev_entry(kev_entry)
    check("cve_id", kv["cve_id"] == "CVE-2024-3400", kv["cve_id"])
    check("date_added", kv["date_added"] == "2024-04-12", kv["date_added"])
    check("due_date", kv["due_date"] == "2024-04-19", kv["due_date"])
    check("ransomware flag present (catalog-only field)",
          kv["known_ransomware_campaign_use"] in {"Known", "Unknown"},
          kv["known_ransomware_campaign_use"])
    check("vendor/product carried", bool(kv["vendor_project"]) and bool(kv["product"]))
    check("source tagged kev_catalog", kv["source"] == "kev_catalog")

    print("\nparse_nvd_kev (NVD mirror)")
    nkev = transform.parse_nvd_kev(enriched)
    check("kev detected from cisaExploitAdd", nkev is not None)
    check("date_added matches catalog", nkev["date_added"] == kv["date_added"],
          f"{nkev['date_added']} vs {kv['date_added']}")
    check("ransomware flag absent in NVD (why the catalog wins)",
          nkev["known_ransomware_campaign_use"] is None)
    check("non-KEV CVE -> None", transform.parse_nvd_kev(bare) is None)

    print("\nedge cases")
    check("empty options -> None", transform.parse_nvd_ssvc(
        {"id": "CVE-2026-0002", "metrics": {"ssvcV203": [{"ssvcData": {"options": []}}]}}) is None)
    check("no metrics at all -> None",
          transform.parse_nvd_ssvc({"id": "CVE-2026-0003"}) is None)
    minimal = transform.parse_nvd_cve({"id": "CVE-2026-0004"})
    check("minimal record parses without raising", minimal["cve_id"] == "CVE-2026-0004")
    check("minimal record has no invented scores",
          minimal["cvss_v31_base_score"] is None and minimal["cwe_ids"] == [])
    check("rejected status detected", transform.parse_nvd_cve(
        {"id": "CVE-2026-0005", "vulnStatus": "Rejected"})["is_rejected"] is True)

    print()
    if failures:
        print(f"FAILED: {len(failures)} check(s): {', '.join(failures)}")
        return 1
    print("All checks passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
