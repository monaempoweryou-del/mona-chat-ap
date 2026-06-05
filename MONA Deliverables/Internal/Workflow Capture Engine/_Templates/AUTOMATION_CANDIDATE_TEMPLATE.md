# MONA WCE — Automation Candidate Evaluation
## Candidate ID: AC-[NUMBER] | Date: [Date]

> Complete this template only when a workflow has reached Tested Once or higher status.
> Do not evaluate automation for untested workflows — this violates VALIDATE-001.

---

## Workflow Identity

| Field | Value |
|-------|-------|
| Workflow Name | |
| Workflow File | `Workflows/WF-00N_...md` |
| Current Status | Tested Once / Tested Multiple / Validated |
| Current Manual Process | Describe how it runs today |
| Repetition Frequency | How often does this run? |

---

## Business Value Assessment

| Question | Answer |
|---------|--------|
| What business outcome does this produce? | |
| What happens if this doesn't run on time? | |
| How much Maor time does this currently consume? | |
| What is the revenue or client impact of this workflow? | |

---

## Automation Scoring

| Dimension | Score (1–5) | Rationale |
|-----------|------------|---------|
| Frequency | | How often does this run? 1=rarely, 5=weekly+ |
| Business Value | | Revenue/retention impact? 1=low, 5=high |
| Risk Level (inverse) | | Risk if auto fails? 1=high risk, 5=low risk |
| Tool Availability | | Are tools/MCPs ready? 1=none, 5=all available |
| Validation Status | | How proven? 1=observed only, 5=validated |
| **TOTAL** | **/25** | |

**Recommended Phase:** [Based on score — see README.md scoring table]

---

## What Can Be Automated Now

*(Steps in the current manual workflow that are mechanical, deterministic, and low-risk)*

| Step | Automation Approach | Tools Required |
|------|-------------------|---------------|
| | | |

---

## What Should Stay Manual

*(Steps that require Maor's judgment, creativity, or approval)*

| Step | Why It Stays Manual | Could It Be Automated Later? |
|------|-------------------|---------------------------|
| | | Yes / No / Maybe |

---

## What Must Be Validated First

*(Prerequisites before automation is safe to deploy)*

| Prerequisite | Status |
|-------------|--------|
| | Not started / In progress / Complete |

---

## Required Tools & Integrations

| Tool / MCP | Current Status | Gap |
|-----------|--------------|-----|
| | Available / PMA pending | |

---

## Human Approval Requirements

*(Points where Maor must review before the automated workflow continues)*

| Approval Point | Can It Be Removed? | Condition for Removal |
|---------------|-------------------|----------------------|
| | Yes / No | |

---

## Recommended Automation Roadmap

| Phase | Description | Timeline |
|-------|-------------|---------|
| Phase 0 → Phase 1 | [What changes] | [When] |
| Phase 1 → Phase 2 | [What changes] | [When] |
| Phase 2 → Phase 3 | [What changes] | [When] |
| Phase 3 → Phase 4 | [What changes] | [When — if ever] |

---

## Risk Assessment

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|-----------|
| | | | |

---

## Recommendation

**Recommended Phase:** [Phase number]
**Start automation:** [Immediately / After [condition] / Not yet]
**First automation step:** [Most specific, lowest-risk step to automate first]

---

## Approval Required

- [ ] Maor approval to proceed with automation — **REQUIRED before Phase 2+**
- [ ] Tool/MCP availability confirmed
- [ ] Validation checkpoint passed

---

*Created: [Date] | Session: [Number]*
