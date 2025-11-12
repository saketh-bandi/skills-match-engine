# backend/app.py
from fastapi import FastAPI
from pydantic import BaseModel
from backend.skills import extract_skills
from backend.jd_parser import analyze_jd
from backend.scorer import compute_score

app = FastAPI()

class TextReq(BaseModel):
    text: str

class MatchReq(BaseModel):
    resume_text: str
    jd_text: str

@app.post("/analyze/skills")
def analyze_skills(req: TextReq):
    return {"skills": extract_skills(req.text)}

@app.post("/match")
def match(req: MatchReq):
    user = extract_skills(req.resume_text)
    jd = analyze_jd(req.jd_text)
    score, components, present, missing = compute_score(user, jd)
    # convert missing to a compact view + impact label
    def impact_label(w: float) -> str:
        if w >= 2.0: return "high"
        if w >= 1.0: return "medium"
        return "low"
    missing_view = [{"skill": m["skill"], "section": m["section"], "impact": impact_label(m["weight"])} for m in missing]

    return {
        "match_score": round(score, 4),
        "present_skills": present,
        "missing_skills": missing_view,
        "components": components,
        "jd_skills_by_section": jd,  # transparency for debugging
    }

@app.get("/")
def root():
    return {"message": "skills-match-engine API is alive"}
