# WF-003 — Renova Content Generation
## Workflow Capture Document | June 5, 2026

> **Status:** Design Phase — Not Yet Tested
> **Automation Phase:** Phase 0 → Phase 1 (first test required)
> **Automation Score:** Not yet scored — test required before scoring
> **Depends on:** WF-001 (Renova Visual Training Platform) — quality standards defined there

---

## 1. Identity

| Field | Value |
|-------|-------|
| Workflow Name | Renova Content Generation |
| Trigger | A content request is received for Renova Builders (trade + platform + goal specified) |
| Desired Outcome | Social media content (image + caption) that passes quality review and is approved for publication by both Maor and Renova team |
| Human Role | Maor provides content brief, reviews image + caption, approves for publication |
| Agent Role | Claude designs content concept, generates image via Higgsfield, writes caption, assembles package for review |
| Frequency | Estimated: 4–12 pieces per month (Renova content calendar) |
| Business Division | MONA Digital Marketing (client services) |

---

## 2. Success Definition

> From Maor, Session 004: *"The actual success condition is NOT 'Review completed.' The actual success condition is: We can consistently generate social media content for Renova Builders that passes quality control and is approved for publication."*

A single piece of approved content = one successful test.

The workflow is **validated** when:
1. At least 3 pieces of content have been generated
2. Each has passed review by Maor AND been approved by the Renova team
3. The content is confirmed ready for real-world publication

Only after this does the workflow become standardized for automation consideration.

---

## 3. Required Inputs

| Input | Source | Required? |
|-------|--------|----------|
| Trade category | Renova / Maor | Required — determines visual standards (WF-001) |
| Platform | Maor | Required — Instagram vs. Facebook vs. LinkedIn have different formats |
| Content goal | Maor | Required — showcase work? educational? promotion? trust-building? |
| Project reference (if any) | Renova / Maor | Helpful — specific project photos or job details |
| Brand guidelines | WF-001 framework | Required — visual standards per trade |
| Caption tone preference | Maor | Helpful — formal vs. approachable vs. technical |

---

## 4. Required Tools & Access

| Tool / MCP | Purpose | Status |
|-----------|---------|--------|
| Higgsfield | Generate reference/hero images for social content | Available (MCP: 01635c4d) |
| Claude Code | Content concept, caption writing, creative direction | Available |
| GitHub repo | Storage and version control of approved content | Available |
| Gmail MCP | Deliver content package as Gmail draft for review | Available (draft only — Maor sends) |

*Future tools needed for Phase 2+:*
| HeyGen | Video content generation from script + avatar | PMA-007/008 pending |
| Canva MCP | Format images to platform specifications | Canva MCP available |
| Buffer / social scheduler | Auto-schedule approved posts | Phase 3 |

---

## 5. Step-by-Step Process (Proposed — Not Yet Tested)

| Step | Action | Owner | Notes |
|------|--------|-------|-------|
| 1 | Receive content brief (trade, platform, goal, any references) | Maor provides | Without a brief, content becomes generic |
| 2 | Identify relevant quality standard from WF-001 | Claude | e.g., "tile work, acceptable vs. unacceptable grout lines" |
| 3 | Define visual concept (scene, composition, lighting, perspective) | Claude | Must match the quality standard for that trade |
| 4 | Generate hero image via Higgsfield | Claude | Aim for publication-quality output |
| 5 | Evaluate image against WF-001 quality standard | Claude (self-check) | Does it show excellent work? Is it specific to Renova's trade style? |
| 6 | Write caption for specified platform | Claude | Platform-appropriate length, tone, CTA |
| 7 | Assemble content package for review | Claude | Image + caption + platform spec in one review document |
| 8 | Create Gmail draft for Maor review | Claude via Gmail MCP | Maor reviews package, approves or requests revision |
| 9 | Maor reviews and sends to Renova (if applicable) | Maor | Maor is the relationship owner |
| 10 | Capture outcome: approved / revised / rejected | Both | Feed back to WF-003 and WF-001 |

---

## 6. Decision Points

| Condition | If True | If False |
|-----------|---------|---------|
| Client supplies reference project photos | Use real photos as concept anchor for Higgsfield | Generate from trade quality standards in WF-001 |
| Platform is Instagram | Square or portrait format, visual-first, concise caption | Adjust format per platform spec |
| Content goal is "showcase work" | Show completed project, specific trade, high quality detail | Use different visual composition for trust/educational content |
| Generated image fails self-check | Regenerate with refined prompt | Proceed to caption step |
| Caption exceeds platform character limit | Edit for concision — prioritize the hook and CTA | Keep |
| Renova requests revision | Document what changed — add to WF-001 quality standards if a new standard is discovered | Archive as approved |

---

## 7. Quality Control Checks

| Check | Who Verifies | Pass Criteria |
|-------|-------------|--------------|
| Image matches the trade's quality standard (WF-001) | Claude (self-check before submission) | The image shows excellent work specific to that trade |
| Image is not generic — identifiable as Renova-quality work | Maor | Cannot be mistaken for a stock photo or a competitor's portfolio |
| Caption is platform-appropriate (length, tone, hashtags) | Claude self-check | Fits the platform. Hook is strong. CTA is clear. |
| Content does not make false claims | Claude self-check | No "best in class" or superlative language without substantiation |
| Package is complete before submission | Claude | Image + caption + platform spec all present |

---

## 8. Human Approval Points

| Approval Point | What Is Reviewed | Can It Be Removed? |
|---------------|-----------------|-------------------|
| Content brief | Maor confirms trade, platform, goal | No — determines all downstream output |
| Image review | Maor evaluates quality and brand fit | No — client-facing visual |
| Caption review | Maor evaluates tone, accuracy, CTA | No — client-facing copy |
| Renova team approval (when required) | Client approves before publication | No — client controls their brand |

---

## 9. Deliverables Produced

| Deliverable | Format | Destination |
|------------|--------|-------------|
| Hero image | PNG/JPG (Higgsfield output) | GitHub repo + Gmail draft |
| Social caption | Text (platform-specific) | Gmail draft |
| Content review package | Gmail draft | Maor for review |
| Approved content archive | GitHub repo | `Clients/Renova Builders/Content/[Date]-[Trade]-[Platform]/` |

---

## 10. Original Assumptions

*(To be filled after first test run)*

- Content generation using Higgsfield will produce sufficiently realistic construction imagery
- The visual standards from WF-001 are specific enough to guide Higgsfield prompt design
- A single review round will be sufficient for approval
- Platform-specific formatting can be handled without additional design tools

---

## 11. What Changed During Execution

*(To be filled after first test run)*

---

## 12. What Worked

*(To be filled after first test run)*

---

## 13. What Failed or Caused Friction

*(To be filled after first test run)*

---

## 14. What Surprised Us

*(To be filled after first test run)*

---

## 15. What Should Become Standard

*(To be filled after first test run)*

---

## 16. What Should Remain Human-Led

| Step | Why It Stays Human |
|------|-------------------|
| Content brief definition | Requires knowledge of client's current projects, campaign calendar, and goals |
| Final image approval | Visual quality judgment for client-facing content |
| Caption approval | Tone, accuracy, and brand fit for this specific client |
| Sending to Renova | Maor owns the relationship |

---

## 17. What Should Eventually Be Automated

| Step | Automation Approach | Phase |
|------|-------------------|-------|
| Image generation from brief | Scripted Higgsfield prompt template per trade category | Phase 2 |
| Caption generation from brief | Structured Claude prompt with brand voice + platform spec | Phase 2 |
| Content package assembly | Template auto-assembles image + caption into review format | Phase 2 |
| Approval workflow | Digital approval form replaces email review | Phase 3 |
| Scheduling | Auto-schedule approved content to social platforms | Phase 3 |

---

## 18. What Should Be Avoided

- Generating generic construction images that could belong to any contractor — content must be Renova-specific
- Skipping the WF-001 quality standard check before submitting for review
- Submitting content for approval before self-checking both image and caption
- Generating content without a brief — no brief means the output will be generic

---

## 19. Lessons Learned

*(To be filled after first test run — sections will be populated from execution)*

| Lesson | Routed To | Routing Status |
|--------|----------|---------------|
| *(pending first test)* | | |

---

## 20. Current Status

**Status:** Design Phase — workflow designed but not yet tested
**Blocking dependency for first test:** Need content brief from Maor (trade category + platform + specific project or general type)
**Next action:** Request content brief → run first test → document findings → update this file

---

## 21. Automation Candidate Scoring

*(Cannot score before testing — VALIDATE-001)*

| Dimension | Score (1–5) | Notes |
|-----------|------------|-------|
| Frequency | 3 | Estimated 4–12 pieces/month if workflow is validated |
| Business Value | 4 | Direct client deliverable — differentiates MONA as AI-powered content agency |
| Risk Level (inverse) | 4 | Low risk — Maor reviews before delivery |
| Tool Availability | 4 | Higgsfield available; HeyGen pending |
| Validation Status | 1 | Design only — not yet tested |
| **TOTAL** | **16/25 (estimated)** | |

**Recommended Phase:** Phase 0 → Phase 1 once first content piece is generated and reviewed

---

*Captured: June 5, 2026 | Session 004*
*Status: Design — first test required*
*First test requires: content brief from Maor (trade category + platform + goal)*
