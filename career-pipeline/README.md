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
python3 -m pipeline.cli import jobs.json          # bulk add from either source
python3 -m pipeline.cli add --url URL --employer E --title T --source manual
python3 -m pipeline.cli gate <key> --jd-file jd.txt
python3 -m pipeline.cli list --stage gated
python3 -m pipeline.cli package                   # hand-off text for ResumePerfector
python3 -I -m unittest discover -s tests
```
Stages: `found -> verified -> gated -> tailored -> applied | skipped`.

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
Then export its scan results as a JSON list of
`{url, employer, title, source: "career-ops", score}` and `import` them.
Keep `portals.yml` pointed at employers known to sponsor.
Never commit `data/` or your resume; both are gitignored/personal.

## Not built yet
- Auto-fetching H-1B employer history (USCIS Employer Data Hub CSV lookup).
- A career-ops export adapter (needs the real output format from your install).
- Scheduling the scan.
