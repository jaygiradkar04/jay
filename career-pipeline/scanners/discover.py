"""Find which H-1B sponsors have a scannable public job board.

Input: an H-1B employer index (msampath/h1b-sponsor-data, built from DOL LCA
and PERM disclosure files; one JSON object per line). Fields used:
  n legal name, ly last filing year, filed LCAs filed, perm PERM filings,
  sh share of filings at a secondary (third-party) worksite.
`sh` is the data-driven staffing/outsourcing signal: direct employers sit near
0, body shops near 1. That matters for STEM OPT, which needs direct employment.

We guess board slugs from the legal name and probe Greenhouse/Lever/Ashby.
A slug that answers is a *guess confirmed by the board existing*; names can
collide, so every hit is printed for a human to eyeball before scanning.
"""
from __future__ import annotations

import gzip
import json
import re
from concurrent.futures import ThreadPoolExecutor

from .ats_scan import API, fetch_json as _fetch, normalize, title_ok


def fetch_json(url, timeout=10):
    return _fetch(url, timeout)

_SUFFIX = re.compile(
    r"\b(incorporated|inc|llc|l\.l\.c|corp|corporation|co|company|ltd|limited|lp|llp|plc|"
    r"holdings?|group|usa|us|america|americas|services|technologies|technology)\b\.?", re.I)


def load_index(path: str) -> list[dict]:
    opener = gzip.open if path.endswith(".gz") else open
    with opener(path, "rt") as fh:
        return [json.loads(l) for l in fh if l.strip()]


def pick_direct_sponsors(rows, *, min_year=2025, min_filed=30, max_filed=6000, max_secondary=0.1):
    out = [r for r in rows if r["ly"] >= min_year and min_filed <= r["filed"] <= max_filed
           and r["sh"] <= max_secondary]
    return sorted(out, key=lambda r: -r["filed"])


def slug_candidates(legal_name: str) -> list[str]:
    name = re.split(r"\bd/?b/?a\b", legal_name, flags=re.I)[-1]   # prefer the trade name
    name = re.sub(r"[,.&'’]", " ", name)
    core = re.sub(r"\s+", " ", _SUFFIX.sub(" ", name)).strip().lower()
    words = [w for w in re.split(r"[^a-z0-9]+", core) if w]
    if words and words[0] == "the":
        words = words[1:]
    if not words:
        return []
    cands = ["".join(words), "-".join(words)]
    # No first-word fallback: "Capital One" -> "capital" would match an unrelated board.
    return list(dict.fromkeys(c for c in cands if len(c) >= 3))


def probe(name: str, fetcher=fetch_json) -> list[dict]:
    """Return [{ats, slug, jobs}] for every board that answers for this name."""
    hits = []
    for slug in slug_candidates(name):
        for ats in API:
            try:
                jobs = normalize(ats, name, fetcher(API[ats].format(slug=slug)))
            except Exception:
                continue            # 404 / timeout / bad JSON: no board here
            if jobs:
                hits.append({"ats": ats, "slug": slug, "jobs": jobs})
    return hits


def discover(rows, positive, negative, limit=400, workers=8, fetcher=fetch_json, offset=0):
    """Probe the top `limit` direct sponsors; report boards with matching titles."""
    def work(r):
        try:
            return [{"ats": h["ats"], "slug": h["slug"], "name": r["n"], "filed": r["filed"],
                     "perm": r["perm"], "ly": r["ly"], "n_jobs": len(h["jobs"]),
                     "matches": [j["title"] for j in h["jobs"] if title_ok(j["title"], positive, negative)]}
                    for h in probe(r["n"], fetcher)]
        except Exception:
            return []               # never let one employer stop the run

    results: list[dict] = []
    with ThreadPoolExecutor(max_workers=workers) as ex:
        for found in ex.map(work, pick_direct_sponsors(rows)[offset:offset + limit]):
            results.extend(found)
    return results
