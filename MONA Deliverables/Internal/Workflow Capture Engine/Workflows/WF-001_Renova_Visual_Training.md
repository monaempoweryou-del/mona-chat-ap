# WF-001 — Renova Visual Training Platform
## Workflow Capture Document | June 5, 2026

> **Status:** Tested Once
> **Automation Phase:** Phase 1 (Manual-Assisted)
> **Automation Score:** Not yet scored — requires additional testing runs

---

## 1. Identity

| Field | Value |
|-------|-------|
| Workflow Name | Renova Visual Training Platform |
| Trigger | Client (Renova Builders) needs to train field staff on visual standards for residential remodeling |
| Desired Outcome | A system that enables Renova staff to distinguish acceptable vs. unacceptable work quality across trades |
| Human Role | Maor defines the client need, reviews outputs, approves direction |
| Agent Role | Claude designs the review framework, builds the platform structure, generates training content |
| Frequency | One-time build per client — recurring when new trade categories are added |
| Business Division | MONA Digital Marketing (client services) |

---

## 2. Required Inputs

| Input | Source | Required? |
|-------|--------|----------|
| Client's quality standards or brand guidelines | Renova Builders | Required |
| Trade categories to cover | Renova Builders / Maor | Required |
| Sample images or references | Renova Builders (when available) | Helpful |
| Platform target (web, app, PDF) | Maor | Required |

---

## 3. Required Tools & Access

| Tool / MCP | Purpose | Status |
|-----------|---------|--------|
| Claude Code | Framework design, content generation | Available |
| Higgsfield / image generation | Reference image creation if client cannot supply | Available |
| HeyGen | Video training module potential | Available (PMA-007/008 pending) |
| GitHub repo | Storage and delivery | Available |

---

## 4. Step-by-Step Process (As Executed)

| Step | Action | Owner | Notes |
|------|--------|-------|-------|
| 1 | Client need described by Maor | Maor | Initial trigger |
| 2 | Claude interprets need and proposes framework | Claude | First interpretation was too narrow |
| 3 | Claude builds review/rating interface | Claude | Designed for image review |
| 4 | Maor tests with real content | Maor | Testing revealed true nature of the need |
| 5 | Framework redesigned as visual training system | Claude | Major pivot based on Step 4 discovery |
| 6 | Training content structured by trade category | Claude | More effective than pure review interface |
| 7 | Output delivered for Renova review | Both | |

---

## 5. Decision Points

| Condition | If True | If False |
|-----------|---------|---------|
| Client supplies reference images | Use client images as training anchors | Generate reference images or use descriptive standards |
| Reviewers are judging marketing content | Show publishable/shareable content | Show actual job-site reference material |
| New trade category added | Add module to existing framework | N/A |

---

## 6. Failure Points

| Failure | Cause | Current Workaround |
|---------|-------|-------------------|
| Wrong mental model of the end user | Assumed reviewers needed a tool — they needed training | Real-world testing revealed the actual need |
| Image availability | Client could not supply example images easily | Generate reference images or use descriptive standards |

---

## 7. Quality Control Checks

| Check | Who Verifies | Pass Criteria |
|-------|-------------|--------------|
| Does content distinguish acceptable vs. unacceptable? | Maor | A Renova field staff member can use it without explanation |
| Is it specific to Renova's trades? | Maor | No generic construction content — specific to their work |

---

## 8. Human Approval Points

| Approval Point | What Is Reviewed | Can It Be Removed? |
|---------------|-----------------|-------------------|
| Trade category list | Maor confirms scope | No — client-specific decision |
| Framework structure | Maor approves before content is built | Eventually reducible to a template check |
| Final output | Maor reviews before delivery to Renova | No — client-facing output |

---

## 9. Deliverables Produced

| Deliverable | Format | Destination |
|------------|--------|-------------|
| Visual Training Framework | HTML / Markdown | Renova Builders + MONA repo |

---

## 10. Original Assumptions

- We were building a tool for reviewing images (pass/fail judgment interface)
- The end users would be managers comparing photos to standards
- The primary output would be a review/rating system

---

## 11. What Changed During Execution

| Original Assumption | What Actually Happened |
|--------------------|----------------------|
| Image review tool | Visual training framework — teach staff what good looks like before they judge |
| Managers reviewing outputs | Field staff learning standards |
| Review interface (ratings, comments) | Training content organized by trade |

---

## 12. What Worked

- Using real-world testing (actual Renova content) to reveal the true need
- Pivoting quickly once the wrong mental model was identified
- Organizing by trade category made the content navigable and specific

---

## 13. What Failed or Caused Friction

- Initial design was built on an assumption about the end user that turned out to be wrong
- Time was spent building a review interface before validating whether that was the right format

---

## 14. What Surprised Us

- The difference between "reviewing" and "training" is fundamental — one assumes knowledge, the other builds it
- The correct output (training framework) was more valuable and more reusable than the original output (review tool)
- Renova became the test environment that revealed a system (Visual Training) rather than just a deliverable

---

## 15. What Should Become Standard

- **Test with real content before building the full system** — the test reveals the actual requirement
- **Ask: who uses this, and what do they already know?** — this determines whether to build a review tool or a training tool
- **Treat the first client build as the framework discovery session** — Renova is to Visual Training what Goldsmith is to BIE

---

## 16. What Should Remain Human-Led

| Step | Why It Stays Human |
|------|-------------------|
| Trade category definition | Requires client knowledge |
| Quality standard decisions | Requires domain expertise |
| Final content approval | Client-facing output |

---

## 17. What Should Eventually Be Automated

| Step | Automation Approach | Phase |
|------|-------------------|-------|
| Framework skeleton generation | Template → auto-populated with trade names + standard criteria | Phase 2 |
| Reference image generation | Higgsfield API auto-generates reference images per trade + quality level | Phase 2 |
| Content formatting | HTML/PDF output auto-generated from approved framework | Phase 3 |

---

## 18. What Should Be Avoided

- Building the full system before validating the use case with one real module
- Assuming the end user is a manager when field staff may be the actual audience
- Treating image review and visual training as the same problem

---

## 19. Lessons Learned

| Lesson | Routed To | Routing Status |
|--------|----------|---------------|
| Test with real content before building the full system | WCE README, VALIDATE-001 rule candidate | ✅ Documented |
| Identify end user's knowledge level before designing the interface | BIE Framework (owner understanding), WCE routing map | ✅ Documented |
| First client build = framework discovery, not just deliverable | WCE operating principle, MONA System Development Framework | ✅ Documented |

---

## 20. Current Status

**Status:** Tested Once
**Next action to advance:** Run the framework for a second client to confirm it generalizes. Capture lessons from that run.
**Blocking dependencies:** None — framework is documented and ready to reuse

---

## 21. Automation Candidate Scoring

*(Preliminary — not yet scored formally. Requires second test run.)*

| Dimension | Score (1–5) | Notes |
|-----------|------------|-------|
| Frequency | 2 | One-time per client, but new trade categories are added |
| Business Value | 4 | Differentiates MONA as a system builder, not just a content creator |
| Risk Level (inverse) | 4 | Low risk if output is wrong — Maor reviews before delivery |
| Tool Availability | 3 | Partial — HeyGen (video) not yet active |
| Validation Status | 2 | Tested once — not yet validated across multiple clients |
| **TOTAL** | **15/25** | |

**Recommended Phase:** Phase 1 (Manual-Assisted) — current status is appropriate

---

*Captured: June 5, 2026 | Session 003*
*Next update: After second visual training client run*
