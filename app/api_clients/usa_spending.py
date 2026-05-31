import requests


def normalize_award(item: dict) -> dict:
    return {
        "award_id": str(item.get("Award ID") or item.get("generated_internal_id") or item.get("award_id") or ""),
        "description": item.get("Description") or item.get("description") or "",
        "agency": item.get("Awarding Agency") or item.get("awarding_agency_name") or "",
        "incumbent": item.get("Recipient Name") or item.get("recipient_name") or "",
        "naics_code": str(item.get("NAICS") or item.get("naics_code") or ""),
        "psc_code": str(item.get("PSC") or item.get("psc_code") or ""),
        "amount": item.get("Award Amount") or item.get("award_amount"),
        "award_date": item.get("Start Date") or item.get("award_date"),
        "end_date": item.get("End Date") or item.get("end_date"),
        "source_url": "https://www.usaspending.gov/",
    }


class USASpendingClient:
    def __init__(self, base_url="https://api.usaspending.gov/api/v2/search/spending_by_award/", session=None):
        self.base_url = base_url
        self.session = session or requests.Session()

    def search_awards(self, naics_codes: list[str], limit=50):
        payload = {
            "filters": {"award_type_codes": ["A", "B", "C", "D"], "naics_codes": naics_codes},
            "fields": ["Award ID", "Recipient Name", "Award Amount", "Description", "Awarding Agency", "Start Date", "End Date", "NAICS", "PSC"],
            "limit": limit,
            "page": 1,
            "subawards": False,
        }
        response = self.session.post(self.base_url, json=payload, timeout=30)
        response.raise_for_status()
        return [normalize_award(item) for item in response.json().get("results", [])]

