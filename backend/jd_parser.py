# backend/jd_parser.py
import re
from typing import Dict, List
from backend.skills import extract_skills, normalize_tokens

SECTION_ALIASES = {
    "requirements": ["requirements", "minimum qualifications", "must have", "basic qualifications"],
    "preferred": ["preferred", "nice to have", "bonus", "preferred qualifications"],
    "responsibilities": ["responsibilities", "what you'll do", "about the role", "job duties"],
}

HEADER_PATTERN = re.compile(r"^\s*[-•*]?\s*(.+):\s*$")  # lines ending with ":" often are headers

def _which_section(header: str) -> str | None:
    h = header.lower().strip()
    for sec, keys in SECTION_ALIASES.items():
        if any(k in h for k in keys):
            return sec
    return None

def split_sections(jd_text: str) -> Dict[str, str]:
    """
    Heuristic: walk the JD line-by-line; whenever a header-like line appears,
    assign following lines to that section until the next header.
    """
    lines = jd_text.splitlines()
    current = None
    buckets = {"requirements": [], "preferred": [], "responsibilities": [], "other": []}

    for raw in lines:
        line = raw.strip()
        if not line:
            continue
        # explicit bullets count as content, but header lines end with ':'
        if HEADER_PATTERN.match(line):
            sec = _which_section(line[:-1])  # strip trailing ':'
            current = sec if sec else "other"
            continue
        # accumulate
        buckets[current or "other"].append(line)

    # Fallbacks: if nothing explicitly classified, assume entire text are "requirements"
    if not any(buckets.values()) or all(len(v) == 0 for v in buckets.values()):
        return {"requirements": jd_text}

    return {k: "\n".join(v) for k, v in buckets.items() if v}

def analyze_jd(jd_text: str) -> Dict[str, Dict[str, float]]:
    """
    Return skills by section: {section: {skill: confidence}}
    """
    sections = split_sections(jd_text)
    out: Dict[str, Dict[str, float]] = {}
    for sec, txt in sections.items():
        out[sec] = extract_skills(txt)
    return out
