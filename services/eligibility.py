import re

from llm_client import chat_completion
from models.user_profile import EligibilityResult, UserProfile
from services.chat_service import SYSTEM_PROMPT, build_profile_context, load_country_context


def _parse_score(text: str) -> float:
    match = re.search(r"(\d{1,3})(?:\.\d+)?\s*(?:%|/100|out of 100)?", text)
    if match:
        value = float(match.group(1))
        return min(max(value, 0.0), 100.0)
    return 50.0


def check_eligibility(profile: UserProfile) -> EligibilityResult:
    country = profile.destination_country or "Unknown"
    country_hint = load_country_context(country)
    profile_context = build_profile_context(profile)

    prompt = f"""Assess visa eligibility for immigration to {country}.

User profile:
{profile_context or "No profile details provided."}

Reference:
{country_hint or "No country-specific reference available."}

Respond in this exact format:
SCORE: <number 0-100>
VISA: <recommended visa type>
RECOMMENDATION: <2-4 sentence automated recommendation>
RISKS: <comma-separated risk flags, or "none">

Be realistic. Lower the score if criminal_record is present or key details are missing."""

    raw = chat_completion(
        [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt},
        ],
        temperature=0.2,
    )

    score = _parse_score(raw)
    visa_match = re.search(r"VISA:\s*(.+)", raw, re.IGNORECASE)
    rec_match = re.search(r"RECOMMENDATION:\s*(.+)", raw, re.IGNORECASE | re.DOTALL)
    risk_match = re.search(r"RISKS:\s*(.+)", raw, re.IGNORECASE)

    recommended_visa = visa_match.group(1).strip() if visa_match else "General visitor/work visa"
    recommendation = rec_match.group(1).strip().split("\n")[0] if rec_match else raw.strip()
    risk_text = risk_match.group(1).strip() if risk_match else "none"
    risk_flags = [r.strip() for r in risk_text.split(",") if r.strip().lower() != "none"]

    return EligibilityResult(
        visa_eligibility_score=score,
        recommended_visa_type=recommended_visa,
        automated_recommendation=recommendation,
        risk_flags=risk_flags,
    )
