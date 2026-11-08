"""Sponsorship / work-authorization gate for an F-1 STEM OPT candidate.

This is a text heuristic over a job description, not legal advice. Anything
that matters (E-Verify enrollment, I-983 training plan, third-party
placement) must be confirmed with the employer and your DSO.

Verdicts, worst to best:
  BLOCK            cannot take this job on STEM OPT (citizen/clearance/ITAR only,
                   or explicitly refuses OPT/CPT/F-1)
  LONG_TERM_RISK   will not sponsor a visa now or in the future; you can work
                   during STEM OPT but there is no path to H-1B
  UNKNOWN          posting is silent; check E-Verify and sponsorship history
  OK_SPONSORS      posting says the employer sponsors or transfers visas

Flags (independent of verdict):
  STAFFING_RISK    consulting / staffing / client-site / C2C wording. STEM OPT
                   needs a bona fide employer-employee relationship and an
                   I-983 plan, which third-party placement generally breaks.
  E_VERIFY         posting mentions E-Verify (good sign for STEM OPT)
"""
from __future__ import annotations

import re

BLOCK, LONG_TERM_RISK, UNKNOWN, OK_SPONSORS = (
    "BLOCK", "LONG_TERM_RISK", "UNKNOWN", "OK_SPONSORS")

_BLOCK = [
    r"u\.?s\.? citizens? only",
    r"must be (?:a )?u\.?s\.? citizen",
    r"u\.?s\.? citizenship (?:is )?required",
    r"(?:citizens?|green card holders?) (?:or|and) (?:permanent residents?|green card holders?) only",
    r"(?:active )?(?:secret|top secret|ts/sci) (?:security )?clearance",
    r"security clearance (?:is )?required",
    r"\bitar\b",
    r"export[- ]control(?:led)?",
    r"(?:no|not (?:accept(?:ing)?|consider(?:ing)?)|unable to (?:accept|consider)) (?:\w+ )?(?:opt|cpt|f-?1|stem opt)\b",
    r"\bopt\b[^.]{0,30}\bnot (?:accepted|eligible|considered)",
]
_NO_SPONSOR = [
    r"(?:no|not|unable to|cannot|can't|won't|will not|do not|does not|don't|doesn't) (?:\w+ ){0,3}(?:provide |offer |support )?(?:visa )?sponsor(?:ship)?",
    r"without (?:the need for )?(?:visa )?sponsorship",
    r"sponsorship (?:is )?(?:not|unavailable)",
    r"not (?:currently )?(?:able|eligible|willing) to sponsor",
    r"(?:now or )?in the future[^.]{0,40}sponsor",
]
_SPONSORS = [
    r"(?:we |will |can |able to |do )(?:offer |provide |support |consider )?(?:visa )?sponsor(?:ship)?\b",
    r"\bh-?1b\b[^.]{0,40}(?:transfer|sponsor|support|welcome)",
    r"visa (?:sponsorship )?(?:is )?(?:available|provided|offered)",
    r"open to (?:sponsoring|visa)",
    r"stem opt (?:friendly|welcome|eligible)",
]
_STAFFING = [
    r"staffing (?:firm|agency|company)",
    r"\bc2c\b|corp[- ]to[- ]corp",
    r"w-?2 only|\bw2 only\b",
    r"client[- ]site",
    r"third[- ]party (?:placement|client)",
    r"our (?:end )?clients?\b",
    r"\bconsulting (?:firm|services|company)\b",
    r"contract(?:[- ]to[- ]hire)?\s+(?:position|role|opportunity)",
]
_EVERIFY = [r"e-?verify"]


def _hits(patterns: list[str], text: str) -> list[str]:
    out: list[str] = []
    for p in patterns:
        for m in re.finditer(p, text, flags=re.I):
            s = max(0, m.start() - 40)
            out.append(text[s:m.end() + 40].replace("\n", " ").strip())
            break  # one snippet per pattern is enough
    return out


def classify(jd_text: str, employer: str = "") -> dict:
    """Return {verdict, reasons, flags, evidence} for a job description."""
    text = re.sub(r"\s+", " ", jd_text or "")
    flags: list[str] = []
    evidence: dict[str, list[str]] = {}

    staffing = _hits(_STAFFING, text)
    if staffing or re.search(r"\b(staffing|consulting|solutions inc)\b", employer, re.I):
        flags.append("STAFFING_RISK")
        evidence["staffing"] = staffing
    ev = _hits(_EVERIFY, text)
    if ev:
        flags.append("E_VERIFY")
        evidence["e_verify"] = ev

    block = _hits(_BLOCK, text)
    no_sp = _hits(_NO_SPONSOR, text)
    sponsors = [s for s in _hits(_SPONSORS, text)
                if not any(s in n or n in s for n in no_sp)]

    if block:
        verdict, reasons = BLOCK, ["Posting requires citizenship/clearance/ITAR or refuses OPT/F-1."]
        evidence["block"] = block
    elif no_sp:
        verdict, reasons = LONG_TERM_RISK, ["Posting refuses sponsorship; usable for STEM OPT only, no H-1B path."]
        evidence["no_sponsorship"] = no_sp
    elif sponsors:
        verdict, reasons = OK_SPONSORS, ["Posting says the employer sponsors or supports visas."]
        evidence["sponsors"] = sponsors
    else:
        verdict, reasons = UNKNOWN, ["Posting is silent on sponsorship; verify employer E-Verify status and H-1B history."]

    if "STAFFING_RISK" in flags:
        reasons.append("Staffing/consulting/client-site wording: confirm direct employment and an I-983 plan.")
    if "E_VERIFY" not in flags and verdict != BLOCK:
        reasons.append("E-Verify not mentioned: STEM OPT requires an E-Verify employer, check e-verify.gov search.")
    return {"verdict": verdict, "reasons": reasons, "flags": flags, "evidence": evidence}
