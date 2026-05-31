from app.models.database import init_db
from app.services.repository import get_or_seed_profile, refresh_scores, upsert_opportunities, upsert_recompete_leads
from app.services.sample_data import sample_awards, sample_opportunities


def seed():
    Session = init_db()
    with Session() as session:
        profile = get_or_seed_profile(session)
        upsert_opportunities(session, sample_opportunities())
        refresh_scores(session, profile)
        upsert_recompete_leads(session, sample_awards())
    print("Seeded sample profile, opportunities, scores, and recompete leads.")


if __name__ == "__main__":
    seed()

