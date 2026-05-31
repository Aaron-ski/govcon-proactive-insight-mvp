import os
import sys
from datetime import date, timedelta
from pathlib import Path

import streamlit as st
from dotenv import load_dotenv
from sqlalchemy import select

# Streamlit Cloud executes this file directly, so add the repository root for app imports.
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from app.api_clients.sam_gov import SamGovClient
from app.api_clients.usa_spending import USASpendingClient
from app.models.database import Opportunity, RecompeteLead, Watchlist, init_db
from app.services.exports import to_csv
from app.services.repository import (
    get_or_seed_profile,
    ranked_matches,
    refresh_scores,
    save_profile,
    save_watchlist,
    upsert_opportunities,
    upsert_recompete_leads,
)
from app.services.sample_data import sample_awards, sample_opportunities

load_dotenv()
st.set_page_config(page_title="GovCon Proactive Insight MVP", layout="wide")
Session = init_db()


def split_csv(value):
    return [item.strip() for item in value.split(",") if item.strip()]


def fmt_date(value):
    return value.strftime("%Y-%m-%d") if value else "Verify on source"


def match_rows(session):
    rows = []
    for match, opportunity in ranked_matches(session):
        rows.append(
            {
                "notice_id": opportunity.notice_id,
                "title": opportunity.title,
                "score": match.score,
                "agency": opportunity.agency,
                "naics": opportunity.naics_code,
                "psc": opportunity.psc_code,
                "set_aside": opportunity.set_aside,
                "due": fmt_date(opportunity.response_deadline),
                "source_url": opportunity.sam_url,
                "match_explanation": "; ".join(match.explanation),
            }
        )
    return rows


def refresh_sample(session):
    profile = get_or_seed_profile(session)
    upsert_opportunities(session, sample_opportunities())
    refresh_scores(session, profile)


def sidebar(session):
    st.sidebar.title("GovCon Insight")
    st.sidebar.caption("Public-data opportunity triage for small businesses")
    page = st.sidebar.radio("Go to", ["Dashboard", "Company Profile", "Opportunity Detail", "Recompete Leads", "Exports"])
    st.sidebar.divider()
    if st.sidebar.button("Load sample opportunities", width="stretch"):
        refresh_sample(session)
        st.sidebar.success("Sample opportunities loaded.")
    if st.sidebar.button("Refresh from SAM.gov", width="stretch"):
        key = os.getenv("SAM_API_KEY", "")
        try:
            today = date.today()
            rows = SamGovClient(key).fetch_active(
                posted_from=(today - timedelta(days=30)).strftime("%m/%d/%Y"),
                posted_to=today.strftime("%m/%d/%Y"),
            )
            upsert_opportunities(session, rows)
            refresh_scores(session, get_or_seed_profile(session))
            st.sidebar.success(f"Loaded {len(rows)} SAM.gov opportunities.")
        except Exception as exc:
            st.sidebar.error(f"SAM.gov refresh failed: {exc}")
    return page


def dashboard(session):
    st.title("Opportunity Dashboard")
    st.caption("Review public opportunity leads, understand the match, then verify details in SAM.gov before acting.")
    rows = match_rows(session)
    watch_count = len(session.scalars(select(Watchlist)).all())
    leads_count = len(session.scalars(select(RecompeteLead)).all())
    due_soon = sum(1 for _, opp in ranked_matches(session) if opp.response_deadline and 0 <= (opp.response_deadline.date() - date.today()).days <= 7)
    cards = st.columns(4)
    cards[0].metric("Active matches", len(rows))
    cards[1].metric("Due in 7 days", due_soon)
    cards[2].metric("Saved watchlist", watch_count)
    cards[3].metric("Recompete leads", leads_count)
    if not rows:
        st.info("Load sample opportunities or refresh from SAM.gov to create your first ranked matches.")
        return
    min_score = st.slider("Minimum match score", 0, 100, 0, 5)
    filtered = [row for row in rows if row["score"] >= min_score]
    st.subheader("Top matches")
    st.dataframe(filtered, width="stretch", hide_index=True)
    st.caption("Scores are triage aids, not procurement advice. Open the official source before making a business decision.")


def company_profile(session):
    st.title("Company Profile")
    profile = get_or_seed_profile(session)
    st.caption("The profile drives ranking. Use comma-separated values for lists.")
    with st.form("company_profile"):
        company_name = st.text_input("Company name", profile.company_name)
        naics = st.text_input("NAICS codes", ", ".join(profile.naics_codes))
        psc = st.text_input("PSC codes", ", ".join(profile.psc_codes))
        keywords = st.text_area("Keywords", ", ".join(profile.keywords))
        agencies = st.text_area("Target agencies", ", ".join(profile.target_agencies))
        set_asides = st.text_input("Set-aside preferences", ", ".join(profile.set_asides))
        c1, c2 = st.columns(2)
        min_value = c1.number_input("Minimum contract value", min_value=0, value=profile.min_value or 0, step=50000)
        max_value = c2.number_input("Maximum contract value", min_value=0, value=profile.max_value or 0, step=50000)
        if st.form_submit_button("Save profile"):
            save_profile(
                session,
                {
                    "company_name": company_name,
                    "naics_codes": split_csv(naics),
                    "psc_codes": split_csv(psc),
                    "keywords": split_csv(keywords),
                    "target_agencies": split_csv(agencies),
                    "set_asides": split_csv(set_asides),
                    "min_value": min_value or None,
                    "max_value": max_value or None,
                },
            )
            refresh_scores(session, get_or_seed_profile(session))
            st.success("Profile saved and opportunity scores refreshed.")


def opportunity_detail(session):
    st.title("Opportunity Detail")
    matches = ranked_matches(session)
    if not matches:
        st.info("Load sample opportunities or refresh from SAM.gov first.")
        return
    options = {f"{match.score:03d} | {opp.title}": (match, opp) for match, opp in matches}
    selected = st.selectbox("Select opportunity", list(options))
    match, opp = options[selected]
    st.subheader(opp.title)
    c1, c2, c3 = st.columns(3)
    c1.metric("Match score", f"{match.score}/100")
    c2.metric("Due date", fmt_date(opp.response_deadline))
    c3.metric("Notice type", opp.notice_type or "Verify on source")
    st.write(f"**Agency:** {opp.agency or 'Verify on source'}")
    st.write(f"**Office:** {opp.office or 'Verify on source'}")
    st.write(f"**Set-aside:** {opp.set_aside or 'Verify on source'}")
    st.link_button("Open official SAM.gov source", opp.sam_url or "https://sam.gov/")
    st.subheader("Why this matched")
    for reason in match.explanation:
        st.write(f"- {reason}")
    st.subheader("Action checklist")
    for task in ["Read the full notice", "Confirm eligibility", "Confirm the deadline", "Gather attachments", "Draft questions", "Make a bid/no-bid decision"]:
        st.checkbox(task, key=f"{opp.notice_id}-{task}")
    with st.form("watchlist"):
        status = st.selectbox("Watchlist status", ["new", "review", "bid", "no-bid", "submitted"])
        notes = st.text_area("Notes")
        if st.form_submit_button("Save to watchlist"):
            save_watchlist(session, opp.notice_id, status, notes)
            st.success("Watchlist updated.")


def recompete_leads(session):
    st.title("Recompete Leads")
    st.warning("These are inferred watch items from public historical award data. They are not confirmed recompetes.")
    c1, c2 = st.columns(2)
    if c1.button("Load sample leads", width="stretch"):
        upsert_recompete_leads(session, sample_awards())
        st.success("Sample inferred leads loaded.")
    if c2.button("Find leads with USAspending", width="stretch"):
        try:
            profile = get_or_seed_profile(session)
            awards = USASpendingClient().search_awards(profile.naics_codes)
            upsert_recompete_leads(session, awards)
            st.success(f"Loaded {len(awards)} public award records.")
        except Exception as exc:
            st.error(f"USAspending search failed: {exc}")
    leads = session.scalars(select(RecompeteLead).order_by(RecompeteLead.confidence, RecompeteLead.end_date)).all()
    rows = [
        {
            "description": lead.description,
            "confidence": lead.confidence,
            "agency": lead.agency,
            "incumbent": lead.incumbent,
            "naics": lead.naics_code,
            "psc": lead.psc_code,
            "amount": lead.amount,
            "award_date": fmt_date(lead.award_date),
            "end_date": fmt_date(lead.end_date),
            "basis": lead.basis,
            "source_url": lead.source_url,
        }
        for lead in leads
    ]
    st.dataframe(rows, width="stretch", hide_index=True)


def exports(session):
    st.title("Exports")
    st.caption("Download working lists for follow-up. Verify source records before business action.")
    matches = match_rows(session)
    match_columns = ["notice_id", "title", "score", "agency", "naics", "psc", "set_aside", "due", "source_url", "match_explanation"]
    st.download_button("Download matched opportunities CSV", to_csv(matches, match_columns), "matched_opportunities.csv", "text/csv")
    watch_rows = [
        {"notice_id": item.notice_id, "status": item.status, "notes": item.notes or "", "created_at": item.created_at}
        for item in session.scalars(select(Watchlist)).all()
    ]
    st.download_button("Download watchlist CSV", to_csv(watch_rows, ["notice_id", "status", "notes", "created_at"]), "watchlist.csv", "text/csv")
    lead_rows = [
        {
            "award_id": lead.award_id,
            "description": lead.description,
            "confidence": lead.confidence,
            "agency": lead.agency,
            "incumbent": lead.incumbent,
            "naics": lead.naics_code,
            "psc": lead.psc_code,
            "amount": lead.amount,
            "award_date": lead.award_date,
            "end_date": lead.end_date,
            "basis": lead.basis,
            "source_url": lead.source_url,
        }
        for lead in session.scalars(select(RecompeteLead)).all()
    ]
    lead_columns = ["award_id", "description", "confidence", "agency", "incumbent", "naics", "psc", "amount", "award_date", "end_date", "basis", "source_url"]
    st.download_button("Download recompete leads CSV", to_csv(lead_rows, lead_columns), "recompete_leads.csv", "text/csv")


def main():
    with Session() as session:
        get_or_seed_profile(session)
        page = sidebar(session)
        pages = {
            "Dashboard": dashboard,
            "Company Profile": company_profile,
            "Opportunity Detail": opportunity_detail,
            "Recompete Leads": recompete_leads,
            "Exports": exports,
        }
        pages[page](session)


if __name__ == "__main__":
    main()
