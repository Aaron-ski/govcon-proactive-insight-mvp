import time
from datetime import datetime, timezone

import requests


def parse_datetime(value):
    if not value:
        return None
    try:
        return datetime.fromisoformat(str(value).replace("Z", "+00:00"))
    except ValueError:
        return None


def normalize_opportunity(item: dict) -> dict:
    notice_id = item.get("noticeId") or item.get("notice_id") or item.get("solicitationNumber")
    return {
        "notice_id": str(notice_id),
        "title": item.get("title") or "Untitled opportunity",
        "agency": item.get("fullParentPathName") or item.get("agency") or "",
        "office": item.get("officeAddress", {}).get("city") if isinstance(item.get("officeAddress"), dict) else item.get("office"),
        "notice_type": item.get("type") or item.get("noticeType") or "",
        "set_aside": item.get("typeOfSetAsideDescription") or item.get("setAside") or "",
        "naics_code": str(item.get("naicsCode") or item.get("naics_code") or ""),
        "psc_code": str(item.get("classificationCode") or item.get("psc_code") or ""),
        "posted_date": parse_datetime(item.get("postedDate") or item.get("posted_date")),
        "response_deadline": parse_datetime(item.get("responseDeadLine") or item.get("response_deadline")),
        "description": item.get("description") or "",
        "sam_url": item.get("uiLink") or item.get("sam_url") or f"https://sam.gov/opp/{notice_id}/view",
        "raw_json": item,
        "last_seen_at": datetime.now(timezone.utc),
    }


class SamGovClient:
    def __init__(self, api_key: str, base_url="https://api.sam.gov/opportunities/v2/search", session=None, retries=2):
        self.api_key = api_key
        self.base_url = base_url
        self.session = session or requests.Session()
        self.retries = retries

    def fetch_active(self, posted_from: str, posted_to: str, limit=100, max_pages=3):
        if not self.api_key:
            raise ValueError("SAM_API_KEY is not configured. Add it to .env or use sample data.")
        results = []
        for page in range(max_pages):
            params = {
                "api_key": self.api_key,
                "postedFrom": posted_from,
                "postedTo": posted_to,
                "limit": limit,
                "offset": page * limit,
            }
            response = self._get(params)
            payload = response.json()
            items = payload.get("opportunitiesData", [])
            results.extend(normalize_opportunity(item) for item in items)
            if len(items) < limit:
                break
        return results

    def _get(self, params):
        for attempt in range(self.retries + 1):
            try:
                response = self.session.get(self.base_url, params=params, timeout=30)
                response.raise_for_status()
                return response
            except requests.RequestException:
                if attempt == self.retries:
                    raise
                time.sleep(0.25 * (attempt + 1))

