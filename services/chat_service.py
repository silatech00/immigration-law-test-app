import json
import re

from config import COUNTRY_RULES_PATH
from llm_client import chat_completion
from models.user_profile import UserProfile

SYSTEM_PROMPT = """You are Immigration Law AI, an assistant specializing in immigration law worldwide.

Help users understand visa types, eligibility requirements, application processes, and general immigration rules across countries.

Rules:
- Provide clear, practical guidance based on publicly known immigration frameworks.
- When laws vary by nationality or situation, explain the main options and caveats.
- Do not claim to be a licensed lawyer. Encourage users to consult official government sources or qualified counsel for binding advice.
- If information may be outdated, say so and suggest checking the relevant embassy or immigration authority website.
"""


def load_country_context(country: str) -> str:
    if not COUNTRY_RULES_PATH.exists():
        return ""
    rules = json.loads(COUNTRY_RULES_PATH.read_text(encoding="utf-8"))
    entry = rules.get(country)
    if not entry:
        return ""
    visas = ", ".join(entry.get("common_visas", []))
    return f"{country}: {entry.get('summary', '')} Common visas: {visas}."


def build_profile_context(profile: UserProfile) -> str:
    parts = []
    if profile.current_country:
        parts.append(f"Current country: {profile.current_country}")
    if profile.destination_country:
        parts.append(f"Destination: {profile.destination_country}")
    if profile.nationality:
        parts.append(f"Nationality: {profile.nationality}")
    if profile.visa_type:
        parts.append(f"Visa type of interest: {profile.visa_type}")
    if profile.passport_number:
        parts.append(f"Passport number: {profile.passport_number}")
    if profile.ethnicity:
        parts.append(f"Ethnicity: {profile.ethnicity}")
    if profile.criminal_record:
        parts.append(f"Criminal record notes: {profile.criminal_record}")
    if profile.social_security_number:
        parts.append(f"Social security number: {profile.social_security_number}")
    if profile.current_latitude is not None and profile.current_longitude is not None:
        parts.append(
            f"Current location: {profile.current_latitude}, {profile.current_longitude}"
        )
    return "\n".join(parts)


def ask(
    user_message: str,
    history: list[dict[str, str]],
    profile: UserProfile,
) -> str:
    country_hint = load_country_context(profile.destination_country)
    profile_context = build_profile_context(profile)

    system_parts = [SYSTEM_PROMPT]
    if country_hint:
        system_parts.append(f"Reference context:\n{country_hint}")
    if profile_context:
        system_parts.append(f"User profile:\n{profile_context}")

    messages: list[dict[str, str]] = [
        {"role": "system", "content": "\n\n".join(system_parts)},
        *history,
        {"role": "user", "content": user_message},
    ]
    return chat_completion(messages)
