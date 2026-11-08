"""career-pipeline CLI.  Run from career-pipeline/:  python3 -m pipeline.cli <cmd>

  add      add one job (any source)
  import   bulk-add from a JSON list (JobRight scrape, career-ops export)
  gate     run the sponsorship gate on a job's description
  list     show the queue
  package  emit the handoff package for ResumePerfector (gated, not BLOCK)
"""
from __future__ import annotations

import argparse
import json
import sys

from .queue import STAGES, Queue
from .sponsorship import BLOCK, classify

DEFAULT_QUEUE = "data/jobs.jsonl"


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(prog="pipeline")
    p.add_argument("--queue", default=DEFAULT_QUEUE)
    sub = p.add_subparsers(dest="cmd", required=True)

    a = sub.add_parser("add")
    a.add_argument("--url", required=True, help="employer ATS apply URL")
    a.add_argument("--employer", required=True)
    a.add_argument("--title", required=True)
    a.add_argument("--source", required=True, choices=["jobright", "career-ops", "manual"])
    a.add_argument("--posted", default="")
    a.add_argument("--score", type=float, default=None)

    i = sub.add_parser("import")
    i.add_argument("file", help="JSON list of {url, employer, title, source, posted?, score?}")

    g = sub.add_parser("gate")
    g.add_argument("key")
    g.add_argument("--jd-file", help="job description text; default stdin")

    l = sub.add_parser("list")
    l.add_argument("--stage", choices=STAGES)

    sub.add_parser("package")

    args = p.parse_args(argv)
    q = Queue(args.queue)

    if args.cmd == "add":
        rec, new = q.add(url=args.url, employer=args.employer, title=args.title,
                         source=args.source, posted=args.posted, source_score=args.score)
        q.save()
        print(("added " if new else "merged ") + rec["key"])
    elif args.cmd == "import":
        added = merged = 0
        with open(args.file) as fh:
            rows = json.load(fh)
        for row in rows:
            _, new = q.add(url=row["url"], employer=row["employer"], title=row["title"],
                           source=row["source"], posted=row.get("posted", ""),
                           source_score=row.get("score"))
            added += new
            merged += not new
        q.save()
        print(f"added {added}, merged {merged} duplicates")
    elif args.cmd == "gate":
        if args.jd_file:
            with open(args.jd_file) as fh:
                jd = fh.read()
        else:
            jd = sys.stdin.read()
        rec = q.jobs[args.key]
        res = classify(jd, rec["employer"])
        q.advance(args.key, "skipped" if res["verdict"] == BLOCK else "gated",
                  sponsorship=res["verdict"], flags=res["flags"], gate_reasons=res["reasons"])
        q.save()
        print(json.dumps(res, indent=2))
    elif args.cmd == "list":
        for j in sorted(q.jobs.values(), key=lambda j: j["stage"]):
            if args.stage and j["stage"] != args.stage:
                continue
            print(f'{j["stage"]:9} {j.get("sponsorship", "-"):15} {j["employer"]} | {j["title"]} | {j["key"]}')
    elif args.cmd == "package":
        for j in q.by_stage("gated"):
            print(f'## {j["employer"]} - {j["title"]}\n- Apply page: {j["url"]}\n'
                  f'- Posted (employer date): {j.get("posted") or "unknown"}\n'
                  f'- Sources: {", ".join(j["sources"])}  scores: {j.get("scores", {})}\n'
                  f'- Sponsorship: {j.get("sponsorship")}  flags: {j.get("flags")}\n'
                  f'- Gate notes: {" ".join(j.get("gate_reasons", []))}\n'
                  f'- Reminder: do not claim skills the resume does not support; '
                  f'leave work-authorization/sponsorship answers to the candidate.\n')
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
