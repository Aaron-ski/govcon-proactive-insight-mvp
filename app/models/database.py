import os
from datetime import datetime, timezone

from sqlalchemy import DateTime, Float, ForeignKey, Integer, JSON, String, Text, create_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, sessionmaker


class Base(DeclarativeBase):
    pass


def utcnow() -> datetime:
    return datetime.now(timezone.utc)


class CompanyProfile(Base):
    __tablename__ = "company_profile"
    id: Mapped[int] = mapped_column(primary_key=True)
    company_name: Mapped[str] = mapped_column(String(200))
    naics_codes: Mapped[list] = mapped_column(JSON, default=list)
    psc_codes: Mapped[list] = mapped_column(JSON, default=list)
    keywords: Mapped[list] = mapped_column(JSON, default=list)
    target_agencies: Mapped[list] = mapped_column(JSON, default=list)
    set_asides: Mapped[list] = mapped_column(JSON, default=list)
    min_value: Mapped[int | None] = mapped_column(Integer, nullable=True)
    max_value: Mapped[int | None] = mapped_column(Integer, nullable=True)


class Opportunity(Base):
    __tablename__ = "opportunity"
    notice_id: Mapped[str] = mapped_column(String(120), primary_key=True)
    title: Mapped[str] = mapped_column(String(500))
    agency: Mapped[str] = mapped_column(String(300), default="")
    office: Mapped[str | None] = mapped_column(String(300), nullable=True)
    notice_type: Mapped[str] = mapped_column(String(120), default="")
    set_aside: Mapped[str | None] = mapped_column(String(200), nullable=True)
    naics_code: Mapped[str | None] = mapped_column(String(30), nullable=True)
    psc_code: Mapped[str | None] = mapped_column(String(30), nullable=True)
    posted_date: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    response_deadline: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    sam_url: Mapped[str] = mapped_column(String(800), default="")
    raw_json: Mapped[dict] = mapped_column(JSON, default=dict)
    last_seen_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)


class MatchResult(Base):
    __tablename__ = "match_result"
    id: Mapped[int] = mapped_column(primary_key=True)
    notice_id: Mapped[str] = mapped_column(ForeignKey("opportunity.notice_id"))
    profile_id: Mapped[int] = mapped_column(ForeignKey("company_profile.id"))
    score: Mapped[int] = mapped_column(Integer)
    explanation: Mapped[list] = mapped_column(JSON, default=list)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)


class Watchlist(Base):
    __tablename__ = "watchlist"
    id: Mapped[int] = mapped_column(primary_key=True)
    notice_id: Mapped[str] = mapped_column(ForeignKey("opportunity.notice_id"), unique=True)
    status: Mapped[str] = mapped_column(String(30), default="new")
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)


class RecompeteLead(Base):
    __tablename__ = "recompete_lead"
    id: Mapped[int] = mapped_column(primary_key=True)
    award_id: Mapped[str] = mapped_column(String(160), unique=True)
    description: Mapped[str] = mapped_column(Text, default="")
    agency: Mapped[str] = mapped_column(String(300), default="")
    incumbent: Mapped[str] = mapped_column(String(300), default="")
    naics_code: Mapped[str | None] = mapped_column(String(30), nullable=True)
    psc_code: Mapped[str | None] = mapped_column(String(30), nullable=True)
    amount: Mapped[float | None] = mapped_column(Float, nullable=True)
    award_date: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    end_date: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    confidence: Mapped[str] = mapped_column(String(20))
    basis: Mapped[str] = mapped_column(Text)
    source_url: Mapped[str] = mapped_column(String(800), default="https://www.usaspending.gov/")


def get_engine(database_url: str | None = None):
    return create_engine(database_url or os.getenv("DATABASE_URL", "sqlite:///./govcon_mvp.db"))


def get_session_factory(database_url: str | None = None):
    return sessionmaker(bind=get_engine(database_url), expire_on_commit=False)


def init_db(database_url: str | None = None):
    engine = get_engine(database_url)
    Base.metadata.create_all(engine)
    return sessionmaker(bind=engine, expire_on_commit=False)

