from datetime import datetime, timedelta, timezone
from types import SimpleNamespace

from app.services.scoring import score_opportunity


NOW = datetime(2026, 5, 31, tzinfo=timezone.utc)


def profile():
    return SimpleNamespace(
        naics_codes=["541511"],
        psc_codes=["DA01"],
        keywords=["dashboard", "data governance"],
        target_agencies=["Department of Homeland Security"],
        set_asides=["Total Small Business"],
    )


def opportunity(**overrides):
    values = {
        "title": "Data governance dashboard",
        "description": "Dashboard implementation",
        "agency": "Department of Homeland Security",
        "office": "Data Office",
        "naics_code": "541511",
        "psc_code": "DA01",
        "set_aside": "Total Small Business",
        "response_deadline": NOW + timedelta(days=20),
        "notice_type": "Combined Synopsis/Solicitation",
    }
    values.update(overrides)
    return SimpleNamespace(**values)


def test_exact_matches_and_keywords_score_high():
    result = score_opportunity(profile(), opportunity(), NOW)
    assert result.score == 90
    assert "+25 NAICS match: 541511" in result.explanation
    assert any("keyword match" in reason for reason in result.explanation)
    assert "+10 set-aside match: Total Small Business" in result.explanation


def test_deadline_risk_does_not_award_deadline_points():
    result = score_opportunity(profile(), opportunity(response_deadline=NOW + timedelta(days=1)), NOW)
    assert result.score == 80
    assert "-10 deadline risk: response due in less than 3 days" in result.explanation


def test_unmatched_opportunity_scores_zero_without_deadline():
    result = score_opportunity(
        profile(),
        opportunity(
            title="Office supplies",
            description="Paper",
            agency="Department of Agriculture",
            office="Procurement",
            naics_code="339940",
            psc_code="7510",
            set_aside="Unrestricted",
            response_deadline=None,
            notice_type="Special Notice",
        ),
        NOW,
    )
    assert result.score == 0
