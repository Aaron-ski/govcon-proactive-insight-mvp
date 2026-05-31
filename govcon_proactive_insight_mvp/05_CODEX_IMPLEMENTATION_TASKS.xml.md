<codex_implementation_tasks>
  <task id="T1" name="Create repository structure">
    <instructions>
      Create folders: app/, app/api_clients/, app/models/, app/services/, app/ui/, tests/, data/exports/.
      Add README.md, requirements.txt, .env.example, .gitignore.
    </instructions>
  </task>

  <task id="T2" name="Build data layer">
    <instructions>
      Implement SQLAlchemy models for company_profile, opportunity, match_result, watchlist, recompete_lead.
      Add database initialization and seed script.
    </instructions>
  </task>

  <task id="T3" name="Build API clients">
    <instructions>
      Implement SamGovClient with configurable base URL, API key, pagination, retries, and normalized opportunity parser.
      Implement USASpendingClient for spending_by_award search.
      Add tests using mocked responses.
    </instructions>
  </task>

  <task id="T4" name="Build scoring service">
    <instructions>
      Implement opportunity scoring based on the rules in 03_MATCHING_AND_RECOMPETE_LOGIC.xml.md.
      Return score and explanation array.
      Add unit tests for exact NAICS match, keyword match, deadline risk, and set-aside match.
    </instructions>
  </task>

  <task id="T5" name="Build Streamlit UI">
    <instructions>
      Create pages for Dashboard, Company Profile, Opportunity Detail, Recompete Leads, and Exports.
      Use Streamlit session state sparingly and keep business logic in services.
    </instructions>
  </task>

  <task id="T6" name="Add exports">
    <instructions>
      Add CSV export for opportunities, match results, watchlist, and recompete leads.
      Include source URL and match explanation columns.
    </instructions>
  </task>

  <task id="T7" name="Add README setup guide">
    <instructions>
      Explain how to get API keys, create .env, install requirements, initialize DB, run app, and run tests.
      Include a safety/compliance note: public data only, verify opportunities in SAM.gov before business action.
    </instructions>
  </task>

  <definition_of_done>
    <item>pytest passes.</item>
    <item>streamlit run app/ui/main.py launches without error.</item>
    <item>Manual refresh retrieves or mock-loads opportunities.</item>
    <item>At least one sample profile produces scored matches from sample data.</item>
    <item>README is beginner-friendly.</item>
  </definition_of_done>
</codex_implementation_tasks>
