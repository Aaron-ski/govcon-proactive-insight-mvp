from datetime import datetime, timedelta, timezone


def sample_opportunities():
    now = datetime.now(timezone.utc)
    common = {"posted_date": now - timedelta(days=3), "last_seen_at": now}
    return [
        {
            **common,
            "notice_id": "SAMPLE-001",
            "title": "Data Governance Dashboard Support",
            "agency": "Department of Homeland Security",
            "office": "Office of the Chief Data Officer",
            "notice_type": "Combined Synopsis/Solicitation",
            "set_aside": "Total Small Business",
            "naics_code": "541511",
            "psc_code": "DA01",
            "response_deadline": now + timedelta(days=21),
            "description": "Dashboard, data governance, analytics, and knowledge management support.",
            "sam_url": "https://sam.gov/",
            "raw_json": {"sample": True},
        },
        {
            **common,
            "notice_id": "SAMPLE-002",
            "title": "AI Knowledge Management Market Research",
            "agency": "Department of Defense",
            "office": "Digital Services Office",
            "notice_type": "Sources Sought",
            "set_aside": "Total Small Business",
            "naics_code": "541512",
            "psc_code": "R408",
            "response_deadline": now + timedelta(days=12),
            "description": "Seeking industry input for AI-enabled SharePoint and knowledge management services.",
            "sam_url": "https://sam.gov/",
            "raw_json": {"sample": True},
        },
        {
            **common,
            "notice_id": "SAMPLE-003",
            "title": "Enterprise Collaboration Platform Operations",
            "agency": "Department of the Interior",
            "office": "IT Operations",
            "notice_type": "Solicitation",
            "set_aside": "Unrestricted",
            "naics_code": "541519",
            "psc_code": "DA10",
            "response_deadline": now + timedelta(days=35),
            "description": "Operations support for collaboration and content management tools.",
            "sam_url": "https://sam.gov/",
            "raw_json": {"sample": True},
        },
    ]


def sample_awards():
    now = datetime.now(timezone.utc)
    return [
        {
            "award_id": "SAMPLE-AWARD-001",
            "description": "Data analytics and dashboard operations support",
            "agency": "Department of Homeland Security",
            "incumbent": "Example Analytics LLC",
            "naics_code": "541511",
            "psc_code": "DA01",
            "amount": 2400000,
            "award_date": now - timedelta(days=1400),
            "end_date": now + timedelta(days=240),
            "source_url": "https://www.usaspending.gov/",
        },
        {
            "award_id": "SAMPLE-AWARD-002",
            "description": "Knowledge management modernization services",
            "agency": "Department of Defense",
            "incumbent": "Example Digital Services Inc.",
            "naics_code": "541512",
            "psc_code": "R408",
            "amount": 875000,
            "award_date": now - timedelta(days=1100),
            "end_date": None,
            "source_url": "https://www.usaspending.gov/",
        },
    ]

