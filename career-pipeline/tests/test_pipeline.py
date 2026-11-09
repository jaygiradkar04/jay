import json
import os
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from pipeline.cli import main
from pipeline.queue import Queue, canonical_key
from pipeline.sponsorship import BLOCK, LONG_TERM_RISK, OK_SPONSORS, UNKNOWN, classify


class Sponsorship(unittest.TestCase):
    def test_block_citizen_clearance_opt(self):
        self.assertEqual(classify("Must be a U.S. citizen. Active Secret clearance.")["verdict"], BLOCK)
        self.assertEqual(classify("We do not accept OPT or CPT candidates.")["verdict"], BLOCK)
        self.assertEqual(classify("This role is subject to ITAR.")["verdict"], BLOCK)

    def test_long_term_risk(self):
        for t in ["We will not sponsor visas now or in the future.",
                  "Candidates must be authorized to work without sponsorship.",
                  "Unable to sponsor employment visas."]:
            self.assertEqual(classify(t)["verdict"], LONG_TERM_RISK, t)

    def test_sponsors(self):
        self.assertEqual(classify("We offer H1B transfers.")["verdict"], OK_SPONSORS)
        self.assertEqual(classify("Visa sponsorship is available.")["verdict"], OK_SPONSORS)

    def test_no_sponsor_not_misread_as_sponsors(self):
        self.assertEqual(classify("We do not offer visa sponsorship.")["verdict"], LONG_TERM_RISK)

    def test_silent_is_unknown_and_mentions_everify(self):
        r = classify("Analyze data with SQL and Python.")
        self.assertEqual(r["verdict"], UNKNOWN)
        self.assertTrue(any("E-Verify" in x for x in r["reasons"]))
        self.assertIn("E_VERIFY", classify("We participate in E-Verify.")["flags"])

    def test_staffing_flag(self):
        r = classify("Our client is hiring. C2C welcome.", "Acme Staffing")
        self.assertIn("STAFFING_RISK", r["flags"])
        self.assertIn("STAFFING_RISK", classify("x", "Adept Consulting Services")["flags"])


class QueueTests(unittest.TestCase):
    def test_canonical_keys_dedupe_across_sources(self):
        a = canonical_key("https://job-boards.greenhouse.io/zipcolimited/jobs/4723591006")
        b = canonical_key("https://boards.greenhouse.io/zipcolimited/jobs/4723591006?utm=x")
        self.assertEqual(a, b)
        self.assertEqual(canonical_key("https://instacart.careers/job/?gh_jid=8115834"),
                         "greenhouse:instacart.careers:8115834")
        self.assertTrue(canonical_key("https://apply.workable.com/adept/j/C1A38B9608/").startswith("workable:adept:"))

    def test_merge_and_cli_flow(self):
        with tempfile.TemporaryDirectory() as d:
            qp = os.path.join(d, "jobs.jsonl")
            rows = [
                {"url": "https://job-boards.greenhouse.io/zipcolimited/jobs/4723591006",
                 "employer": "Zip", "title": "Product Analyst", "source": "jobright", "score": 72},
                {"url": "https://boards.greenhouse.io/zipcolimited/jobs/4723591006",
                 "employer": "Zip", "title": "Product Analyst", "source": "career-ops", "score": 4.1},
            ]
            f = os.path.join(d, "in.json")
            json.dump(rows, open(f, "w"))
            main(["--queue", qp, "import", f])
            q = Queue(qp)
            self.assertEqual(len(q.jobs), 1)
            rec = next(iter(q.jobs.values()))
            self.assertEqual(sorted(rec["sources"]), ["career-ops", "jobright"])
            jd = os.path.join(d, "jd.txt")
            open(jd, "w").write("We offer H1B transfers and participate in E-Verify.")
            main(["--queue", qp, "gate", rec["key"], "--jd-file", jd])
            self.assertEqual(Queue(qp).jobs[rec["key"]]["stage"], "gated")
            open(jd, "w").write("US citizens only.")
            main(["--queue", qp, "gate", rec["key"], "--jd-file", jd])
            self.assertEqual(Queue(qp).jobs[rec["key"]]["stage"], "skipped")


class AtsScanner(unittest.TestCase):
    GH = {"jobs": [
        {"title": "Senior Data Analyst", "absolute_url": "https://job-boards.greenhouse.io/acme/jobs/1",
         "location": {"name": "Remote - US"}, "first_published": "2026-11-05T10:00:00-05:00",
         "content": "&lt;p&gt;Analyze data. We offer H1B transfers and use E-Verify.&lt;/p&gt;"},
        {"title": "Data Analyst Intern", "absolute_url": "https://job-boards.greenhouse.io/acme/jobs/2",
         "location": {"name": "NYC"}, "first_published": "2026-11-05", "content": ""},
        {"title": "Business Analyst", "absolute_url": "https://job-boards.greenhouse.io/acme/jobs/3",
         "location": {"name": "Remote"}, "first_published": "2026-01-01", "content": "old"},
        {"title": "Product Analyst", "absolute_url": "https://job-boards.greenhouse.io/acme/jobs/4",
         "location": {"name": "Remote"}, "first_published": "2026-11-06",
         "content": "&lt;p&gt;US citizens only. Security clearance required.&lt;/p&gt;"}]}
    LEVER = [{"text": "Analytics Engineer", "hostedUrl": "https://jobs.lever.co/acme/0f1e2d3c-4b5a-6978-8897-a6b5c4d3e2f1",
              "categories": {"location": "Remote"}, "createdAt": 1793836800000,
              "descriptionPlain": "We will not sponsor visas.", "additionalPlain": "", "lists": []}]
    ASHBY = {"jobs": [{"title": "Business Intelligence Analyst", "jobUrl": "https://jobs.ashbyhq.com/acme/11111111-2222-3333-4444-555555555555",
                       "location": "Remote", "publishedAt": "2026-11-07T00:00:00Z", "isListed": True,
                       "descriptionPlain": "Silent about visas."},
                      {"title": "Data Analyst", "jobUrl": "https://jobs.ashbyhq.com/acme/unlisted", "isListed": False}]}

    def fake(self, url):
        if "greenhouse" in url:
            return self.GH
        if "lever" in url:
            return self.LEVER
        if "ashby" in url:
            return self.ASHBY
        raise OSError("boom")

    def cfg(self):
        return {"max_age_days": 14, "title_positive": ["Analyst", "Analytics Engineer"],
                "title_negative": ["Intern"], "companies": [
                    {"name": "Acme GH", "ats": "greenhouse", "slug": "acme"},
                    {"name": "Acme Lever", "ats": "lever", "slug": "acme"},
                    {"name": "Acme Ashby", "ats": "ashby", "slug": "acme"},
                    {"name": "Down", "ats": "ashby", "slug": "down2"}]}

    def test_scan_filters_titles_age_unlisted_and_isolates_errors(self):
        from datetime import datetime, timezone
        from scanners.ats_scan import scan
        # fetcher fails only for the 'down2' slug
        f = lambda u: (_ for _ in ()).throw(OSError("boom")) if "down2" in u else self.fake(u)
        jobs, errors = scan(self.cfg(), f, today=datetime(2026, 11, 9, tzinfo=timezone.utc))
        titles = sorted(j["title"] for j in jobs)
        self.assertEqual(titles, ["Analytics Engineer", "Business Intelligence Analyst",
                                  "Product Analyst", "Senior Data Analyst"])
        self.assertEqual(len(errors), 1)
        gh = next(j for j in jobs if j["title"] == "Senior Data Analyst")
        self.assertIn("H1B", gh["jd"])
        self.assertNotIn("<p>", gh["jd"])
        self.assertEqual(gh["posted"], "2026-11-05")

    def test_scan_cli_gates_and_skips(self):
        import io, contextlib
        from datetime import datetime, timezone
        import scanners.ats_scan as mod
        real = mod.scan
        mod.scan = lambda cfg: real(cfg, self.fake, today=datetime(2026, 11, 9, tzinfo=timezone.utc))
        try:
            with tempfile.TemporaryDirectory() as d:
                cfgp = os.path.join(d, "c.json")
                cfg = self.cfg(); cfg["companies"] = cfg["companies"][:3]
                with open(cfgp, "w") as fh:
                    json.dump(cfg, fh)
                qp = os.path.join(d, "data", "jobs.jsonl")
                buf = io.StringIO()
                with contextlib.redirect_stdout(buf):
                    main(["--queue", qp, "scan", "--config", cfgp])
                stats = json.loads(buf.getvalue().strip().splitlines()[-1])
                self.assertEqual((stats["new"], stats["blocked"], stats["gated"]), (4, 1, 3))
                q = Queue(qp)
                by = {j["title"]: j for j in q.jobs.values()}
                self.assertEqual(by["Product Analyst"]["stage"], "skipped")
                self.assertEqual(by["Senior Data Analyst"]["sponsorship"], "OK_SPONSORS")
                self.assertEqual(by["Analytics Engineer"]["sponsorship"], "LONG_TERM_RISK")
                self.assertTrue(os.path.exists(by["Senior Data Analyst"]["jd_file"]))
                buf2 = io.StringIO()
                with contextlib.redirect_stdout(buf2):
                    main(["--queue", qp, "scan", "--config", cfgp])
                self.assertEqual(json.loads(buf2.getvalue().strip().splitlines()[-1])["new"], 0)  # idempotent
        finally:
            mod.scan = real


class Discover(unittest.TestCase):
    def test_slug_candidates(self):
        from scanners.discover import slug_candidates
        self.assertEqual(slug_candidates("Instacart, Inc."), ["instacart"])
        self.assertIn("fidelityinvestments", slug_candidates("Fidelity Technology Group, LLC d/b/a Fidelity Investments"))
        self.assertNotIn("the", slug_candidates("The Home Depot USA Inc"))
        self.assertNotIn("capital", slug_candidates("Capital One Services, LLC"))  # too generic

    def test_pick_direct_sponsors_excludes_staffing_and_stale(self):
        from scanners.discover import pick_direct_sponsors
        rows = [{"n": "Good Co", "ly": 2026, "filed": 100, "sh": 0.0},
                {"n": "Body Shop", "ly": 2026, "filed": 900, "sh": 0.95},
                {"n": "Old Co", "ly": 2022, "filed": 100, "sh": 0.0},
                {"n": "Tiny Co", "ly": 2026, "filed": 3, "sh": 0.0}]
        self.assertEqual([r["n"] for r in pick_direct_sponsors(rows)], ["Good Co"])

    def test_discover_survives_errors_and_reports_matches(self):
        from scanners.discover import discover
        gh = {"jobs": [{"title": "Data Analyst", "absolute_url": "https://x/1", "location": {"name": "R"},
                        "first_published": "2026-11-01", "content": ""}]}
        def fake(url):
            if "/boards/goodco/" in url:
                return gh
            raise OSError("timeout")
        rows = [{"n": "Goodco, Inc.", "ly": 2026, "filed": 100, "perm": 5, "sh": 0.0},
                {"n": "Ghost Corp", "ly": 2026, "filed": 90, "perm": 0, "sh": 0.0}]
        res = discover(rows, ["Analyst"], [], fetcher=fake, workers=2)
        self.assertEqual(len(res), 1)
        self.assertEqual((res[0]["ats"], res[0]["slug"], res[0]["matches"]), ("greenhouse", "goodco", ["Data Analyst"]))


class Priority(unittest.TestCase):
    def test_tiers_and_rules(self):
        from pipeline.priority import history_tier, priority
        self.assertEqual(history_tier(1819, 475), "STRONG")
        self.assertEqual(history_tier(150, 0), "MODERATE")
        self.assertEqual(history_tier(None, None), "NONE")
        self.assertEqual(priority("UNKNOWN", "STRONG"), "HIGH")
        self.assertEqual(priority("UNKNOWN", "NONE"), "LOW")
        self.assertEqual(priority("OK_SPONSORS", "STRONG"), "TOP")
        self.assertEqual(priority("LONG_TERM_RISK", "STRONG"), "LOW")   # explicit refusal beats history
        self.assertEqual(priority("BLOCK", "STRONG"), "SKIP")
        self.assertEqual(priority("UNKNOWN", "STRONG", ["STAFFING_RISK"]), "MEDIUM")

    def test_scan_records_history_and_priority(self):
        from datetime import datetime, timezone
        import scanners.ats_scan as mod
        real = mod.scan
        gh = {"jobs": [{"title": "Data Analyst", "absolute_url": "https://job-boards.greenhouse.io/acme/jobs/9",
                        "location": {"name": "R"}, "first_published": "2026-11-05", "content": "Silent."}]}
        mod.scan = lambda cfg: real(cfg, lambda u: gh, today=datetime(2026, 11, 9, tzinfo=timezone.utc))
        try:
            with tempfile.TemporaryDirectory() as d:
                cfgp = os.path.join(d, "c.json")
                with open(cfgp, "w") as fh:
                    json.dump({"title_positive": ["Analyst"], "companies": [
                        {"name": "Acme", "ats": "greenhouse", "slug": "acme", "filed": 1800, "perm": 400}]}, fh)
                qp = os.path.join(d, "jobs.jsonl")
                main(["--queue", qp, "scan", "--config", cfgp])
                rec = next(iter(Queue(qp).jobs.values()))
                self.assertEqual((rec["h1b_history"], rec["priority"]), ("STRONG", "HIGH"))
        finally:
            mod.scan = real


FIX = os.path.join(os.path.dirname(__file__), "fixtures", "pipeline.sample.md")


class CareerOpsAdapter(unittest.TestCase):
    def setUp(self):
        from adapters.career_ops import parse_pipeline
        with open(FIX) as fh:
            self.text = fh.read()
        self.rows = {r["url"].rstrip("/").split("/")[-1].split("?")[0]: r for r in parse_pipeline(self.text)}

    def test_pending_with_location_and_posted(self):
        r = self.rows["4723591006"]
        self.assertEqual((r["employer"], r["title"], r["posted"]), ("Zip Co", "Product Analyst", "2026-10-27"))
        self.assertEqual(r["extra"]["location"], "Remote - US")
        self.assertEqual(r["stage"], "found")

    def test_title_with_comma_and_yrs(self):
        r = self.rows["8115834"]
        self.assertEqual(r["title"], "Insights Lead, Instacart Business")
        self.assertEqual(r["extra"]["yrs"], "5+")

    def test_trust_segment_not_taken_as_location(self):
        r = self.rows["0f1e2d3c-4b5a-6978-8897-a6b5c4d3e2f1"]
        self.assertNotIn("location", r["extra"])
        self.assertTrue(r["extra"]["trust"].startswith("60"))

    def test_bare_url_row_and_comp_and_rank(self):
        self.assertEqual(self.rows["550665"]["employer"], "")
        a = self.rows["C1A38B9608"]
        self.assertEqual(a["score"], 3.0)
        self.assertEqual(a["extra"]["comp"], "$90,000-$110,000")
        self.assertEqual(a["extra"]["location"], "Remote")

    def test_processed_expired_prescreen_and_unfetched(self):
        self.assertEqual(self.rows["7516411003"]["stage"], "verified")
        self.assertEqual(self.rows["7516411003"]["score"], 3.4)
        self.assertEqual(self.rows["999"]["stage"], "skipped")
        self.assertEqual(self.rows["aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee"]["stage"], "skipped")
        self.assertNotIn("broken-link", self.rows)

    def test_ingest_dedupes_against_jobright_and_never_downgrades(self):
        from adapters.career_ops import ingest
        with tempfile.TemporaryDirectory() as d:
            q = Queue(os.path.join(d, "jobs.jsonl"))
            q.add(url="https://job-boards.greenhouse.io/zipcolimited/jobs/4723591006",
                  employer="Zip", title="Product Analyst", source="jobright", source_score=72)
            applied, _ = q.add(url="https://boards.greenhouse.io/oldco/jobs/999",
                               employer="OldCo", title="Analyst", source="jobright")
            q.advance(applied["key"], "applied")
            counts = ingest(q, self.text)
            zip_rec = q.jobs[canonical_key("https://boards.greenhouse.io/zipcolimited/jobs/4723591006")]
            self.assertEqual(sorted(zip_rec["sources"]), ["career-ops", "jobright"])
            self.assertEqual(q.jobs[applied["key"]]["stage"], "applied")  # expiry must not downgrade
            self.assertEqual(counts["ignored"], 1)  # the [!] row
            again = ingest(q, self.text)
            self.assertEqual(again["added"], 0)  # idempotent


if __name__ == "__main__":
    unittest.main()
