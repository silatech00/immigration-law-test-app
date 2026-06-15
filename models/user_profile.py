from dataclasses import asdict, dataclass, field


@dataclass
class UserProfile:
    session_id: str
    passport_number: str = ""
    nationality: str = ""
    ethnicity: str = ""
    criminal_record: str = ""
    social_security_number: str = ""
    current_latitude: float | None = None
    current_longitude: float | None = None
    destination_country: str = ""
    current_country: str = ""
    visa_type: str = ""

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_row(cls, row: dict) -> "UserProfile":
        return cls(
            session_id=row["session_id"],
            passport_number=row.get("passport_number") or "",
            nationality=row.get("nationality") or "",
            ethnicity=row.get("ethnicity") or "",
            criminal_record=row.get("criminal_record") or "",
            social_security_number=row.get("social_security_number") or "",
            current_latitude=row.get("current_latitude"),
            current_longitude=row.get("current_longitude"),
            destination_country=row.get("destination_country") or "",
            current_country=row.get("current_country") or "",
            visa_type=row.get("visa_type") or "",
        )


@dataclass
class EligibilityResult:
    visa_eligibility_score: float
    recommended_visa_type: str
    automated_recommendation: str
    risk_flags: list[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        return {
            "visa_eligibility_score": self.visa_eligibility_score,
            "recommended_visa_type": self.recommended_visa_type,
            "automated_recommendation": self.automated_recommendation,
            "risk_flags": self.risk_flags,
        }
