from app.api_clients.sam_gov import normalize_opportunity
from app.api_clients.usa_spending import normalize_award


def test_normalize_sam_opportunity():
    row = normalize_opportunity(
        {
            "noticeId": "abc",
            "title": "Dashboard",
            "fullParentPathName": "Department of Defense",
            "naicsCode": "541511",
            "classificationCode": "DA01",
            "responseDeadLine": "2026-06-30T12:00:00Z",
            "uiLink": "https://sam.gov/opp/abc/view",
        }
    )
    assert row["notice_id"] == "abc"
    assert row["naics_code"] == "541511"
    assert row["response_deadline"].year == 2026


def test_normalize_usaspending_award():
    row = normalize_award({"Award ID": "award-1", "Recipient Name": "Example LLC", "Award Amount": 123})
    assert row["award_id"] == "award-1"
    assert row["incumbent"] == "Example LLC"

