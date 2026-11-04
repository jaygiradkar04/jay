#!/usr/bin/env python3
"""Fetch jobs from Greenhouse/Lever/Ashby boards, filter, and report only NEW postings.

Usage: python3 search.py [--all] [--reset]
  (default) print + save only postings not seen in earlier runs
  --all     ignore seen-state and show everything that matches
  --reset   forget seen-state
State: seen.json   Output log: new_jobs.csv
"""
import csv, json, re, sys, html, urllib.request
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone, timedelta
from pathlib import Path

HERE = Path(__file__).parent
CFG = json.loads((HERE / "config.json").read_text())
COMPANIES = json.loads((HERE / "companies.json").read_text())
SEEN_F, CSV_F = HERE / "seen.json", HERE / "new_jobs.csv"
UA = {"User-Agent": "job-search-script/0.1"}


def get(url):
    with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=30) as r:
        return json.load(r)


def strip(t):
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", html.unescape(t or ""))).strip()


def iso(ts):
    if ts is None: return None
    if isinstance(ts, (int, float)): return datetime.fromtimestamp(ts / 1000, timezone.utc)
    try: return datetime.fromisoformat(ts.replace("Z", "+00:00"))
    except ValueError: return None


def fetch(c):
    s = c["slug"]
    if c["ats"] == "greenhouse":
        data = get(f"https://boards-api.greenhouse.io/v1/boards/{s}/jobs?content=true")["jobs"]
        return [dict(id=f"gh-{s}-{j['id']}", title=j["title"], loc=(j.get("location") or {}).get("name", ""),
                     url=j["absolute_url"], posted=iso(j.get("first_published") or j.get("updated_at")),
                     desc=strip(j.get("content"))) for j in data]
    if c["ats"] == "lever":
        data = get(f"https://api.lever.co/v0/postings/{s}?mode=json")
        return [dict(id=f"lv-{j['id']}", title=j["text"], loc=(j.get("categories") or {}).get("location", ""),
                     url=j["hostedUrl"], posted=iso(j.get("createdAt")),
                     desc=strip(j.get("descriptionPlain"))) for j in data]
    if c["ats"] == "ashby":
        data = get(f"https://api.ashbyhq.com/posting-api/job-board/{s}")["jobs"]
        return [dict(id=f"ab-{j['id']}", title=j["title"], loc=j.get("location", ""),
                     url=j["jobUrl"], posted=iso(j.get("publishedAt")),
                     desc=strip(j.get("descriptionPlain") or j.get("descriptionHtml"))) for j in data]
    raise ValueError(c["ats"])


def keep(j):
    t, l, d = j["title"].lower(), j["loc"].lower(), j["desc"].lower()
    if not any(k in t for k in CFG["title_include"]): return False
    if any(k in t for k in CFG["title_exclude"]): return False
    if l and not any(k in l for k in CFG["location_include"]): return False
    if any(k in d for k in CFG["description_exclude"]): return False
    if j["posted"] and j["posted"] < datetime.now(timezone.utc) - timedelta(days=CFG["max_age_days"]): return False
    return True


def main():
    args = set(sys.argv[1:])
    if "--reset" in args:
        SEEN_F.unlink(missing_ok=True); print("seen-state cleared"); return
    seen = set(json.loads(SEEN_F.read_text())) if SEEN_F.exists() else set()

    def run(c):
        try: return c, fetch(c), None
        except Exception as e: return c, [], e

    found = []
    with ThreadPoolExecutor(8) as ex:
        for c, jobs, err in ex.map(run, COMPANIES):
            if err: print(f"! {c['name']}: {err}", file=sys.stderr); continue
            found += [dict(j, company=c["name"]) for j in jobs if keep(j)]

    new = [j for j in found if "--all" in args or j["id"] not in seen]
    new.sort(key=lambda j: j["posted"] or datetime.min.replace(tzinfo=timezone.utc), reverse=True)
    for j in new:
        p = j["posted"].strftime("%Y-%m-%d") if j["posted"] else "?"
        print(f"[{p}] {j['company']} | {j['title']} | {j['loc']}\n    {j['url']}")
    print(f"\n{len(new)} new / {len(found)} matching")

    if new and "--all" not in args:
        first = not CSV_F.exists()
        with CSV_F.open("a", newline="") as f:
            w = csv.writer(f)
            if first: w.writerow(["found_on", "posted", "company", "title", "location", "url", "status"])
            today = datetime.now().strftime("%Y-%m-%d")
            for j in new:
                w.writerow([today, j["posted"].strftime("%Y-%m-%d") if j["posted"] else "", j["company"], j["title"], j["loc"], j["url"], "new"])
    if "--all" not in args:
        SEEN_F.write_text(json.dumps(sorted(seen | {j["id"] for j in found})))


if __name__ == "__main__":
    main()
