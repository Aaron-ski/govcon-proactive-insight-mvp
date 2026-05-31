from datetime import datetime, timedelta, timezone

from app.services.recompete import infer_recompete_lead


def test_explicit_end_date_in_window_is_high_confidence():
    now = datetime(2026, 5, 31, tzinfo=timezone.utc)
    row = infer_recompete_lead({"award_id": "a", "end_date": now + timedelta(days=180)}, now)
    assert row["confidence"] == "high"
    assert "not a confirmed recompete" in row["basis"]

