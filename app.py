import json
import uuid

import streamlit as st

from config import COUNTRY_RULES_PATH
from models.user_profile import UserProfile
from services import chat_service, eligibility, storage

COUNTRIES = sorted(json.loads(COUNTRY_RULES_PATH.read_text(encoding="utf-8")).keys())

st.set_page_config(page_title="Immigration Law AI", page_icon="🌍", layout="wide")

storage.init_db()


def _session_id() -> str:
    if "session_id" not in st.session_state:
        st.session_state.session_id = str(uuid.uuid4())
    return st.session_state.session_id


def _load_history() -> list[dict[str, str]]:
    if "messages" not in st.session_state:
        st.session_state.messages = storage.load_messages(_session_id())
    return st.session_state.messages


def _sidebar_profile() -> UserProfile:
    sid = _session_id()
    existing = storage.load_profile(sid)

    with st.sidebar:
        st.header("Your profile")
        st.caption("Optional details help tailor immigration guidance.")

        destination_country = st.selectbox(
            "Destination country",
            [""] + COUNTRIES,
            index=(
                COUNTRIES.index(existing.destination_country) + 1
                if existing and existing.destination_country in COUNTRIES
                else 0
            ),
        )
        current_country = st.selectbox(
            "Current country",
            [""] + COUNTRIES,
            index=(
                COUNTRIES.index(existing.current_country) + 1
                if existing and existing.current_country in COUNTRIES
                else 0
            ),
        )
        nationality = st.text_input(
            "Nationality",
            value=existing.nationality if existing else "",
        )
        visa_type = st.text_input(
            "Visa type of interest",
            value=existing.visa_type if existing else "",
            placeholder="e.g. Skilled Worker, H-1B",
        )
        passport_number = st.text_input(
            "Passport number",
            value=existing.passport_number if existing else "",
        )
        ethnicity = st.text_input(
            "Ethnicity",
            value=existing.ethnicity if existing else "",
        )
        criminal_record = st.text_area(
            "Criminal record (if any)",
            value=existing.criminal_record if existing else "",
            height=80,
        )
        social_security_number = st.text_input(
            "Social security number",
            value=existing.social_security_number if existing else "",
        )

        col1, col2 = st.columns(2)
        with col1:
            current_latitude = st.number_input(
                "Current latitude",
                value=float(existing.current_latitude) if existing and existing.current_latitude else 0.0,
                format="%.6f",
            )
        with col2:
            current_longitude = st.number_input(
                "Current longitude",
                value=float(existing.current_longitude) if existing and existing.current_longitude else 0.0,
                format="%.6f",
            )

        if st.button("Save profile", use_container_width=True):
            profile = UserProfile(
                session_id=sid,
                passport_number=passport_number,
                nationality=nationality,
                ethnicity=ethnicity,
                criminal_record=criminal_record,
                social_security_number=social_security_number,
                current_latitude=current_latitude or None,
                current_longitude=current_longitude or None,
                destination_country=destination_country,
                current_country=current_country,
                visa_type=visa_type,
            )
            storage.save_profile(profile)
            st.success("Profile saved.")

    return UserProfile(
        session_id=sid,
        passport_number=passport_number,
        nationality=nationality,
        ethnicity=ethnicity,
        criminal_record=criminal_record,
        social_security_number=social_security_number,
        current_latitude=current_latitude or None,
        current_longitude=current_longitude or None,
        destination_country=destination_country,
        current_country=current_country,
        visa_type=visa_type,
    )


def _render_chat(profile: UserProfile) -> None:
    history = _load_history()
    for msg in history:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    if prompt := st.chat_input("Ask about immigration law..."):
        history.append({"role": "user", "content": prompt})
        storage.save_message(_session_id(), "user", prompt)
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                try:
                    reply = chat_service.ask(prompt, history[:-1], profile)
                except ValueError as exc:
                    reply = f"Configuration error: {exc}"
                except Exception as exc:
                    reply = f"Sorry, something went wrong: {exc}"
            st.markdown(reply)

        history.append({"role": "assistant", "content": reply})
        storage.save_message(_session_id(), "assistant", reply)
        st.session_state.messages = history


def _render_eligibility(profile: UserProfile) -> None:
    st.subheader("Visa eligibility check")
    st.write(
        "Get an automated visa eligibility score and recommended visa type "
        "based on your profile and destination country."
    )

    if not profile.destination_country:
        st.warning("Select a destination country in the sidebar first.")
        return

    if st.button("Run eligibility check", type="primary"):
        with st.spinner("Assessing eligibility..."):
            try:
                result = eligibility.check_eligibility(profile)
            except ValueError as exc:
                st.error(str(exc))
                return
            except Exception as exc:
                st.error(f"Assessment failed: {exc}")
                return

            storage.save_eligibility(
                _session_id(),
                profile.destination_country,
                result,
            )

            st.metric("Visa eligibility score", f"{result.visa_eligibility_score:.0f}/100")
            st.write(f"**Recommended visa:** {result.recommended_visa_type}")
            st.write(f"**Recommendation:** {result.automated_recommendation}")
            if result.risk_flags:
                st.write("**Risk flags:**")
                for flag in result.risk_flags:
                    st.write(f"- {flag}")


def main() -> None:
    st.title("Immigration Law AI")
    st.caption("Worldwide immigration Q&A and automated visa eligibility checks.")

    profile = _sidebar_profile()

    mode = st.radio(
        "Mode",
        ["Ask", "Check eligibility"],
        horizontal=True,
    )

    if mode == "Ask":
        _render_chat(profile)
    else:
        _render_eligibility(profile)


if __name__ == "__main__":
    main()
