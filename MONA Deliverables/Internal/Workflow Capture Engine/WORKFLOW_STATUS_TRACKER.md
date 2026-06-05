# MONA Workflow Capture Engine — Status Tracker
## Master index of all captured workflows

> Updated after every major project session.
> Governed by WCE README.md operating principles.

---

## Active Workflows

| ID | Workflow Name | Status | Automation Phase | Last Updated | File |
|----|--------------|--------|-----------------|-------------|------|
| WF-001 | Renova Visual Training Platform | Tested Once | Phase 1 | June 5, 2026 | `Workflows/WF-001_Renova_Visual_Training.md` |
| WF-002 | MONA Business Intelligence Engine | Tested — Advanced | Phase 1 | June 5, 2026 | `Workflows/WF-002_Business_Intelligence_Engine.md` |

---

## Workflow Pipeline

### Phase 0 — Observed (not yet documented)
*Add workflows here when a pattern is noticed but not yet captured formally.*

| Workflow | Notes |
|---------|-------|
| Client Proposal Generation | Happens via COO pipeline — needs formal capture |
| Monthly Client Reporting | Manual, no trigger — high automation candidate |
| Gmail Draft → Client Delivery | Currently manual (Maor sends) — needs capture |

---

### Phase 1 — Manual-Assisted (active)
| ID | Workflow | Next Action |
|----|---------|------------|
| WF-001 | Renova Visual Training | Second real-world test to validate — success condition: approved publishable content |
| WF-002 | Business Intelligence Engine | Goldsmith step 2 reply pending → deliver report → capture final lessons → update WF-002 score |

---

### Validation Queue
*Workflows that have been tested and are ready for Maor review/approval.*

*(Empty — add items here when workflows reach Tested Multiple Times status)*

---

### Automation Candidates
*(Workflows that have been validated and scored for automation)*

| ID | Workflow | Automation Score | Recommended Phase |
|----|---------|-----------------|------------------|
| — | Monthly Client Reporting | Not yet scored | Estimated Phase 3 |
| — | Gmail Draft Creation | Not yet scored | Estimated Phase 2 |

---

## Deprecated Workflows

| ID | Workflow | Superseded By | Date |
|----|---------|--------------|------|
| — | Lead Onboarding Workflow (7-step) | WF-002 Business Intelligence Engine | June 5, 2026 |

---

---

## Autonomy Notes (Added Session 004)

| Workflow | Current Autonomous Capability | Remaining Human Touchpoints |
|---------|------------------------------|---------------------------|
| WF-002 BIE | Steps 1–9 executable autonomously | (1) Send Step 2 email — Gmail MCP cannot send, draft only. (2) Approve BIE report before client delivery. (3) Set proposal pricing and scope. |
| WF-001 Visual Training | Framework design and content generation | (1) Client approves trade category list. (2) Maor approves output before delivery. (3) Images require Higgsfield API access (available). |

*Last updated: June 5, 2026 | Session 004*
