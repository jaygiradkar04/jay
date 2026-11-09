# career-pipeline

One queue, two discovery sources, one honest tailoring step, human Submit.

```
 JobRight (PostingFinder, read-only) ─┐
                                      ├─► data/jobs.jsonl ─► verify on employer ATS
 career-ops scan (ATS APIs) ──────────┘     (deduped by         │
                                             ATS job id)        ▼
                                                      sponsorship gate (STEM OPT)
                                                      BLOCK -> skipped
                                                               │
                                                               ▼
                                         ResumePerfector (no fabricated claims)
                                                               │
                                       career-ops `apply` prefills, stops at Submit
                                                               │
                                                        YOU press Submit
```

## Why keep JobRight
It surfaces companies you did not list in career-ops. But its freshness labels
and scores are unreliable, so it only *nominates*; the employer page decides.

## Commands (Python 3, standard library only)
```bash
python3 -m pipeline.cli scan                      # cloud-safe: public ATS APIs -> gate -> queue
python3 -m pipeline.cli ingest-career-ops ~/career-ops/data/pipeline.md   # career-ops inbox
python3 -m pipeline.cli import jobs.json          # bulk add (e.g. JobRight scrape)
python3 -m pipeline.cli add --url URL --employer E --title T --source manual
python3 -m pipeline.cli gate <key> --jd-file jd.txt
python3 -m pipeline.cli list --stage gated
python3 -m pipeline.cli package                   # hand-off text for ResumePerfector
python3 -m unittest discover -s tests
```
Stages: `found -> verified -> gated -> tailored -> applied | skipped`.

## Cloud scanning
`scan` reads `config/companies.json` (copy `config/companies.example.json`):
Greenhouse, Lever and Ashby boards, title filter, max age. It uses urllib, so
it honors the sandbox proxy and talks only to fixed public API hosts. career-ops'
own `scan.mjs` bypasses a proxy-only sandbox unless you set
`CAREER_OPS_TRUST_PROXY_EGRESS=1` (only safe if the proxy blocks private
addresses), so the cloud path uses this scanner instead. Postings from an
employer board are live by construction; each description is saved under
`data/jds/` and gated immediately (BLOCK -> `skipped`, otherwise `gated`).
Workable and other ATSs are not covered yet.

## STEM OPT notes (not legal advice; confirm with your DSO)
- The employer must be enrolled in E-Verify and complete an I-983 training
  plan. The gate flags when a posting does not mention E-Verify; check the
  employer on the e-verify.gov search yourself.
- Staffing/consulting/client-site roles usually break the direct-employer
  requirement. They are flagged `STAFFING_RISK`, not auto-rejected.
- `LONG_TERM_RISK` means you can work during STEM OPT but have no H-1B path.
- The gate is a text heuristic. It will miss unusual phrasing; read the
  evidence snippets it prints.

## Install career-ops (on your machine)
```bash
npx @santifer/career-ops init
```
Then run `ingest-career-ops` on its `data/pipeline.md`. The adapter is
read-only on career-ops files, idempotent, and maps: pending -> `found`,
evaluated (`n/5`) -> `verified`, expired/pre-screen-skipped -> `skipped`.
It never downgrades a job you already tailored or applied to. A bare-URL row
(no company/title yet) is kept; its employer fills in once career-ops
evaluates it. `tests/fixtures/pipeline.sample.md` was generated with
career-ops' own `formatPipelineOffer`.
Keep `portals.yml` pointed at employers known to sponsor.
Never commit `data/` or your resume; both are gitignored/personal.

## Not built yet
- Auto-fetching H-1B employer history (USCIS Employer Data Hub CSV lookup).
- Reading career-ops evaluation reports (`reports/`) and the tracker for richer scores.
- Scheduling the scan.
