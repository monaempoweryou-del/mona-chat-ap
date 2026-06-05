# WF-002 — MONA Business Intelligence Engine
## Workflow Capture Document | June 5, 2026

> **Status:** Tested Once
> **Automation Phase:** Phase 1 (Manual-Assisted)
> **Automation Score:** Not yet scored — Goldsmith test in progress

---

## 1. Identity

| Field | Value |
|-------|-------|
| Workflow Name | MONA Business Intelligence Engine |
| Trigger | A new lead email arrives in the inbox (or is manually introduced to the session) |
| Desired Outcome | A prospect receives a deeply personalized business intelligence report + strategic recommendations + proposal that demonstrates MONA understands their business better than they expected — leading naturally toward engagement |
| Human Role | Maor introduces the lead email, reviews the Step 2 draft, sends outreach, reviews and sends the final report and proposal |
| Agent Role | Claude reads the email, extracts intelligence, identifies gaps, conducts research, drafts all communications, generates the report, proposal, and follow-up sequence |
| Frequency | Once per new lead — estimated 1–4 per month at current volume |
| Business Division | MONA Digital Marketing (new client acquisition) |

---

## 2. Required Inputs

| Input | Source | Required? |
|-------|--------|----------|
| Lead's initial email | Gmail inbox | Required |
| Lead's website URL | Lead email or research | Required |
| Lead's social profiles | Lead email or research | Required |
| Lead's Step 2 answers (goals, referral sources, prior agencies, compliance, 90-day vision) | Lead (via Step 2 email) | Required |
| Competitive landscape data | Web research | Required |

---

## 3. Required Tools & Access

| Tool / MCP | Purpose | Status |
|-----------|---------|--------|
| Gmail MCP | Read lead email, create draft replies | Available |
| WebSearch | Research website content, competitors, reviews, regulatory records | Available |
| WebFetch | Direct website content (when not blocked) | Available — often blocked for professional services |
| Claude Code | Analysis, report generation, proposal writing | Available |
| GitHub repo | Storage of execution documents | Available |

*Future tools needed for Phase 2+:*
| GSC MCP | SEO keyword data for lead's business | PMA-010 pending |
| GBP API | Google review and GBP data for lead | PMA-011 pending |
| Browser automation (Playwright) | Social media audit, website interaction | Mac Mini / PMA-005 pending |

---

## 4. Step-by-Step Process (Current Phase 1 Version)

| Step | Action | Owner | Notes |
|------|--------|-------|-------|
| 1 | Read full lead email thread via Gmail MCP | Claude | Extract all intelligence before asking anything |
| 2 | Build Lead Intelligence Profile from email | Claude | Identity, goals, digital footprint, tone assessment |
| 3 | Assess Step 2 email depth needed (adaptive) | Claude | Exceptional brief = 2-4 gap questions only |
| 4 | Draft Step 2 "Understand The Human" email | Claude | Only gap questions — personalized to their specific brief |
| 5 | Create Gmail draft for Maor review | Claude | Maor reviews + sends |
| 6 | Receive Step 2 responses | Maor (pastes into session) | No automation yet |
| 7 | Run research protocol (WebSearch + site: + regulatory) | Claude | All public sources — document every finding |
| 8 | Build NAP consistency audit across all directories | Claude | Flag every inconsistency |
| 9 | Map competitive landscape | Claude | Who ranks, who reviews well, where the opening is |
| 10 | Identify bottlenecks (Critical / Quick Win / Strategic) | Claude | What is blocking growth right now |
| 11 | Generate Business Intelligence Report (HTML) | Claude | Owner Profile + Reality + Gap Analysis + Bottlenecks + Competitors + Opportunities |
| 12 | Generate Strategic Recommendations | Claude | Max 7 items, each tied to stated goal |
| 13 | Build 90-Day Execution Plan | Claude | Quick Wins / Foundation / Growth Engine phases |
| 14 | Generate Proposal (HTML) | Claude | Services justified by findings, priced clearly |
| 15 | Draft 3-touch follow-up sequence as Gmail drafts | Claude | Day 2 / Day 7 / Day 14 |
| 16 | Maor reviews and sends the full package | Maor | Approval required before any client-facing output is sent |

---

## 5. Decision Points

| Condition | If True | If False |
|-----------|---------|---------|
| Lead provides exceptional brief | 2-4 targeted gap questions only | Full 7-question Understanding interview |
| Industry is regulated (financial, legal, medical) | Add compliance flag — check regulatory record + compliance constraints | Standard research protocol |
| Website blocks WebFetch (403) | WebSearch + site: query as primary research path | Use WebFetch content directly |
| Less than 2 indexed pages on site: query | Flag as Critical SEO issue — leads Section 4 bottleneck analysis | Proceed with content analysis |
| NAP inconsistency found | Document every discrepancy — becomes Quick Win recommendation | Note consistency as strength |
| No Google reviews found | Flag as Critical Gap — review generation strategy is always a recommendation | Analyze review sentiment and recency |
| Lead mentions prior marketing agency | Add "What worked/what failed" to Step 2 questions | Proceed with standard questions |

---

## 6. Failure Points

| Failure | Cause | Current Workaround |
|---------|-------|-------------------|
| WebFetch blocked (403) | Professional services sites use WAF/enterprise hosting | WebSearch + site: query as primary path |
| Gmail MCP cannot find thread | Spelling error in lead name, or email in non-inbox folder | Search by broader term (industry, partial name) |
| No social media data without browser | Social platforms block WebSearch/WebFetch for content details | Note as research gap — flag for browser-based session |
| Step 2 response not received | Lead hasn't replied | Proceed with research on available data; flag gap in report |
| Website has only 1 page indexed | Google cannot crawl the site | Critical finding — top-3 bottleneck guaranteed |

---

## 7. Quality Control Checks

| Check | Who Verifies | Pass Criteria |
|-------|-------------|--------------|
| Step 2 email sounds personalized, not templated | Maor (before sending) | Lead should feel we read every word they wrote |
| Research findings are evidence-based | Claude self-check | Every finding has a source — no assumptions presented as fact |
| Recommendations tie to stated goals | Claude self-check | Cannot recommend anything not traceable to the owner's goals |
| Proposal scope matches recommendations | Claude self-check | No services appear in the proposal that weren't in recommendations |
| Report reads as specific to this business | Maor (final review) | No paragraph could be copy-pasted to a different client |

---

## 8. Human Approval Points

| Approval Point | What Is Reviewed | Can It Be Removed? |
|---------------|-----------------|-------------------|
| Step 2 email draft | Tone, accuracy, question relevance | Eventually — once template is validated |
| Business Intelligence Report | Accuracy, completeness, tone | No — client-facing |
| Proposal (pricing, scope) | Scope and pricing decisions | No — financial decision |
| Follow-up sequence | Tone and timing | Eventually — once sequence is validated |

---

## 9. Deliverables Produced

| Deliverable | Format | Destination |
|------------|--------|-------------|
| Lead Intelligence Profile | Markdown | MONA repo (Clients/[Business]/) |
| Step 2 Understanding Email | Gmail draft | Lead's inbox (Maor sends) |
| Business Intelligence Report | HTML | monaempoweryou@gmail.com + lead (Maor sends) |
| Strategic Recommendations | HTML (within report) | Same |
| 90-Day Execution Plan | HTML (within report) | Same |
| Proposal | HTML | monaempoweryou@gmail.com + lead (Maor sends) |
| Follow-up sequence (3 drafts) | Gmail drafts | Staged for Day 2, 7, 14 |

---

## 10. Original Assumptions

- This started as a "Lead Onboarding Workflow" — 7 steps focused on collecting information
- The objective was framed as gathering information efficiently
- The first version had research come before understanding the owner
- Step 2 (Understanding) was a generic 5-question template

---

## 11. What Changed During Execution

| Original Assumption | What Actually Happened |
|--------------------|----------------------|
| Collect information efficiently | Understand the human deeply before researching anything |
| 7 steps: Lead → Research → Report | 9 steps: Lead → Understand The Human → Research → Intelligence → Strategy → Proposal → Follow-Up |
| Generic 5-question Step 2 template | Adaptive questioning based on what the email already answered |
| "Lead Onboarding Workflow" | "MONA Business Intelligence Engine" — reframeed entirely |
| Research happens before understanding | Understanding happens before research — understanding shapes what to look for |
| Gossmith Financial is the deliverable | Goldsmith Financial is the test environment — BIE is the deliverable |

---

## 12. What Worked

- Extracting maximum intelligence from the email before asking the lead for anything (HIM-001 applied to client intake)
- Identifying the exceptional brief as a category — not all leads are equal in information quality
- Adaptive questioning reduces friction for well-prepared leads
- Treating the lead's email tone as a signal for how to communicate back (Joshua's formality = formal, precise response)
- WebSearch as fallback for blocked WebFetch — effective for regulatory profiles, competitive research, directory presence

---

## 13. What Failed or Caused Friction

- WebFetch blocked on financial services site (goldsmithfinancial.net) — 403 error
- Social media content (post frequency, engagement quality) requires browser — cannot be accessed via current toolset in remote environment
- Website interior page content inaccessible — only homepage appears in Google index anyway (itself a critical finding)

---

## 14. What Surprised Us

- Joshua Goldsmith's email was one of the most detailed lead briefs received — it answered almost all standard questions before being asked
- Only 1 page of goldsmithfinancial.net is indexed by Google — a 20-year veteran firm with near-invisible web presence
- NAP inconsistency after a location move is extremely common and systematically overlooked by advisors
- A clean 20-year FINRA record is a major marketing asset that financial advisors almost never mention publicly
- The "Understand The Human" phase is more important than any research tool — knowing what Joshua believes the problem is shapes the entire report

---

## 15. What Should Become Standard

- **Read the email completely before designing Step 2 questions** — don't use a template if the answer is already in the email
- **Check `site:domain.com` early in research** — single-page indexing is the most common hidden SEO crisis
- **Add compliance flag automatically for regulated industries** — financial, legal, medical, real estate always have marketing constraints
- **NAP audit is always a first-check item** — compare Name/Address/Phone across every directory found
- **A clean regulatory record = marketing asset** — always surface it if it exists and the industry is regulated
- **Research tool hierarchy:** Gmail → WebFetch (try) → WebSearch (always works) → browser (Phase 2+)

---

## 16. What Should Remain Human-Led

| Step | Why It Stays Human |
|------|-------------------|
| Sending Step 2 email | Direct client communication — Maor reviews tone and accuracy |
| Sending the final report | Client-facing deliverable — Maor owns the relationship |
| Proposal pricing decisions | Commercial decision — Maor sets scope and price |
| Follow-up sequence sends | Relationship-sensitive timing decisions |

---

## 17. What Should Eventually Be Automated

| Step | Automation Approach | Phase |
|------|-------------------|-------|
| Lead email detection | Mission Zero: Gmail webhook or polling → auto-trigger | Phase 3 |
| Step 1 intelligence extraction | Template auto-populated from parsed email | Phase 2 |
| Research protocol execution | Scripted sequence of WebSearch calls per template | Phase 2 |
| Report HTML generation | COO pipeline: structured inputs → branded HTML report | Phase 2 |
| Gmail draft creation | Already partially automated (Gmail MCP) | Phase 1 |
| Follow-up sequence drafts | All three drafted at delivery time | Phase 1 (done) |

---

## 18. What Should Be Avoided

- Sending the same generic 5-question template to every lead regardless of brief quality
- Starting research before understanding what the owner believes is true about their business
- Skipping the NAP audit because "it seems fine" — always check
- Writing recommendations that could apply to any business (generic = trust killer for a sophisticated lead like Joshua)

---

## 19. Lessons Learned

| Lesson | Routed To | Routing Status |
|--------|----------|---------------|
| Understanding the human must precede research | BIE Framework Step 2, AGENT_ROUTING_MAP | ✅ Done |
| Adaptive questioning based on email quality | BIE Framework Step 1 Decision Table | ✅ Done |
| Financial services = compliance flag mandatory | BIE Framework Compliance Table, WCE Routing Map | ✅ Done |
| WebFetch blocked → WebSearch fallback | BIE Framework Research Blockers, Learning Engine candidate | 🔄 Pending |
| site:domain.com check → single-page index is a critical finding | BIE Framework Research Protocol | ✅ Done |
| NAP consistency check = always first-check item | BIE Framework Research Protocol | ✅ Done |
| Clean regulatory record = underused marketing asset | BIE Framework, Learning Engine candidate | 🔄 Pending |

---

## 20. Current Status

**Status:** Tested Once (Goldsmith Financial — in progress)
**Next action:** Receive Step 2 responses from Joshua → complete research → generate report
**Blocking dependencies:** Maor must send Step 2 Gmail draft (r3365570789961105155)

---

## 21. Automation Candidate Scoring

*(Preliminary — Goldsmith test still in progress)*

| Dimension | Score (1–5) | Notes |
|-----------|------------|-------|
| Frequency | 2 | 1–4 leads/month currently — higher as growth strategy executes |
| Business Value | 5 | Direct client acquisition — revenue impact is high |
| Risk Level (inverse) | 3 | Report sent to a prospect — moderate risk if poorly generated |
| Tool Availability | 3 | Core tools available; social media + browser research pending |
| Validation Status | 2 | Tested once — not yet validated |
| **TOTAL** | **15/25** | |

**Recommended Phase:** Phase 1 (current) → Phase 2 once Goldsmith delivers a successful outcome and pattern is validated

---

*Captured: June 5, 2026 | Session 003*
*Next update: After Goldsmith Financial Step 2 response received and research completes*
