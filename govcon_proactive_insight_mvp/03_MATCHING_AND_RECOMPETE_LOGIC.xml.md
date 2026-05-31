<matching_and_recompete_logic>
  <matching_score total="100">
    <rule points="25" name="naics_match">Exact NAICS match between profile and opportunity.</rule>
    <rule points="15" name="psc_match">Exact PSC match between profile and opportunity.</rule>
    <rule points="20" name="keyword_match">Keywords found in title, description, agency office, or notice text. Award partial credit by count and strength.</rule>
    <rule points="15" name="agency_match">Agency or office matches user target agencies.</rule>
    <rule points="10" name="set_aside_match">Set-aside aligns to profile eligibility/preferences.</rule>
    <rule points="10" name="deadline_health">Deadline is not expired and has enough time remaining. More points for 7-45 days remaining.</rule>
    <rule points="5" name="notice_type_fit">Sources Sought, RFI, RFQ, RFP, Combined Synopsis/Solicitation, etc. aligns to user preference.</rule>
  </matching_score>

  <match_explanation_examples>
    <example>+25 NAICS match: 541511</example>
    <example>+20 keyword match: dashboard, data governance, SharePoint</example>
    <example>+15 agency match: Department of the Navy</example>
    <example>-10 deadline risk: response due in less than 3 days</example>
  </match_explanation_examples>

  <recompete_inference>
    <goal>Identify contracts that may be candidates for future recompete based on historical award data.</goal>
    <inputs>
      <input>USAspending awards by NAICS/PSC/agency/recipient.</input>
      <input>Award base date, latest action date, period of performance start/end if available.</input>
      <input>Contract type, award amount, recipient, awarding agency, funding agency.</input>
    </inputs>
    <logic>
      <step>Search awards matching profile NAICS/PSC/agencies from the last 3-7 fiscal years.</step>
      <step>Prefer awards with period of performance end dates in the next 3-18 months.</step>
      <step>If no end date exists, infer rough recompete windows using award date plus common contract durations such as 1, 3, or 5 years. Clearly label as low confidence.</step>
      <step>Group similar awards by agency, incumbent, NAICS/PSC, and description.</step>
      <step>Generate a recompete lead record with confidence score and why it was flagged.</step>
    </logic>
    <confidence_levels>
      <level name="high">Has explicit period of performance end date in next 3-18 months and recurring procurement pattern.</level>
      <level name="medium">Has historical award pattern and likely contract duration, but incomplete end-date data.</level>
      <level name="low">Only keyword/agency similarity suggests possible future opportunity.</level>
    </confidence_levels>
  </recompete_inference>

  <guardrails>
    <guardrail>Do not imply inside knowledge.</guardrail>
    <guardrail>Do not claim an opportunity will definitely recompete unless public notice confirms it.</guardrail>
    <guardrail>Show source fields and confidence rating.</guardrail>
    <guardrail>Keep user-facing language conservative: “possible lead,” “watch item,” “inferred from historical award data.”</guardrail>
  </guardrails>
</matching_and_recompete_logic>
