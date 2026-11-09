"""Priority ranking: posting text + employer H-1B filing history.

Evidence tiers come from DOL-derived counts (company level, not role level):
  STRONG    >= 500 LCAs filed and >= 100 PERM (green card) filings
  MODERATE  >= 100 LCAs filed
  WEAK      some history below that
  NONE      no history supplied
Rules (a posting that explicitly refuses always wins over history):
  BLOCK            -> SKIP
  LONG_TERM_RISK   -> LOW
  OK_SPONSORS      -> TOP if history STRONG/MODERATE else HIGH
  UNKNOWN          -> HIGH if STRONG, MEDIUM if MODERATE, else LOW
STAFFING_RISK flag drops one level (STEM OPT needs direct employment).
"""
from __future__ import annotations

ORDER = ["TOP", "HIGH", "MEDIUM", "LOW", "SKIP"]


def history_tier(filed: int | None, perm: int | None) -> str:
    if not filed:
        return "NONE"
    if filed >= 500 and (perm or 0) >= 100:
        return "STRONG"
    if filed >= 100:
        return "MODERATE"
    return "WEAK"


def priority(verdict: str, tier: str, flags: list[str] | None = None) -> str:
    if verdict == "BLOCK":
        return "SKIP"
    if verdict == "LONG_TERM_RISK":
        level = "LOW"
    elif verdict == "OK_SPONSORS":
        level = "TOP" if tier in ("STRONG", "MODERATE") else "HIGH"
    else:
        level = {"STRONG": "HIGH", "MODERATE": "MEDIUM"}.get(tier, "LOW")
    if flags and "STAFFING_RISK" in flags and level in ORDER[:-2]:
        level = ORDER[ORDER.index(level) + 1]
    return level
