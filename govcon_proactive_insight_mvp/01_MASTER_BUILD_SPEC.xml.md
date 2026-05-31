<codex_project>
  <project_name>GovCon Proactive Insight MVP</project_name>
  <goal>
    Build a locally hosted MVP that helps small and midsize government contractors identify relevant active opportunities, track likely recompetes, and reduce time spent navigating SAM.gov/USAspending data.
  </goal>

  <constraints>
    <constraint>Solo-developer friendly.</constraint>
    <constraint>Run locally first with minimal/no cost.</constraint>
    <constraint>Use public/open APIs where possible.</constraint>
    <constraint>Do not scrape sites unless explicitly allowed by terms of service.</constraint>
    <constraint>Do not store CUI, source-selection sensitive, proprietary, or non-public contracting data.</constraint>
    <constraint>Design so it can later be published as a static GitHub Pages demo or deployed as a small web app.</constraint>
  </constraints>

  <recommended_stack>
    <backend>Python 3.11+, FastAPI, requests/httpx, pydantic, SQLite, SQLAlchemy</backend>
    <frontend>Streamlit for fastest MVP, or React/Vite if creating a portfolio-grade web UI</frontend>
    <scheduler>Local cron, Windows Task Scheduler, or APScheduler</scheduler>
    <data_sources>
      <source>SAM.gov Get Opportunities Public API for active opportunities</source>
      <source>USAspending API for historical awards and incumbent/recompete research</source>
      <source>Optional: SAM.gov entity APIs for entity lookup if API access is approved</source>
    </data_sources>
  </recommended_stack>

  <mvp_scope>
    <feature id="F1">Company profile with NAICS, PSC, keywords, agencies, place of performance, set-aside preferences, and contract value range.</feature>
    <feature id="F2">Daily or manual opportunity ingestion from SAM.gov opportunities API.</feature>
    <feature id="F3">Opportunity matching score based on NAICS/PSC/keywords/agency/set-aside/deadline.</feature>
    <feature id="F4">Dashboard showing best-fit opportunities, due dates, days remaining, agency, type, set-aside, and match explanation.</feature>
    <feature id="F5">Historical award/recompete research using USAspending search endpoint to identify expiring/old awards by agency, NAICS, PSC, recipient, and period of performance where available.</feature>
    <feature id="F6">Plain-English action checklist for each opportunity: read notice, confirm eligibility, confirm deadline, gather attachments, draft questions, bid/no-bid decision.</feature>
    <feature id="F7">CSV export for matched opportunities and watchlist.</feature>
  </mvp_scope>

  <out_of_scope_for_mvp>
    <item>Automated proposal writing.</item>
    <item>Login/multi-tenant SaaS.</item>
    <item>Payment processing.</item>
    <item>Storing proposal files.</item>
    <item>Integrating with proprietary GovCon platforms.</item>
  </out_of_scope_for_mvp>

  <deliverables>
    <deliverable>Working local app.</deliverable>
    <deliverable>README with setup steps.</deliverable>
    <deliverable>.env.example for API keys and config.</deliverable>
    <deliverable>SQLite database schema and seed profile.</deliverable>
    <deliverable>Unit tests for scoring and API parsing.</deliverable>
  </deliverables>

  <acceptance_criteria>
    <criterion>User can create/edit one company profile.</criterion>
    <criterion>User can run ingestion manually.</criterion>
    <criterion>App displays at least 25 active opportunities when API is configured.</criterion>
    <criterion>Each matched opportunity has a score and explanation.</criterion>
    <criterion>User can save opportunities to a watchlist.</criterion>
    <criterion>User can export matches to CSV.</criterion>
    <criterion>App handles API failures gracefully with a clear message.</criterion>
  </acceptance_criteria>
</codex_project>
