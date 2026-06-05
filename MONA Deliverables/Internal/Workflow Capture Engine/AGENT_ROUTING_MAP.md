# MONA WCE — Agent Lesson Routing Map

> When a lesson is extracted from a workflow, this map determines which agents and systems receive the update.
> A lesson that goes nowhere changes nothing. Route deliberately.

---

## Routing Logic

Ask two questions for every lesson:
1. Which agent will encounter this situation again?
2. Would that agent's behavior be different if it knew this lesson?

If yes to both: route it. If the lesson is only relevant to a one-time context: note it in the workflow file but do not route globally.

---

## Agent Routing Table

| Lesson Category | Route To | Why |
|----------------|---------|-----|
| Research methodology (web, social, regulatory) | Business Intelligence Agent · All research-capable agents | Prevents repeating the same failed research paths |
| Client communication tone and framing | Mona Intake Agent · COO Agent | Affects how requests are received and processed |
| Content production (scripts, captions, platform formats) | Content Machine workflows · HeyGen agent | Improves content quality and format compliance |
| Platform or tool behavior (API quirks, 403s, rate limits) | All agents using that tool | Prevents agents from re-learning tool limitations |
| Compliance and regulatory constraints | All client-facing agents | Prevents compliance violations across all client work |
| Workflow failures and friction points | The specific workflow agent + Systems Analyst | Fixes root causes, not just symptoms |
| Maor approval patterns and preferences | USER-001 Operating Profile | Reduces revision cycles |
| Automation opportunities | Systems/Infrastructure planning · HIM-001 tracker | Feeds the automation roadmap |
| Lesson about understanding before acting | All intake-stage agents · BIE Agent | Core operating principle |
| Data and research quality | BIE Agent · Reporting Agent | Improves accuracy of all analysis |
| Naming, address, and NAP standards | BIE Agent · Local SEO workflows | Prevents standard audit gaps from being missed |

---

## Destination Definitions

| Destination | Location | Update Method |
|------------|---------|--------------|
| MONA_AGENCY_RULES.md | Repo root | Add to Learning Engine table + propose formal rule if durable |
| USER-001 Operating Profile | `Internal/Systems/MONA_USER001_Maor_Operating_Profile.md` | Update relevant section |
| BIE Framework | `Internal/Systems/MONA_Business_Intelligence_Engine_Framework_June2026.md` | Add to Framework Discoveries table |
| WCE Workflow file | `Workflow Capture Engine/Workflows/WF-00N_...md` | Update Lessons Learned section |
| HIM-001 Metrics | `Internal/Systems/HIM001_Metrics.md` | Update if lesson affects Maor action count |
| Agent prompt (app.py) | `/home/user/mona-chat-ap/app.py` | Propose as PROPOSED CHANGE — requires approval |
| TASK_TRACKER.md | Repo root | Add PMA if lesson surfaces an unresolved blocker |

---

## Routing Examples

**Lesson:** Financial services websites block WebFetch — use WebSearch + site: query as fallback.
- Route to: BIE Framework (research protocol) ✅ Done in Session 003
- Route to: Learning Engine in MONA_AGENCY_RULES.md → *not yet added*
- Route to: Any future agent that conducts web research on regulated industries

**Lesson:** Owner understanding must precede business research.
- Route to: BIE Framework (Step 2 added before Step 3) ✅ Done in Session 003
- Route to: Mona Intake Agent (PROPOSED — would need app.py change)
- Route to: USER-001 profile (Maor's operating preference)

**Lesson:** A workflow built through theory alone is incomplete — test first.
- Route to: VALIDATE-001 rule (candidate — pending approval)
- Route to: WCE README operating principles ✅ Done
- Route to: All future workflow planning contexts

---

## Routing Cadence

| When | Action |
|------|--------|
| End of every major project session | Extract lessons → route per this map |
| When a workflow reaches Validated status | Route any remaining un-routed lessons |
| When a new agent prompt is written | Check all un-routed lessons for relevant updates |
| During Lessons Learned Audit (Priority 10 template) | Full routing review for accumulated lessons |

---

*Created: June 5, 2026 | Session 003*
