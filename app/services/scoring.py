from dataclasses import dataclass
from datetime import datetime, timezone


@dataclass
class ScoreResult:
    score: int
    explanation: list[str]


def _norm(value) -> str:
    return str(value or "").strip().lower()


def _days_remaining(deadline: datetime | None, now: datetime) -> int | None:
    if not deadline:
        return None
    if deadline.tzinfo is None:
        deadline = deadline.replace(tzinfo=timezone.utc)
    return (deadline - now).days


def score_opportunity(profile, opportunity, now: datetime | None = None) -> ScoreResult:
    now = now or datetime.now(timezone.utc)
    score = 0
    reasons: list[str] = []
    naics = {_norm(x) for x in profile.naics_codes}
    psc = {_norm(x) for x in profile.psc_codes}

    if _norm(opportunity.naics_code) in naics:
        score += 25
        reasons.append(f"+25 NAICS match: {opportunity.naics_code}")
    if _norm(opportunity.psc_code) in psc:
        score += 15
        reasons.append(f"+15 PSC match: {opportunity.psc_code}")

    searchable = " ".join(
        [_norm(opportunity.title), _norm(opportunity.description), _norm(opportunity.agency), _norm(opportunity.office)]
    )
    matched_keywords = [word for word in profile.keywords if _norm(word) and _norm(word) in searchable]
    if matched_keywords:
        keyword_points = min(20, 5 * len(matched_keywords))
        score += keyword_points
        reasons.append(f"+{keyword_points} keyword match: {', '.join(matched_keywords)}")

    matched_agency = next((agency for agency in profile.target_agencies if _norm(agency) in searchable), None)
    if matched_agency:
        score += 15
        reasons.append(f"+15 agency match: {matched_agency}")

    set_aside = _norm(opportunity.set_aside)
    matched_set_aside = next((item for item in profile.set_asides if _norm(item) in set_aside or set_aside in _norm(item)), None)
    if set_aside and matched_set_aside:
        score += 10
        reasons.append(f"+10 set-aside match: {opportunity.set_aside}")

    days = _days_remaining(opportunity.response_deadline, now)
    if days is None:
        reasons.append("Deadline not provided: verify on SAM.gov")
    elif days < 0:
        reasons.append("Deadline expired: verify notice status on SAM.gov")
    elif days < 3:
        reasons.append("-10 deadline risk: response due in less than 3 days")
    elif 7 <= days <= 45:
        score += 10
        reasons.append(f"+10 healthy deadline: {days} days remaining")
    else:
        score += 5
        reasons.append(f"+5 deadline: {days} days remaining")

    notice_type = _norm(opportunity.notice_type)
    if any(label in notice_type for label in ["solicitation", "sources sought", "rfi", "rfq", "rfp"]):
        score += 5
        reasons.append(f"+5 notice type fit: {opportunity.notice_type}")
    return ScoreResult(min(100, max(0, score)), reasons)

