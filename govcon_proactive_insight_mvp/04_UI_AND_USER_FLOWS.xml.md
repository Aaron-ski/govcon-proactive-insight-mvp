<ui_and_user_flows>
  <pages>
    <page name="Dashboard">
      <component>Summary cards: active matches, due in 7 days, saved watchlist, recompete leads.</component>
      <component>Top matches table sorted by score.</component>
      <component>Filters: agency, NAICS, PSC, set-aside, deadline, score threshold.</component>
    </page>

    <page name="Company Profile">
      <component>Form for company name, NAICS, PSC, keywords, agencies, set-asides, value range.</component>
      <component>Save/update profile button.</component>
      <component>Seed profile for IT consulting/data/dashboard/AI/knowledge management.</component>
    </page>

    <page name="Opportunity Detail">
      <component>Title, agency, office, notice type, deadline, SAM.gov link.</component>
      <component>Match score with explanation bullets.</component>
      <component>Action checklist.</component>
      <component>Watchlist status and notes.</component>
    </page>

    <page name="Recompete Leads">
      <component>Table of possible future recompetes from USAspending/historical awards.</component>
      <component>Confidence rating and basis for inference.</component>
      <component>Incumbent, agency, NAICS/PSC, amount, award date, end date if available.</component>
    </page>

    <page name="Exports">
      <component>Download CSV for matches.</component>
      <component>Download CSV for watchlist.</component>
      <component>Download CSV for recompete leads.</component>
    </page>
  </pages>

  <primary_user_flow>
    <step>Open local app.</step>
    <step>Create or edit company profile.</step>
    <step>Click “Refresh Opportunities.”</step>
    <step>App calls SAM.gov API and stores opportunities.</step>
    <step>App scores opportunities against profile.</step>
    <step>User reviews top matches and saves promising ones to watchlist.</step>
    <step>User exports CSV for follow-up.</step>
  </primary_user_flow>

  <stretch_user_flow>
    <step>User clicks “Find Recompete Leads.”</step>
    <step>App queries USAspending awards by agency/NAICS/PSC/keywords.</step>
    <step>App groups historical awards and flags possible upcoming recompetes.</step>
    <step>User reviews leads and manually validates in SAM.gov.</step>
  </stretch_user_flow>

  <design_requirements>
    <requirement>Use plain language for non-expert users.</requirement>
    <requirement>Every opportunity card should answer: What is it? Why does it match? When is it due? What should I do next?</requirement>
    <requirement>Use warning labels for inferred recompete leads.</requirement>
    <requirement>Mobile-friendly layout preferred but not required for MVP.</requirement>
  </design_requirements>
</ui_and_user_flows>
