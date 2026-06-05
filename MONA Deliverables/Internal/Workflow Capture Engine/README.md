# MONA Workflow Capture Engine — v1.0
## June 5, 2026

> **Purpose:** Observe how MONA manually solves business problems. Identify repeatable patterns. Document them. Validate them. Convert them into standard operating procedures and, where appropriate, automation.
>
> **Core principle:** The deliverable is not only the output. The deliverable is the proven workflow that created the output.

---

## What This Is

Every time Maor, Claude, or any MONA agent works through a business task, a workflow is being discovered — even if it doesn't feel that way in the moment. The Workflow Capture Engine (WCE) is the system that makes those discoveries permanent.

Without WCE: MONA solves the same problems repeatedly, from scratch.
With WCE: MONA solves a problem once, documents the process, and repeats it faster — until it can be automated.

**Individual workflows create client deliverables.**
**The Workflow Capture Engine creates MONA's operating intelligence.**

---

## What This Is Not

- Not a documentation exercise
- Not bureaucracy for its own sake
- Not a replacement for doing the work
- Not theory — every captured workflow must have at least one real-world test

---

## Architecture

```
Workflow Capture Engine/
├── README.md                        ← This file. Architecture overview.
├── WORKFLOW_STATUS_TRACKER.md       ← Master list of all captured workflows + current status
├── AGENT_ROUTING_MAP.md             ← Which lesson types go to which agents
│
├── _Templates/                      ← Blank templates for new captures
│   ├── WORKFLOW_CAPTURE_TEMPLATE.md
│   ├── LESSON_EXTRACTION_TEMPLATE.md
│   ├── RULE_PROPOSAL_TEMPLATE.md
│   ├── AGENT_TRAINING_UPDATE_TEMPLATE.md
│   └── AUTOMATION_CANDIDATE_TEMPLATE.md
│
└── Workflows/                       ← One file per captured workflow
    ├── WF-001_Renova_Visual_Training.md
    ├── WF-002_Business_Intelligence_Engine.md
    └── WF-00N_[Next workflow].md
```

---

## The 13-Step WCE Operating Loop

Every workflow passes through this cycle:

| Step | Action | Who |
|------|--------|-----|
| 1 | Human executes or directs a task manually | Maor |
| 2 | System observes the task and session | Claude |
| 3 | System identifies the workflow emerging from the work | Claude |
| 4 | System separates one-time details from repeatable process | Claude |
| 5 | System captures assumptions made, corrections required, decisions taken | Claude |
| 6 | System identifies what worked and what failed or caused friction | Claude |
| 7 | System proposes a clean, reusable workflow document | Claude |
| 8 | Human validates or corrects the proposed workflow | Maor |
| 9 | System documents the approved workflow to Workflows/ | Claude |
| 10 | System routes lessons to relevant agents and updates Agent Routing Map | Claude |
| 11 | System identifies automation opportunities embedded in the workflow | Claude |
| 12 | System recommends: automate now / automate later / stay manual / discard | Claude |
| 13 | Workflow joins MONA's operating system — referenced in future sessions | Ongoing |

---

## Workflow Status Definitions

| Status | Definition |
|--------|-----------|
| **Observed** | Workflow happened but not yet formally documented |
| **Drafted** | Template filled — not yet tested with real-world use |
| **Tested Once** | Run once in a live context — first real-world observations recorded |
| **Tested Multiple Times** | Run 2+ times. Patterns are stable. Variations documented. |
| **Validated** | Workflow produces consistent, high-quality output. Ready to standardize. |
| **Standardized** | Approved by Maor. Part of MONA's official operating process. |
| **Automation Candidate** | Validated + automation scored. Awaiting phase assignment. |
| **Automated** | Some or all steps are handled by system without manual trigger. |
| **Deprecated** | Superseded by a better workflow. Retained for historical reference. |

---

## Automation Phase Definitions

| Phase | Name | Description |
|-------|------|-------------|
| 0 | Do Not Automate | Workflow not stable enough or too complex/risky to automate |
| 1 | Manual-Assisted | Claude executes workflow within an active session — Maor triggers manually |
| 2 | Semi-Automated | Some steps automated (e.g., research, drafting), some require manual trigger |
| 3 | Human-Approved Automation | Workflow runs automatically but stops for Maor approval before output is sent |
| 4 | Fully Automated | End-to-end automated. Runs without Maor present. Output delivered autonomously. |

---

## Automation Candidate Scoring

Rate each dimension 1–5. Score = sum of all ratings.

| Dimension | 1 | 3 | 5 |
|-----------|---|---|---|
| **Frequency** | Happens rarely (<1/month) | Monthly | Weekly or more |
| **Business Value** | Low impact | Moderate impact | Directly drives revenue or client retention |
| **Risk Level** (inverse — higher risk = lower score) | High risk if automation fails | Moderate | Low risk — recoverable if automation fails |
| **Tool Availability** | Tools don't exist yet | Tools partially available | All required tools/MCPs connected |
| **Validation Status** | Observed only | Tested once | Validated across multiple runs |

**Score thresholds:**
- **5–12:** Phase 0 — Do not automate yet
- **13–17:** Phase 1 — Manual-assisted
- **18–20:** Phase 2 — Semi-automated
- **21–23:** Phase 3 — Human-approved automation
- **24–25:** Phase 4 — Fully automated

---

## Operating Principles

1. Do not automate chaos. Stabilize the workflow first.
2. Do not document noise. Only capture patterns that repeat.
3. Do not turn every idea into a rule. Evidence required.
4. Separate one-time decisions from repeatable patterns before documenting.
5. A workflow must survive real-world testing before becoming standard.
6. A standard must be validated before becoming automation.
7. Human approval remains required for all client-facing output unless explicitly removed.
8. The purpose is to reduce Maor's workload — not create more review work.
9. Every workflow should eventually answer: **repeat, revise, automate, or discard?**
10. If a lesson only applies once, it's a note — not a workflow capture.

---

## Relationship to Other MONA Systems

| System | Relationship |
|--------|-------------|
| MONA_AGENCY_RULES.md | Validated WCE workflows produce candidates for permanent rules |
| TASK_TRACKER.md | WCE discoveries may create new PMAs or activate blocked tasks |
| HIM-001 | WCE is the mechanism that surfaces automation opportunities for HIM-001 |
| VALIDATE-001 (candidate rule) | Core principle behind WCE: test before automating |
| MONA_System_Development_Framework | WCE is the implementation layer for that framework |
| DELIVERABLES-001 | WCE workflow files are deliverables — stored and indexed per DELIVERABLES-001 |

---

*Created: June 5, 2026 | Session 003*
*Status: Active — add new workflow files to Workflows/ after each major project session*
