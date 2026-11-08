"""Shared job queue (JSON Lines) that every source writes to.

Sources: jobright (PostingFinder), career-ops (scan.mjs output), manual.
Dedupe key is the employer's ATS identity, not the aggregator URL, so the same
Greenhouse job found by JobRight and by career-ops collapses into one record.

Stages: found -> verified -> gated -> tailored -> applied | skipped
"""
from __future__ import annotations

import json
import re
from pathlib import Path
from urllib.parse import parse_qs, urlparse

STAGES = ["found", "verified", "gated", "tailored", "applied", "skipped"]
_ATS = [
    (r"greenhouse\.io/([^/]+)/jobs/(\d+)", "greenhouse"),
    (r"jobs\.lever\.co/([^/]+)/([0-9a-f-]{8,})", "lever"),
    (r"jobs\.ashbyhq\.com/([^/]+)/([0-9a-f-]{8,})", "ashby"),
    (r"apply\.workable\.com/([^/]+)/j/([0-9A-Za-z]+)", "workable"),
]


def canonical_key(url: str) -> str:
    """Stable identity for a posting: ats:company:jobid, else normalized URL."""
    u = (url or "").strip()
    parsed = urlparse(u)
    gh = parse_qs(parsed.query).get("gh_jid")
    if gh:  # company career pages that embed a Greenhouse job id
        return f"greenhouse:{parsed.netloc.lower()}:{gh[0]}"
    for pat, name in _ATS:
        m = re.search(pat, u, re.I)
        if m:
            return f"{name}:{m.group(1).lower()}:{m.group(2).lower()}"
    return f"url:{parsed.netloc.lower()}{parsed.path.rstrip('/').lower()}"


class Queue:
    def __init__(self, path: str | Path):
        self.path = Path(path)
        self.jobs: dict[str, dict] = {}
        if self.path.exists():
            for line in self.path.read_text().splitlines():
                if line.strip():
                    rec = json.loads(line)
                    self.jobs[rec["key"]] = rec

    def add(self, *, url: str, employer: str, title: str, source: str,
            posted: str = "", source_score: float | None = None, **extra) -> tuple[dict, bool]:
        """Insert or merge. Returns (record, is_new)."""
        key = canonical_key(url)
        if key in self.jobs:
            rec = self.jobs[key]
            rec.setdefault("sources", [])
            if source not in rec["sources"]:
                rec["sources"].append(source)
            if source_score is not None:
                rec.setdefault("scores", {})[source] = source_score
            return rec, False
        rec = {"key": key, "employer": employer, "title": title, "url": url,
               "posted": posted, "stage": "found", "sources": [source],
               "scores": {source: source_score} if source_score is not None else {},
               **extra}
        self.jobs[key] = rec
        return rec, True

    def advance(self, key: str, stage: str, **fields) -> dict:
        if stage not in STAGES:
            raise ValueError(f"unknown stage {stage}")
        rec = self.jobs[key]
        rec["stage"] = stage
        rec.update(fields)
        return rec

    def by_stage(self, stage: str) -> list[dict]:
        return [j for j in self.jobs.values() if j["stage"] == stage]

    def save(self) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.path.write_text("".join(json.dumps(j, sort_keys=True) + "\n" for j in self.jobs.values()))
