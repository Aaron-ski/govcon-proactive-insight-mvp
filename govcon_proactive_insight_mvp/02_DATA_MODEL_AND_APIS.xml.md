<data_model_and_apis>
  <environment_variables>
    <var name="SAM_API_KEY" required="true">SAM.gov API key for opportunities.</var>
    <var name="DATABASE_URL" default="sqlite:///./govcon_mvp.db">Local SQLite database.</var>
    <var name="DEFAULT_DAYS_AHEAD" default="90">How far ahead to search active opportunities.</var>
  </environment_variables>

  <tables>
    <table name="company_profile">
      <field name="id" type="integer primary key" />
      <field name="company_name" type="text" />
      <field name="naics_codes" type="json array text" example="[541511,541512,541519]" />
      <field name="psc_codes" type="json array text" example="[DA01, R408]" />
      <field name="keywords" type="json array text" example="[data governance, dashboard, AI, SharePoint, knowledge management]" />
      <field name="target_agencies" type="json array text" example="[Department of Defense, Department of Homeland Security]" />
      <field name="set_asides" type="json array text" example="[Total Small Business, 8(a), SDVOSB]" />
      <field name="min_value" type="integer nullable" />
      <field name="max_value" type="integer nullable" />
    </table>

    <table name="opportunity">
      <field name="notice_id" type="text primary key" />
      <field name="title" type="text" />
      <field name="agency" type="text" />
      <field name="office" type="text nullable" />
      <field name="notice_type" type="text" />
      <field name="set_aside" type="text nullable" />
      <field name="naics_code" type="text nullable" />
      <field name="psc_code" type="text nullable" />
      <field name="posted_date" type="date nullable" />
      <field name="response_deadline" type="datetime nullable" />
      <field name="description" type="text nullable" />
      <field name="sam_url" type="text" />
      <field name="raw_json" type="json" />
      <field name="last_seen_at" type="datetime" />
    </table>

    <table name="match_result">
      <field name="id" type="integer primary key" />
      <field name="notice_id" type="text foreign key" />
      <field name="profile_id" type="integer foreign key" />
      <field name="score" type="integer 0-100" />
      <field name="explanation" type="json array text" />
      <field name="created_at" type="datetime" />
    </table>

    <table name="watchlist">
      <field name="id" type="integer primary key" />
      <field name="notice_id" type="text foreign key" />
      <field name="status" type="text enum" example="new, review, bid, no-bid, submitted" />
      <field name="notes" type="text nullable" />
      <field name="created_at" type="datetime" />
    </table>
  </tables>

  <api_integration>
    <sam_opportunities>
      <purpose>Retrieve published active opportunities matching query parameters.</purpose>
      <implementation_notes>
        <note>Use pagination.</note>
        <note>Store raw JSON for debugging but map normalized fields into the opportunity table.</note>
        <note>Query by date range, NAICS, keyword, agency, and notice type when supported.</note>
        <note>Never hardcode API keys. Use .env.</note>
      </implementation_notes>
    </sam_opportunities>

    <usaspending>
      <purpose>Research historical awards for recompete/market intelligence.</purpose>
      <implementation_notes>
        <note>Use /api/v2/search/spending_by_award/ for award search.</note>
        <note>Filter by NAICS, PSC, agency, recipient, and award date where possible.</note>
        <note>Do not present recompete predictions as facts. Label them as inferred leads.</note>
      </implementation_notes>
    </usaspending>
  </api_integration>
</data_model_and_apis>
