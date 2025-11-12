# backend/skills.py
import yaml
import re
from pathlib import Path

SKILLS_PATH = Path(__file__).resolve().parent.parent / "data" / "skills.yaml"

if not SKILLS_PATH.exists():
    raise FileNotFoundError(f"Missing skills taxonomy at: {SKILLS_PATH}. Create data/skills.yaml")

with open(SKILLS_PATH, "r") as f:
    RAW_SKILLS = yaml.safe_load(f) or {}

if not isinstance(RAW_SKILLS, dict) or not RAW_SKILLS:
    raise ValueError(f"skills.yaml is empty or malformed at {SKILLS_PATH}")

ALL_SKILLS = {s.lower() for group in RAW_SKILLS.values() for s in group}

ALIASES = {
    "py": "python",
    "python3": "python",
    "sklearn": "scikit-learn",
    "tf": "tensorflow",
    "js": "javascript",
}

def normalize_tokens(text: str) -> str:
    text = text.lower()
    text = re.sub(r"[^a-z0-9+.# ]", " ", text)
    tokens = text.split()
    tokens = [ALIASES.get(t, t) for t in tokens]
    return " ".join(tokens)

def extract_skills(text: str) -> dict[str, float]:
    clean = normalize_tokens(text)
    found = {}
    for skill in ALL_SKILLS:
        if skill in clean:
            found[skill] = 1.0
    return found

if __name__ == "__main__":
    print(extract_skills("Python3, AWS, C++, Pandas, and REST API"))
