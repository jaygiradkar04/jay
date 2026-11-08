"""Adapter: career-ops `data/pipeline.md` -> career-pipeline queue.

Reads the inbox file career-ops writes and tracks. Read-only on career-ops'
files; it never edits pipeline.md (career-ops owns that file and locks it).

Row shapes handled (see career-ops scan.mjs formatPipelineOffer and
modes/pipeline.md):
  pending    - [ ] URL | Company | Title [| Location [| Comp]] [| posted: D]
                      [| trust: ..] [| yrs: ..] [| note: ..] [| rank: n/5 ..]
  processed  - [x] #143 | URL | Company | Role | 3.4/5 | PDF ok
  expired    - [x] ~~URL | Company | Role~~ - posting expired (...)
  pre-screen - [x] #-- | URL | Company | Role | skipped (reason)
  unfetched  - [!] URL ...            (ignored: not evidence of a live posting)
"""
from __future__ import annotations

import re

_CHECKBOX = re.compile(r"^\s*- \[([ x!])\]\s+(.*)$")
_URL = re.compile(r"https?://[^\s|~]+")
_LABELED = re.compile(r"^(posted|trust|yrs|note|rank):\s*(.*)$", re.I)
_SCORE = re.compile(r"^(\d(?:\.\d+)?)\s*/\s*5\b")
_COMP = re.compile(r"[$€£]|\bk\b|\d{2,3},\d{3}", re.I)


def _cells(body: str) -> list[str]:
    return [c.strip() for c in body.split("|")]


def parse_line(line: str) -> dict | None:
    """Parse one inbox line into a queue-ready dict, or None if not an entry."""
    m = _CHECKBOX.match(line)
    if not m:
        return None
    mark, rest = m.group(1), m.group(2)
    if mark == "!":
        return None

    expired = rest.startswith("~~")
    body = rest[2:] if expired else rest
    if expired:
        closed = re.match(r"(.*?)~~", body)
        body = closed.group(1) if closed else body

    cells = _cells(body)
    u_idx = next((i for i, c in enumerate(cells) if _URL.search(c)), -1)
    if u_idx == -1:
        return None
    url = _URL.search(cells[u_idx]).group(0).rstrip(".,)")
    after = cells[u_idx + 1:]

    prescreen = cells[0].startswith("#--")
    rec: dict = {"url": url, "source": "career-ops", "employer": "", "title": "",
                 "stage": "found", "extra": {}}
    rec["employer"] = after[0] if len(after) > 0 else ""
    rec["title"] = after[1] if len(after) > 1 else ""

    # Remaining positional/labeled cells after company and title.
    for cell in after[2:]:
        lab = _LABELED.match(cell)
        if lab:
            key, val = lab.group(1).lower(), lab.group(2).strip()
            if key == "posted":
                rec["posted"] = val
            elif key == "rank":
                s = _SCORE.match(val)
                if s:
                    rec["score"] = float(s.group(1))
                rec["extra"]["rank_note"] = val
            else:
                rec["extra"][key] = val
        elif prescreen and cell.lower().startswith("skipped"):
            rec["stage"] = "skipped"
            rec["extra"]["skip_reason"] = cell
        elif (s := _SCORE.match(cell)):
            rec["score"] = float(s.group(1))      # evaluated by career-ops
            rec["stage"] = "verified"
        elif cell.upper().startswith("PDF"):
            rec["extra"]["pdf"] = "✅" in cell
        elif _COMP.search(cell):
            rec["extra"]["comp"] = cell
        elif cell and "location" not in rec["extra"]:
            rec["extra"]["location"] = cell

    if expired:
        rec["stage"] = "skipped"
        rec["extra"]["skip_reason"] = "expired (career-ops liveness sweep)"
    return rec


def parse_pipeline(text: str) -> list[dict]:
    return [r for r in map(parse_line, text.splitlines()) if r]


def ingest(queue, text: str) -> dict:
    """Merge a pipeline.md into `queue`. Returns counts. Never downgrades stage."""
    from pipeline.queue import STAGES

    counts = {"added": 0, "merged": 0, "skipped": 0, "ignored": 0}
    lines = text.splitlines()
    parsed = parse_pipeline(text)
    counts["ignored"] = sum(1 for l in lines if _CHECKBOX.match(l)) - len(parsed)
    for r in parsed:
        rec, new = queue.add(url=r["url"], employer=r["employer"], title=r["title"],
                             source="career-ops", posted=r.get("posted", ""),
                             source_score=r.get("score"), **r["extra"])
        counts["added" if new else "merged"] += 1
        target = r["stage"]
        if rec["stage"] in ("tailored", "applied"):
            continue  # a posting closing after you acted on it is normal
        # A dead/discarded posting wins; otherwise only move forward.
        if target == "skipped" or STAGES.index(target) > STAGES.index(rec["stage"]):
            queue.advance(rec["key"], target)
            counts["skipped"] += target == "skipped"
    return counts
