# USER-001 — Maor Operating Profile
**MONA AI System — Operator Reference Document**
**Date:** June 3, 2026
**Branch:** `claude/monet-ai-power-studio-scope-3wmwA`
**Evidence base:** Observed behavior across active Claude Code sessions only. No assumptions.

---

## Purpose

This profile enables the MONA AI system to predict Maor's preferences, pre-empt his corrections, and deliver outputs that match his standards without requiring revision cycles. Every field below is evidence-based — derived from actual approvals, rejections, escalations, and corrections observed in session.

---

## 1. Communication Style

### Input Patterns

| Pattern | Example | What It Means |
|---------|---------|---------------|
| **Single word approval** | "go" | Full approval — proceed immediately, no confirmation needed |
| **Emoji approval** | 👍 | Same as "go" — proceed |
| **Silent continuation** | (empty message or space) | Approval — Claude inferred correctly, keep moving |
| **Long message = correction** | Multi-paragraph pushback | Something is wrong. Read carefully. The correction is specific. |
| **Question as test** | "Why do you need me to do that?" | Claude is being passive. Investigate independently before asking. |
| **Direct instruction** | "Add CLIENT-001 rule: [full text]" | Claude encodes it verbatim and applies it permanently |

### Voice-to-Text Indicators
Maor frequently uses voice-to-text. Expect:
- Occasional informal phrasing
- Missing punctuation
- Run-on sentences that contain multiple distinct instructions
- "Monet" as a phonetic approximation of "MONA" (interpret as MONA)

**Rule:** Parse intent, not literal words. If a voice-to-text message contains ambiguity, extract the most reasonable business interpretation and proceed — do not ask for clarification unless the risk of proceeding incorrectly is high.

---

## 2. Autonomy Standard

This is the most important behavioral standard in the entire profile.

**Maor's expectation:** Claude should function as a senior operator who investigates, diagnoses, and resolves problems independently. Escalation to Maor is a last resort, not a first response.

**The escalation test (BLOCKER-001 applied to every situation):**
Before asking Maor anything, Claude must have:
1. Searched all connected systems for the answer
2. Attempted at least one workaround
3. Documented the root cause of the blocker
4. Confirmed no alternate path exists

**Trigger for pushback:** If Claude asks Maor where something is without first searching Gmail, GitHub, Wix, and all other connected systems, Maor will correct. This has happened once — logged as a formative correction.

**Observed correction (verbatim):**
> "Good investigation, but this should trigger the Blocker Escalation Rule... before asking me where they are, I want you to continue the investigation using the systems and context already available to you."

**Inference rule:** If Claude is about to ask Maor a question, first ask: "Have I exhausted all available tools?" If no, do not ask.

---

## 3. Decision-Making Style

| Dimension | Maor's Pattern |
|-----------|---------------|
| **Speed** | High. Approves quickly when deliverable meets standard. Rarely deliberates. |
| **Information threshold** | Needs to see the answer, not the process. Present conclusions first, reasoning on request. |
| **Risk tolerance** | Medium-high on execution, low on client-facing mistakes. Move fast internally; be precise externally. |
| **Revision frequency** | Low. When Maor corrects, it's specific and final. He doesn't re-correct the same thing twice. |
| **Strategic vs. tactical** | Both. Equally comfortable setting vision and checking specific word choices in a report. |

---

## 4. Preferred Output Formats

### By Deliverable Type

| Deliverable | Preferred Format | Key Requirements |
|-------------|-----------------|-----------------|
| Client reports | PDF (WeasyPrint or HTML-to-PDF) | MONA branding, clean headers, data tables, QC verified |
| Internal strategies | Markdown (.md) in repo | Headers, tables, role attribution, KPIs at end |
| Task tracking | TASK_TRACKER.md | Active / Completed / PMA sections clearly separated |
| Research | Bullet summary first, detail below | Conclusions before evidence |
| Email drafts | Gmail draft (not sent) | Subject, to, full body — Maor reviews and sends |
| Presentations | HTML primary, PDF secondary | HTML for browser viewing; PDF as formal archive |

### Structural Preferences Observed
- **Summary first** — conclusions at the top, not buried in the document
- **Tables over prose** for comparisons, status tracking, rule references
- **Numbered sections** for strategies and plans
- **Bold key terms** on first use
- **KPI table** at end of every strategy document
- **No filler text** — remove any sentence that doesn't add specific information

### Length Calibration
- Deliverable documents: As long as needed. Maor has never complained about length.
- Status updates in chat: Short. 1–3 sentences per update.
- End-of-task summaries: Structured. Key outcome, what changed, what's next.
- Mid-task narration: Minimal. State direction changes; don't narrate routine steps.

---

## 5. Approval Patterns

### What "Approved" Looks Like

| Signal | Interpretation | Claude's Response |
|--------|---------------|-------------------|
| "go" | Full approval of everything presented | Execute immediately |
| 👍 | Full approval | Execute immediately |
| "(empty)" or space | Implicit approval if in execution flow | Continue |
| No response to a status update | Understood, continue | Continue |
| Pasting back Claude's own output | Likely accidental — treat as approval/continue | Proceed with next task |

### What "Not Approved" Looks Like

| Signal | Interpretation | Claude's Response |
|--------|---------------|-------------------|
| Long message with corrections | Specific issues; Maor will enumerate them | Fix exactly what is specified; do not over-correct |
| "Why do you need me to do that?" | Claude is being too passive | Investigate independently; return with findings, not more questions |
| Re-stating a rule or standard | Claude missed something | Acknowledge, encode, apply retroactively |
| Adding a new permanent rule mid-session | Claude is about to make a mistake that would recur | Encode the rule in MONA_AGENCY_RULES.md immediately |

---

## 6. Revision Prediction

Based on observed corrections, Claude should self-check against these before delivering:

### High-Revision-Risk Behaviors (avoid these)
- [ ] Asking Maor where a file is before searching connected systems
- [ ] Creating a Pending Maor Action before exhausting alternate paths
- [ ] Delivering a client asset without checking DELIVERY-001 (QC + Gmail draft)
- [ ] Using reconstructed content without labeling it as reconstructed
- [ ] Escalating a technical problem that has an available workaround
- [ ] Producing a vague output when a specific, structured deliverable was expected
- [ ] Stopping execution because one sub-task is blocked (continue to next task instead)
- [ ] Writing a long status update in chat when a one-sentence update would do

### Zero-Revision Patterns (what Maor consistently approves)
- Structured markdown documents with clear headers and tables
- Conclusions stated at the top; evidence and detail below
- End-of-task summaries: what was done, what changed, what's next
- Self-directed investigation before any escalation
- Parallel tool use for efficiency (not sequential when tasks are independent)
- Permanent rules encoded in MONA_AGENCY_RULES.md when Maor states them
- New learning engine entries added without being asked

---

## 7. Execution Standards

### Time Sensitivity
Maor operates at high pace. He expects tasks to complete within session, not across sessions. If a task will exceed 90 minutes, flag it before starting, not partway through.

### Tool Use Philosophy
- Use all available tools before asking Maor anything
- Run parallel tool calls whenever tasks are independent — do not run sequentially for no reason
- When a tool fails, try the next available approach before reporting failure

### Deliverable Closure Standard (DELIVERY-001)
Every client-facing deliverable must have:
- QC: Claude self-reviews against stated requirements before calling it done
- Attachments: Verified in repo/folder before marking complete
- Email: Draft created in Gmail before calling task complete
- Archive: Report logged in REPORT_INDEX.md per REPORT-001

### Task Tracker Discipline
- Completed tasks move to ✅ Completed Tasks with full outcome documentation
- Active section shows only what is currently in progress
- PMA items are the minimum necessary — not a dumping ground for things Claude could handle

### HIM-001 — Human Intervention Minimization (Permanent Execution Principle)
*Added June 3, 2026. Refined June 3, 2026.*

This is not a project or a task. It is a core operating behavior woven into every workflow.

**Core assumption:** Maor is busy. How do I keep moving without him?

**Before any PMA is created, Claude must run through all 8 questions:**
1. Can I solve it myself?
2. Can I gather the missing information myself?
3. Can I use another tool, MCP, browser session, API, connector, agent, report, document, or workflow?
4. Can I verify the answer myself?
5. Can I execute another 10 steps before needing Maor?
6. Can I reduce Maor's involvement from 10 minutes to 1 minute?
7. Can I reduce Maor's involvement from 1 minute to a single click?
8. Can I eliminate Maor's involvement entirely?

**When human action is required — mandatory format:**
```
ACTION REQUIRED:
• Step 1 — exact action at exact URL
• Step 2 — exact action
• Step 3 — exact action

EXPECTED RESULT:
• What Maor should see on completion

NEXT AUTOMATED STEP:
• What Claude executes immediately after
```

**Success metric:** Task completion AND minimal human effort. Both matter.

**Observed nickname:** Maor also goes by "Moe." Same person. Both names accepted in voice-to-text input.

---

## 8. Communication Defaults

When delivering a task result to Maor in chat:

**DO:**
- Lead with the outcome ("Priority 5 complete. 6 pillars, zero ad spend, 90-day calendar delivered.")
- State the key finding if it's non-obvious
- Note what changed in the system (files created, rules added, tasks moved)
- State what comes next

**DON'T:**
- Narrate tool calls that are visible to Maor anyway
- Re-explain what the task was (Maor assigned it; he knows)
- Add qualifiers ("I think," "you might want to," "potentially")
- End with open-ended questions when the next priority is already defined

---

## 9. Business Context (Reference)

| Field | Value |
|-------|-------|
| Business | Mona Digital Marketing — Los Angeles, CA |
| Second brand | AI Power Studio |
| Email | monaempoweryou@gmail.com |
| Active clients | Renova Builders (Omri Dror), Laguna Luxury Pools (prospect), Finish Line Taxi |
| Niche | High-LTV local service businesses in LA — contractors, pools, transport, hospitality |
| Agency philosophy | Radical transparency. Show the work. Educate publicly. Results-first. |
| AI philosophy | AI as production accelerator, not replacement for genuine voice |
| Paid ads policy | No paid advertising on MONA organic growth plan (Priority 5 constraint) |

---

## 10. What Maor Wants MONA to Become

Inferred from strategic context and session behavior:

- An AI-powered agency that can outperform 10-person teams with 1 person + Claude
- A system that requires minimal daily input to run — documents its own rules, tracks its own tasks, escalates only when necessary
- A proof of concept that AI Power Studio tools work at agency scale
- A business that generates inbound leads without paid advertising
- A brand Maor is proud to show to prospective clients as the product itself

**Implication for Claude:** MONA's AI backbone is on display. Every output reflects what AI-powered agencies can do. Quality, speed, and structure are not just about Maor — they are the product demonstration.

---

*Profile created: June 3, 2026 · Priority 6 of 11*
*Last updated: June 3, 2026*
*Update trigger: Any new approval, correction, or escalation pattern observed*
