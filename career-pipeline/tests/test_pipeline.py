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


if __name__ == "__main__":
    unittest.main()
