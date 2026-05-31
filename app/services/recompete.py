from datetime import datetime, timedelta, timezone

from app.api_clients.sam_gov import parse_datetime


def infer_recompete_lead(award: dict, now: datetime | None = None) -> dict:
    now = now or datetime.now(timezone.utc)
    award_date = award.get("award_date")
    end_date = award.get("end_date")
    if isinstance(award_date, str):
        award_date = parse_datetime(award_date)
    if isinstance(end_date, str):
        end_date = parse_datetime(end_date)
    if end_date and end_date.tzinfo is None:
        end_date = end_date.replace(tzinfo=timezone.utc)

    confidence = "low"
    basis = "Possible watch item inferred from similar public historical award data. Validate in SAM.gov."
    if end_date and now + timedelta(days=90) <= end_date <= now + timedelta(days=548):
        confidence = "high"
        basis = "Public award period of performance ends in the next 3-18 months. This is an inferred lead, not a confirmed recompete."
    elif award_date:
        confidence = "medium"
        basis = "Historical award timing suggests a possible future procurement window, but public end-date data is incomplete."
    return {**award, "award_date": award_date, "end_date": end_date, "confidence": confidence, "basis": basis}

