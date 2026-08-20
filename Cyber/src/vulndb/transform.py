"""Bronze -> Silver parsing.

Every function here is pure: JSON in, plain dict out, no database and no network. That is what
makes them testable against small fixtures, and it means a parser bug is fixed by editing this
file and re-running `rebuild` -- never by re-downloading from upstream.
"""

from __future__ import annotations

from typing import Any

# SSVC option keys differ between the two feeds that carry them. Verified against live records
# on 2026-08-20:
#   NVD          -> {"exploitation": ..., "automatable": ..., "technicalImpact": ...}
#   Vulnrichment -> {"Exploitation": ..., "Automatable": ..., "Technical Impact": ...}
# Normalising to lowercase-without-spaces collapses both onto one set of names.
_SSVC_KEYS = {
    "exploitation": "exploitation",
    "automatable": "automatable",
    "technicalimpact": "technical_impact",
}


def _normalise_ssvc_options(options: list[dict[str, Any]]) -> dict[str, str]:
    out: dict[str, str] = {}
    for opt in options or []:
        for raw_key, value in opt.items():
            key = _SSVC_KEYS.get(raw_key.replace(" ", "").replace("_", "").lower())
            if key and isinstance(value, str):
                out[key] = value.strip().lower()
    return out


def _pick_metric(metrics: list[dict[str, Any]] | None) -> dict[str, Any] | None:
    """NVD may carry several CVSS entries per version; the Primary one is authoritative."""
    if not metrics:
        return None
    for m in metrics:
        if m.get("type") == "Primary":
            return m
    return metrics[0]


def parse_nvd_cve(cve: dict[str, Any]) -> dict[str, Any]:
    """vulnerabilities[].cve -> a silver.cve row."""
    descriptions = cve.get("descriptions") or []
    description_en = next(
        (d.get("value") for d in descriptions if d.get("lang") == "en"), None
    )

    metrics = cve.get("metrics") or {}
    v31 = _pick_metric(metrics.get("cvssMetricV31")) or {}
    v40 = _pick_metric(metrics.get("cvssMetricV40")) or {}
    v31_data = v31.get("cvssData") or {}
    v40_data = v40.get("cvssData") or {}

    cwe_ids: list[str] = []
    for weakness in cve.get("weaknesses") or []:
        for desc in weakness.get("description") or []:
            value = desc.get("value")
            if value and value.startswith("CWE-") and value not in cwe_ids:
                cwe_ids.append(value)

    return {
        "cve_id": cve["id"],
        "published": cve.get("published"),
        "last_modified": cve.get("lastModified"),
        "vuln_status": cve.get("vulnStatus"),
        "description_en": description_en,
        "cvss_v31_base_score": v31_data.get("baseScore"),
        "cvss_v31_severity": v31_data.get("baseSeverity") or v31.get("baseSeverity"),
        "cvss_v31_vector": v31_data.get("vectorString"),
        "cvss_v40_base_score": v40_data.get("baseScore"),
        "cvss_v40_severity": v40_data.get("baseSeverity") or v40.get("baseSeverity"),
        "cvss_v40_vector": v40_data.get("vectorString"),
        "cwe_ids": cwe_ids,
        "source_identifier": cve.get("sourceIdentifier"),
        "is_rejected": (cve.get("vulnStatus") or "").lower() == "rejected",
    }


def parse_nvd_ssvc(cve: dict[str, Any]) -> dict[str, Any] | None:
    """cve.metrics.ssvcV203[].ssvcData -> a silver.ssvc row, or None if absent."""
    entries = (cve.get("metrics") or {}).get("ssvcV203") or []
    if not entries:
        return None
    data = entries[0].get("ssvcData") or {}
    opts = _normalise_ssvc_options(data.get("options") or [])
    if not opts:
        return None
    return {
        "cve_id": cve["id"],
        "exploitation": opts.get("exploitation"),
        "automatable": opts.get("automatable"),
        "technical_impact": opts.get("technical_impact"),
        "ssvc_version": data.get("version"),
        "role": data.get("role"),
        "decided_at": data.get("timestamp"),
        "source": "nvd",
    }


def parse_nvd_kev(cve: dict[str, Any]) -> dict[str, Any] | None:
    """NVD's own KEV mirror (cisaExploitAdd et al). Fallback only -- the catalog feed wins."""
    if not cve.get("cisaExploitAdd"):
        return None
    return {
        "cve_id": cve["id"],
        "date_added": cve.get("cisaExploitAdd"),
        "due_date": cve.get("cisaActionDue"),
        "known_ransomware_campaign_use": None,  # NVD does not carry this field
        "vendor_project": None,
        "product": None,
        "vulnerability_name": cve.get("cisaVulnerabilityName"),
        "required_action": cve.get("cisaRequiredAction"),
        "notes": None,
        "source": "nvd",
    }


def _cisa_adp_blocks(record: dict[str, Any], block_type: str) -> list[dict[str, Any]]:
    """Yield content dicts of a given type from the CISA-ADP container.

    Real shape, verified against cisagov/vulnrichment on 2026-08-20:
        containers.adp[] -> providerMetadata.shortName == 'CISA-ADP'
                         -> metrics[] -> other -> {"type": "ssvc"|"kev", "content": {...}}
    The record also carries an adp[] entry from the 'CVE' program itself with no metrics, so
    filtering on shortName matters.
    """
    found: list[dict[str, Any]] = []
    for adp in (record.get("containers") or {}).get("adp") or []:
        if (adp.get("providerMetadata") or {}).get("shortName") != "CISA-ADP":
            continue
        for metric in adp.get("metrics") or []:
            other = metric.get("other") or {}
            if other.get("type") == block_type and other.get("content"):
                found.append(other["content"])
    return found


def _vulnrichment_cve_id(record: dict[str, Any]) -> str | None:
    return ((record.get("cveMetadata") or {}).get("cveId")) or None


def parse_vulnrichment_ssvc(record: dict[str, Any]) -> dict[str, Any] | None:
    """A Vulnrichment CVE record file -> a silver.ssvc row, or None if CISA has not scored it."""
    for content in _cisa_adp_blocks(record, "ssvc"):
        opts = _normalise_ssvc_options(content.get("options") or [])
        if not opts:
            continue
        cve_id = _vulnrichment_cve_id(record) or content.get("id")
        if not cve_id:
            continue
        return {
            "cve_id": cve_id,
            "exploitation": opts.get("exploitation"),
            "automatable": opts.get("automatable"),
            "technical_impact": opts.get("technical_impact"),
            "ssvc_version": content.get("version"),
            "role": content.get("role"),
            "decided_at": content.get("timestamp"),
            "source": "vulnrichment",
        }
    return None


def parse_vulnrichment_kev(record: dict[str, Any]) -> dict[str, Any] | None:
    """CISA-ADP 'kev' block -> a minimal silver.kev row.

    A fallback for the days cisa.gov refuses the catalog feed: it carries dateAdded, which is what
    starts the remediation clock. It has no dueDate or ransomware flag, so the catalog still wins.
    """
    cve_id = _vulnrichment_cve_id(record)
    for content in _cisa_adp_blocks(record, "kev"):
        if not content.get("dateAdded") or not cve_id:
            continue
        return {
            "cve_id": cve_id,
            "date_added": content["dateAdded"],
            "due_date": None,
            "known_ransomware_campaign_use": None,
            "vendor_project": None,
            "product": None,
            "vulnerability_name": None,
            "required_action": None,
            "notes": content.get("reference"),
            "source": "vulnrichment",
        }
    return None


def parse_kev_entry(entry: dict[str, Any]) -> dict[str, Any]:
    """One element of the KEV catalog's vulnerabilities[] -> a silver.kev row."""
    return {
        "cve_id": entry["cveID"],
        "date_added": entry.get("dateAdded"),
        "due_date": entry.get("dueDate"),
        "known_ransomware_campaign_use": entry.get("knownRansomwareCampaignUse"),
        "vendor_project": entry.get("vendorProject"),
        "product": entry.get("product"),
        "vulnerability_name": entry.get("vulnerabilityName"),
        "required_action": entry.get("requiredAction"),
        "notes": entry.get("notes"),
        "source": "kev_catalog",
    }
