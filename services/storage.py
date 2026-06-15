import json
import sqlite3
from pathlib import Path

from config import DB_PATH, ROOT_DIR
from models.user_profile import EligibilityResult, UserProfile

SCHEMA_PATH = ROOT_DIR / "schema.sql"


def _connect() -> sqlite3.Connection:
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db() -> None:
    schema = SCHEMA_PATH.read_text(encoding="utf-8")
    with _connect() as conn:
        conn.executescript(schema)


def save_profile(profile: UserProfile) -> None:
    with _connect() as conn:
        conn.execute(
            """
            INSERT INTO user_profiles (
                session_id, passport_number, nationality, ethnicity,
                criminal_record, social_security_number,
                current_latitude, current_longitude,
                destination_country, current_country, visa_type, updated_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, datetime('now'))
            ON CONFLICT(session_id) DO UPDATE SET
                passport_number = excluded.passport_number,
                nationality = excluded.nationality,
                ethnicity = excluded.ethnicity,
                criminal_record = excluded.criminal_record,
                social_security_number = excluded.social_security_number,
                current_latitude = excluded.current_latitude,
                current_longitude = excluded.current_longitude,
                destination_country = excluded.destination_country,
                current_country = excluded.current_country,
                visa_type = excluded.visa_type,
                updated_at = datetime('now')
            """,
            (
                profile.session_id,
                profile.passport_number,
                profile.nationality,
                profile.ethnicity,
                profile.criminal_record,
                profile.social_security_number,
                profile.current_latitude,
                profile.current_longitude,
                profile.destination_country,
                profile.current_country,
                profile.visa_type,
            ),
        )


def load_profile(session_id: str) -> UserProfile | None:
    with _connect() as conn:
        row = conn.execute(
            "SELECT * FROM user_profiles WHERE session_id = ?",
            (session_id,),
        ).fetchone()
    if row is None:
        return None
    return UserProfile.from_row(dict(row))


def save_message(session_id: str, role: str, content: str) -> None:
    with _connect() as conn:
        conn.execute(
            "INSERT INTO chat_messages (session_id, role, content) VALUES (?, ?, ?)",
            (session_id, role, content),
        )


def load_messages(session_id: str) -> list[dict[str, str]]:
    with _connect() as conn:
        rows = conn.execute(
            "SELECT role, content FROM chat_messages WHERE session_id = ? ORDER BY id",
            (session_id,),
        ).fetchall()
    return [{"role": row["role"], "content": row["content"]} for row in rows]


def save_eligibility(
    session_id: str,
    destination_country: str,
    result: EligibilityResult,
) -> None:
    with _connect() as conn:
        conn.execute(
            """
            INSERT INTO eligibility_assessments (
                session_id, destination_country,
                visa_eligibility_score, recommended_visa_type,
                automated_recommendation, risk_flags
            ) VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                session_id,
                destination_country,
                result.visa_eligibility_score,
                result.recommended_visa_type,
                result.automated_recommendation,
                json.dumps(result.risk_flags),
            ),
        )
