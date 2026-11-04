# Job search

Pulls open roles from Greenhouse / Lever / Ashby boards for the companies in `companies.json`,
filters them using `config.json`, and prints only postings not seen on earlier runs.

    python3 job_search/search.py          # new postings only; appends to new_jobs.csv
    python3 job_search/search.py --all    # everything matching, ignore seen-state
    python3 job_search/search.py --reset  # forget seen-state

- Add companies to `companies.json` (`ats` = greenhouse | lever | ashby, `slug` = the board name in the job-board URL).
- Edit `config.json` for title/location keywords, "no sponsorship" phrases to drop, and max posting age.
- Only companies you list are searched, so build the list from known H-1B sponsors (USCIS H-1B Employer Data Hub).
- The filter drops postings that say they won't sponsor, but it can't confirm that a company does sponsor.
