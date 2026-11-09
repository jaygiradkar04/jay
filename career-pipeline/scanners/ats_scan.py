"""Cloud-safe scanner for public employer job-board APIs.

Why this exists instead of career-ops' scan.mjs: inside a proxy-only sandbox
career-ops bypasses the proxy unless you assert the proxy blocks private
addresses. This scanner uses urllib, which honors the sandbox's HTTPS_PROXY,
talks only to fixed public API hosts, and is small enough to audit.

Supported: Greenhouse, Lever, Ashby (public, unauthenticated board APIs).
Output records are queue-ready, and include the job description so the
sponsorship gate can run immediately.
"""
from __future__ import annotations

import html
import json
import re
import urllib.request
from datetime import datetime, timedelta, timezone

UA = "career-pipeline/0.1 (personal job search)"
API = {
    "greenhouse": "https://boards-api.greenhouse.io/v1/boards/{slug}/jobs?content=true",
    "lever": "https://api.lever.co/v0/postings/{slug}?mode=json",
    "ashby": "https://api.ashbyhq.com/posting-api/job-board/{slug}",
}


def fetch_json(url: str, timeout: int = 30):
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "application/json"})
    with urllib.request.urlopen(req, timeout=timeout) as r:  # honors HTTPS_PROXY
        return json.load(r)


def html_to_text(s: str) -> str:
    s = html.unescape(s or "")
    s = re.sub(r"(?i)<br\s*/?>|</p>|</li>|</h\d>", "\n", s)
    s = re.sub(r"<[^>]+>", " ", s)
    s = html.unescape(s)
    return re.sub(r"[ \t]+", " ", re.sub(r"\n\s*\n+", "\n", s)).strip()


def _date(value) -> str:
    """ISO string or epoch-ms -> YYYY-MM-DD ('' if unknown)."""
    if not value:
        return ""
    if isinstance(value, (int, float)):
        return datetime.fromtimestamp(value / 1000, tz=timezone.utc).strftime("%Y-%m-%d")
    return str(value)[:10]


def normalize(ats: str, company: str, payload) -> list[dict]:
    out: list[dict] = []
    if ats == "greenhouse":
        for j in payload.get("jobs", []):
            out.append({"url": j.get("absolute_url", ""), "employer": company,
                        "title": j.get("title", ""), "location": (j.get("location") or {}).get("name", ""),
                        "posted": _date(j.get("first_published") or j.get("updated_at")),
                        "jd": html_to_text(j.get("content", ""))})
    elif ats == "lever":
        for j in payload if isinstance(payload, list) else []:
            jd = "\n".join([j.get("descriptionPlain") or "", j.get("additionalPlain") or ""]
                           + [html_to_text(x.get("content", "")) for x in j.get("lists", [])])
            out.append({"url": j.get("hostedUrl", ""), "employer": company,
                        "title": j.get("text", ""), "location": (j.get("categories") or {}).get("location", ""),
                        "posted": _date(j.get("createdAt")), "jd": jd.strip()})
    elif ats == "ashby":
        for j in payload.get("jobs", []):
            if j.get("isListed") is False:
                continue
            out.append({"url": j.get("jobUrl") or j.get("applyUrl", ""), "employer": company,
                        "title": j.get("title", ""), "location": j.get("location", ""),
                        "posted": _date(j.get("publishedAt")),
                        "jd": j.get("descriptionPlain") or html_to_text(j.get("descriptionHtml", ""))})
    else:
        raise ValueError(f"unsupported ats: {ats}")
    return [o for o in out if o["url"]]


def title_ok(title: str, positive: list[str], negative: list[str]) -> bool:
    t = title.lower()
    if any(n.lower() in t for n in negative):
        return False
    return not positive or any(p.lower() in t for p in positive)


def scan(config: dict, fetcher=fetch_json, today: datetime | None = None) -> tuple[list[dict], list[str]]:
    """Return (jobs, errors). Filters by title and max_age_days; unknown dates are kept."""
    today = today or datetime.now(timezone.utc)
    pos = config.get("title_positive", [])
    neg = config.get("title_negative", [])
    cutoff = (today - timedelta(days=config.get("max_age_days", 14))).strftime("%Y-%m-%d")
    jobs: list[dict] = []
    errors: list[str] = []
    for c in config["companies"]:
        try:
            payload = fetcher(API[c["ats"]].format(slug=c["slug"]))
            for j in normalize(c["ats"], c["name"], payload):
                if not title_ok(j["title"], pos, neg):
                    continue
                if j["posted"] and j["posted"] < cutoff:
                    continue
                jobs.append(j)
        except Exception as e:  # one bad board must not stop the scan
            errors.append(f'{c.get("name", "?")}: {type(e).__name__}: {e}')
    return jobs, errors
