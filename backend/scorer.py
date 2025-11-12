# backend/scorer.py
from typing import Dict, Tuple

# Transparent, adjustable weights
WEIGHTS = {
    "requirements": 2.0,
    "preferred": 1.2,
    "responsibilities": 0.6,
    "other": 0.5,
}

def compute_score(
    user_skills: Dict[str, float],
    jd_skills_by_section: Dict[str, Dict[str, float]]
) -> Tuple[float, Dict, list[str], list[dict]]:
    """
    Returns (score, components, present_skills, missing_list)
    where missing_list = [{skill, section, weight}]
    """
    present = 0.0
    missing = 0.0
    present_skills = set()
    missing_list = []

    for section, skills in jd_skills_by_section.items():
        w = WEIGHTS.get(section, WEIGHTS["other"])
        for skill in skills.keys():
            if skill in user_skills:
                present += w
                present_skills.add(skill)
            else:
                missing += w
                missing_list.append({"skill": skill, "section": section, "weight": w})

    denom = present + missing
    score = present / denom if denom > 0 else 0.0

    components = {
        "present_weight": present,
        "missing_weight": missing,
        "weights": WEIGHTS,
    }
    # sort missing by impact (weight desc, then alpha)
    missing_list.sort(key=lambda x: (-x["weight"], x["skill"]))
    return score, components, sorted(present_skills), missing_list
