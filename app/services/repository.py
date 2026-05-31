from sqlalchemy import delete, select

from app.models.database import CompanyProfile, MatchResult, Opportunity, RecompeteLead, Watchlist
from app.services.recompete import infer_recompete_lead
from app.services.scoring import score_opportunity


SEED_PROFILE = {
    "company_name": "Example Small Business IT Consulting",
    "naics_codes": ["541511", "541512", "541519"],
    "psc_codes": ["DA01", "R408"],
    "keywords": ["data governance", "dashboard", "AI", "SharePoint", "knowledge management"],
    "target_agencies": ["Department of Defense", "Department of Homeland Security"],
    "set_asides": ["Total Small Business", "8(a)", "SDVOSB"],
    "min_value": 100000,
    "max_value": 5000000,
}


def get_or_seed_profile(session):
    profile = session.scalar(select(CompanyProfile).limit(1))
    if not profile:
        profile = CompanyProfile(**SEED_PROFILE)
        session.add(profile)
        session.commit()
    return profile


def save_profile(session, values):
    profile = get_or_seed_profile(session)
    for key, value in values.items():
        setattr(profile, key, value)
    session.commit()
    return profile


def upsert_opportunities(session, rows):
    for row in rows:
        existing = session.get(Opportunity, row["notice_id"])
        if existing:
            for key, value in row.items():
                setattr(existing, key, value)
        else:
            session.add(Opportunity(**row))
    session.commit()


def refresh_scores(session, profile):
    session.execute(delete(MatchResult).where(MatchResult.profile_id == profile.id))
    for opportunity in session.scalars(select(Opportunity)).all():
        result = score_opportunity(profile, opportunity)
        session.add(MatchResult(notice_id=opportunity.notice_id, profile_id=profile.id, score=result.score, explanation=result.explanation))
    session.commit()


def ranked_matches(session):
    return session.execute(
        select(MatchResult, Opportunity).join(Opportunity, MatchResult.notice_id == Opportunity.notice_id).order_by(MatchResult.score.desc())
    ).all()


def save_watchlist(session, notice_id, status="new", notes=""):
    item = session.scalar(select(Watchlist).where(Watchlist.notice_id == notice_id))
    if not item:
        item = Watchlist(notice_id=notice_id)
        session.add(item)
    item.status = status
    item.notes = notes
    session.commit()


def upsert_recompete_leads(session, awards):
    for award in awards:
        row = infer_recompete_lead(award)
        existing = session.scalar(select(RecompeteLead).where(RecompeteLead.award_id == row["award_id"]))
        if existing:
            for key, value in row.items():
                setattr(existing, key, value)
        else:
            session.add(RecompeteLead(**row))
    session.commit()

