# GovCon Proactive Insight MVP

Local-first Streamlit app for small and midsize government contractors. It ranks public SAM.gov opportunities against one company profile, tracks a watchlist, exports follow-up lists, and surfaces cautious recompete watch items inferred from public USAspending award records.

## MVP Boundaries

- Public data only. Do not add CUI, source-selection sensitive, proprietary, or non-public contracting data.
- Match scores are triage aids, not procurement advice.
- Recompete leads are inferred watch items, not confirmed future solicitations.
- Verify every opportunity and deadline in the official SAM.gov record before taking business action.
- This MVP has no login, cloud deployment, paid APIs, or automated proposal writing.

## Quick Start

1. Install Python 3.11 or newer.
2. Create a virtual environment:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

3. Copy `.env.example` to `.env`. Add a SAM.gov public API key if you have one:

```text
SAM_API_KEY=your_key_here
DATABASE_URL=sqlite:///./govcon_mvp.db
DEFAULT_DAYS_AHEAD=90
```

4. Seed the local database and run the app:

```powershell
python -m app.seed
streamlit run app/ui/main.py
```

5. Open `http://localhost:8501`.

The app also works without a SAM.gov key: click **Load sample opportunities** for an immediately usable offline demo.

## API Keys

Request a SAM.gov public API key through [SAM.gov](https://sam.gov/). USAspending award search uses its public API and does not require a key.

## Main Workflow

1. Edit the seeded company profile.
2. Load sample opportunities or refresh from SAM.gov.
3. Review ranked matches and the plain-language explanation for each score.
4. Open the official SAM.gov source record.
5. Save promising opportunities to the watchlist.
6. Export matched opportunities, watchlist items, or recompete leads as CSV.

## Tests

```powershell
pytest
```

## Project Structure

```text
app/api_clients/   Public SAM.gov and USAspending clients
app/models/        SQLAlchemy schema and database initialization
app/services/      Scoring, persistence helpers, exports, and sample data
app/ui/            Streamlit application
tests/             Scoring, parsing, and recompete inference tests
```

