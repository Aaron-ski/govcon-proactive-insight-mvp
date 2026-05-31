# GovCon Proactive Insight MVP — Codex Pack

Use these files as Codex instructions to build a locally hosted MVP that helps small/midsize contractors find relevant opportunities and possible recompete leads.

## Recommended way to use in Codex

Start one Codex chat with `01_MASTER_BUILD_SPEC.xml.md` and `05_CODEX_IMPLEMENTATION_TASKS.xml.md` first. Then add the remaining files as supporting context.

If Codex gets confused, create separate chats for:
1. Data/API layer
2. Scoring logic
3. UI/dashboard
4. Tests/README polish

## MVP goal

A local app where a user enters a company profile, pulls public SAM.gov opportunities, scores matches, saves a watchlist, and exports results.

## Important caveat

Recompete prediction should be treated as an inferred lead, not a fact. The app should always send the user back to official SAM.gov source records for validation.
