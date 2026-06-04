# MONA Agency — Permanent Rules & Standards

> These rules govern how Claude Code operates as the AI backbone of Mona Digital Marketing.
> Rules are permanent until explicitly revised by Maor.

---

## MASTER-001 — Rule Completeness Standard

**Effective:** June 4, 2026

Every rule in this system — agent instructions, code behavior, automation workflows, folder organization, reporting, browser, deliverables, scheduling — must define all five components before it is considered complete:

| Component | Definition |
|-----------|-----------|
| **Trigger** | What activates this rule? What event, condition, or action causes it to run? |
| **Timing** | When exactly does it run? Before task completion? On file creation? On session start? |
| **Scope** | Where does it apply? Which workflows, agents, file types, clients, or systems? |
| **Action** | What exactly happens? Specific steps, destinations, outputs. |
| **Failure Handling** | What happens if it cannot complete? Fallback behavior, labels, escalation path. |

**A rule without a trigger is incomplete. An incomplete rule is not a rule — it is a note.**

When creating or editing any rule, fill all five fields. If a field genuinely does not apply, state why explicitly — do not omit it silently.

**Retroactive application:** Existing rules (HIM-001 through BROWSER-001) will have MASTER-001 components added during the next scheduled Lessons Learned Audit.

---

## DELIVERABLES-001 — Claude Deliverables Center

**Effective:** June 4, 2026

### Trigger
Any time Claude creates, exports, downloads, edits, generates, or receives a deliverable file — including reports, proposals, invoices, PDFs, HTML files, images, video files, strategy documents, audits, or any other output intended for use, review, or delivery.

### Timing
Immediately before marking the task complete. File placement is a prerequisite for task closure, not an optional final step.

### Scope
All deliverable files across all MONA workflows:
- Client deliverables (Renova, Laguna, Finish Line Taxi, any new client)
- Internal strategy, audits, systems, and brand documents
- AI Power Studio deliverables
- Applies in all Claude Code sessions, local and remote

### Action

**In-session (remote environment):**
Save to the repo under `MONA Deliverables/` using the correct STORAGE-001 subfolder. Log in `MONA Deliverables/REPORT_INDEX.md`. Push to branch. File becomes available locally via:
```bash
git pull origin claude/monet-ai-power-studio-scope-3wmwA
```

**Local Desktop target structure (synced via git pull):**
```
Desktop → 📦 CLAUDE DELIVERABLES
├── Clients/
│   ├── Renova Builders/
│   ├── Laguna Luxury Pools/
│   └── Finish Line Taxi/
├── Internal/
│   ├── Strategy/
│   ├── Audits/
│   ├── Systems/
│   └── Brand/
└── Archive/
```

This mirrors `MONA Deliverables/` in the repo exactly.

### Failure Handling

| Failure Condition | Action |
|------------------|--------|
| Correct subfolder is unclear | Place in closest matching division. Prefix filename with `[REVIEW_LOCATION]_`. Log in REPORT_INDEX.md with note: "Location flagged for review." |
| Git push fails (network) | Retry up to 4× with exponential backoff (2s, 4s, 8s, 16s). If all fail, preserve to `/tmp/` and log the path in server output. |
| REPORT_INDEX.md update fails | Complete the file save first. Add REPORT_INDEX entry at next available opportunity. Never skip the file save waiting for the index. |
| File format unsupported | Save in the available format, note the intended format in the REPORT_INDEX entry. |

---

## DELIVERABLES-001A — Ownership Metadata Standard

**Effective:** June 4, 2026
**Parent rule:** DELIVERABLES-001

### Purpose

Storage location alone is not sufficient for organizational memory. Every deliverable must carry ownership metadata so future audits, reporting, search, analytics, and workflow tracking can answer instantly:
- Which agent created this?
- Which workflow produced it?
- Which business owns it?
- Which project requested it?
- Where is it stored?

DELIVERABLES-001 is the file storage rule. DELIVERABLES-001A is the memory layer on top of it.

### Trigger

When REPORT_INDEX.md is updated — meaning any time DELIVERABLES-001 fires and a new entry is appended.

### Timing

Immediately after file creation and before task completion. Metadata entry is written in the same operation as the REPORT_INDEX table entry — not deferred.

### Scope

Every entry in REPORT_INDEX.md. Applies to all deliverable types: client, internal, brand, archive.

### Action

For every deliverable logged in REPORT_INDEX.md, append a metadata block to the **Metadata Registry** section using this exact format:

```
**[Filename]**
Timestamp:         YYYY-MM-DD HH:MM (UTC)
Business Owner:    [Mona Digital Marketing | AI Power Studio | Client Name]
Client / Project:  [client name or internal project name]
Deliverable Type:  [Report | Audit | Strategy | Invoice | Proposal | Logo | etc.]
Producing Agent:   [agent role(s) that created this]
Workflow:          [task or priority name that generated this]
File:              [relative path in MONA Deliverables/]
Status:            [Complete | Review Required | Pending Delivery | Archive]
```

### Failure Handling

| Failure Condition | Action |
|------------------|--------|
| Business owner unknown | Mark as `[REVIEW_OWNER]` — do not silently guess |
| Producing agent unknown | Mark as `[REVIEW_AGENT]` |
| Workflow name unknown | Mark as `[REVIEW_WORKFLOW]` |
| Status unclear | Default to `Review Required` |

Never omit a field. Never leave it blank. Use the `[REVIEW_X]` prefix to flag uncertainty explicitly.

---

## HIM-001 — Human Intervention Minimization

**Effective:** June 3, 2026
**Refined:** June 3, 2026

### Core Principle

**Maor's time is the most expensive resource in the system.**

The goal is not simply to delay human intervention. The goal is to minimize Maor's labor throughout the entire system.

The operating assumption at all times: **"Maor is busy. How do I keep moving without him?"**

Success is measured not only by task completion, but by how little human effort was required to achieve it.

### Mandatory Thought Process Before Any Escalation

Before presenting Maor with any request, question, blocker, approval, decision, or action item, run through this checklist in order:

1. **Can I solve it myself?**
2. **Can I gather the missing information myself?** (search connected systems, read files, call APIs, use MCP tools)
3. **Can I use another tool, MCP, browser session, API, connector, agent, report, document, or workflow?**
4. **Can I verify the answer myself?**
5. **Can I execute another 10 steps before needing Maor?**
6. **Can I reduce Maor's involvement from 10 minutes to 1 minute?**
7. **Can I reduce Maor's involvement from 1 minute to a single click?**
8. **Can I eliminate Maor's involvement entirely?**

Only after exhausting all eight questions should human intervention be requested.

### When Intervention Is Required — Mandatory Format

Present only the minimum action needed. Present it at the latest possible point.

**ACTION REQUIRED:**
- Step 1 — exact action at exact URL/screen
- Step 2 — exact action
- Step 3 — exact action

**EXPECTED RESULT:**
- What Maor should see on completion

**NEXT AUTOMATED STEP:**
- What Claude executes immediately after

### Navigation Standard

- Exact URL — never "go to the dashboard"
- Exact field, button, or form element identified
- Instructions start from the current screen state
- Zero context switching required

### Application Scope

HIM-001 applies by default to every workflow type without exception:

| Workflow | HIM-001 Applies |
|----------|----------------|
| Browser operations | ✅ Always |
| Client fulfillment (reports, audits, proposals) | ✅ Always |
| Infrastructure work (Render, env vars, MCP setup) | ✅ Always |
| Reporting (GA4, GSC, GBP, monthly reports) | ✅ Always |
| Content production (video, graphics, social) | ✅ Always |
| Website development (Wix, WordPress, monaempoweryou.com) | ✅ Always |
| AI Power Studio projects | ✅ Always |
| Connector deployment and integration | ✅ Always |
| Research and competitive analysis | ✅ Always |
| Mission Zero and infrastructure builds | ✅ Always |

### Measurement and Reporting

HIM-001 must be tracked and reported. Metrics are logged in `MONA Deliverables/Internal/Systems/HIM001_Metrics.md`.

**Tracked per session:**

| Metric | Definition |
|--------|-----------|
| Human interventions requested | Number of PMA items created or Maor actions requested |
| Human interventions avoided | Tasks initially requiring Maor that Claude solved autonomously |
| Tasks completed fully autonomously | Zero Maor input required start to finish |
| Average Maor actions per session | Total PMAs created ÷ sessions |
| PMA compressions | Multi-step PMAs reduced to a single reply or click |
| Estimated hours saved | (Avoided interventions × 5 min) + (Compressions × 4 min) ÷ 60 |

**Reporting cadence:** Updated at the end of every completed task block. Reviewed during every Lessons Learned Audit (Priority 10 template).

### Review Checkpoints

HIM-001 is evaluated during every Lessons Learned Audit with these specific questions:

1. Which PMA items from this period could have been avoided entirely?
2. Which PMA items were compressed well and which could be compressed further?
3. Were any escalations premature — did Claude ask before exhausting the 8-step checklist?
4. What new autonomous paths were discovered this period?
5. What is the trend — is Maor's required input per task decreasing over time?

### Relationship to BLOCKER-001

HIM-001 extends BLOCKER-001. BLOCKER-001 requires investigation before escalation. HIM-001 requires that after investigation, Claude completes the maximum possible autonomous work before the escalation point — not the minimum.

---

## STORAGE-001 — Deliverable Storage Standard

**Effective:** June 3, 2026

All MONA and MONA client deliverables must be saved to the `MONA Deliverables/` folder in the repository. This excludes AI Power Studio deliverables (separate structure).

### Folder Structure

| Folder | Contents |
|--------|---------|
| `MONA Deliverables/Clients/<Client Name>/` | Reports, audits, proposals, presentations, PDFs, marketing plans |
| `MONA Deliverables/Internal/Strategy/` | Growth strategies, connector research, market research |
| `MONA Deliverables/Internal/Audits/` | Capability audits, website audits, internal reviews |
| `MONA Deliverables/Internal/Systems/` | Operating profiles, agency rules, playbooks |
| `MONA Deliverables/Internal/Brand/` | Logo files, brand assets, presentations |
| `MONA Deliverables/Archive/` | Delivered documents retained for reference only |

### Deliverable Types That Must Use This Folder
Reports, Audits, Proposals, Presentations, PDFs, Logo packages, Growth plans, Strategy documents, Website roadmaps, Marketing plans.

### Desktop Sync Note
Remote Claude Code sessions cannot write to Maor's local Desktop. To sync deliverables locally:
```bash
git pull origin claude/monet-ai-power-studio-scope-3wmwA
```
All files in `MONA Deliverables/` will appear at the local repo path. To place the folder on the Desktop directly:
```bash
git clone https://github.com/monaempoweryou-del/mona-chat-ap ~/Desktop/MONA\ Workspace
```

### Index
All deliverables must be logged in `MONA Deliverables/REPORT_INDEX.md` per REPORT-001.

---

## REPORT-001 — Report Archive Standard

**Effective:** June 3, 2026

Whenever reports are located, generated, reconstructed, or migrated, each report must be documented with the following fields:

| Field | Description |
|-------|-------------|
| **Original Source** | Where the report was created (session, tool, local machine, etc.) |
| **Archive Location** | Current storage path in the repo |
| **Delivery Status** | Delivered to client / Internal only / Draft / Pending |
| **Reconstruction Status** | Original / Reconstructed (with reason) |
| **Client Delivery Status** | Delivered (with date) / Not yet delivered / N/A |
| **Source of Truth** | Which version is authoritative if multiple exist |

### Report Categories

Every report must belong to exactly one category:

| Category | Definition |
|----------|------------|
| **1. Archive Asset** | Originally delivered to client; this copy is for internal reference only |
| **2. Internal Draft** | Created for internal use; never intended for client delivery |
| **3. Client Deliverable** | Created for a client; delivery status may be pending or complete |
| **4. Reconstructed Asset** | Rebuilt from available data when original was inaccessible; original may exist elsewhere |

### Goal

Six months from now, anyone looking at this index should immediately know:
- Where the report came from
- Whether it was delivered to the client
- Whether it is original or reconstructed
- Which version is the source of truth

---

## CLIENT-001 — Original Source Preference

**Effective:** June 3, 2026

For client-facing deliverables, original source documents are always preferred over reconstructed versions.

If an original file exists but is inaccessible due to a tool limitation:

1. Document the limitation
2. Attempt alternate retrieval methods
3. Determine whether reconstruction is acceptable
4. Clearly label reconstructed documents internally

**Reconstruction is acceptable when:**
- Original cannot be obtained
- Business value outweighs retrieval effort
- Content can be recreated with high confidence

If the original can likely be obtained later, preserve that as the preferred source of truth and flag for replacement.

---

## BLOCKER-001 — Escalation Standard

**Effective:** June 3, 2026

When a file or resource is found but inaccessible, determine WHY before escalating.

Investigate in this order:
1. Can I see it?
2. Can I read it?
3. Can I identify it?
4. Can I download it?
5. Can I save it?

Document:
- Root cause of inaccessibility
- Attempted solutions
- Whether reconstruction or an alternate path exists

**Pending Maor Action is the last resort, not the first available option.**

---

## DELIVERY-001 — MONA Delivery Standard

**Effective:** June 3, 2026

Client-facing deliverables are not complete until:
- QC approved
- Attachments verified
- Email created
- Gmail Draft exists (or confirmed sent)

Internal archive assets are exempt from the email/draft requirement but must still pass QC and be filed under the correct REPORT-001 category.

---

## BROWSER-001 — Browser Profile Standard

**Effective:** June 4, 2026
**Refined:** June 4, 2026

### MONA "007" Profile — Permanently Excluded

MONA "007" is an empty Chrome profile created accidentally during setup. It contains no agency accounts, no client accounts, no operational access, and no business value.

**Exclusion rules:**

1. Do NOT connect to MONA "007" under any circumstances.
2. Do NOT use MONA "007" as a fallback, default, or backup profile.
3. Do NOT attempt to repair, recover, reconnect, preserve, or prioritize MONA "007".
4. Remove MONA "007" from all browser-selection logic, default assumptions, and profile preference systems.
5. Ignore any saved browser pairing that references MONA "007".

---

### Operational Profile Definition

A profile is usable **only if it passes BOTH tests:**

**Test 1 — Business Access**
- The profile contains the correct agency or client account
- It is logged into the needed services
- It has real operational value for the task at hand

**Test 2 — Full Claude Control**
- Claude can access and control the browser through the MCP connector / browser extension
- Claude can navigate pages, inspect the active account, take actions, and execute tasks
- Claude does not need Maor to manually click every step (except where a genuine security checkpoint or sensitive approval is required)

**Operational profile = Business Access ✅ + Full Claude Control ✅**

A profile with the right account but no Claude control = not operational yet.
A profile with Claude control but no useful account access = not operational.
Both conditions must be true before proceeding.

---

### Mandatory Validation Output

Before any browser-based task begins, output this check visibly in chat:

```
BROWSER-001 CHECK

Business Value:   PASS / FAIL
Claude Control:   PASS / FAIL
Profile:          [profile name]
Execution Status: PROCEED / STOP
Required Action:  [exact corrective action, only if STOP]
```

If status is PROCEED — execute immediately after the check. No further narration needed.
If status is STOP — state only the missing component and the exact action required to resolve it. No broad troubleshooting. No speculative fixes.

### Enforcement Principle

BROWSER-001 is a behavior, not a documented rule. The check runs every time. The format is the proof it ran.

Every browser task must follow this sequence in order:

1. **Verify business value** — Does this profile contain the agency account or client account needed for this task?
2. **Verify Claude control** — Does Claude have active MCP/browser control? Can Claude navigate, take actions, and execute the workflow without constant manual assistance?
3. **Connect** — Only after both verifications pass.
4. **Execute** — Proceed with the task autonomously.

**If either verification fails:**
- Do not proceed as if the browser is ready.
- Report the specific deficiency (which test failed and why).
- Request only the corrective action needed to resolve it.

The objective is autonomous execution, not merely browser connectivity. A connected browser that requires Maor to click every step is not an operational browser — it is a partially working one.

### Pre-Work Checklist (Applied Within Step 1 and Step 2)

- Which Chrome profile is active — named, confirmed, not "007"
- Which email/account is logged in — correct for the task
- Whether Claude browser connector/MCP has full control — connected and responsive
- Whether Claude can perform the required workflow end-to-end without repeated manual intervention

---

### Permitted Escalations (Genuine Human-Only Steps)

Escalate to Maor only when manual input is genuinely required:
- 2FA / security verification
- Payment approval
- Password entry
- Legal / financial final approval
- User-only business decision

All other browser actions are Claude's responsibility. The goal is execution without involving Maor unnecessarily.

---

## Learning Engine

Lessons recorded during active execution:

| Date | Lesson |
|------|--------|
| 2026-06-03 | When a file is found but inaccessible, determine WHY before escalating. Document root cause, attempted solutions, and remaining blocker. Only escalate after exhausting alternate paths. |
| 2026-06-03 | Gmail MCP (d1d24a0c) does not expose `messages.attachments.get`. PDF attachments can be seen and identified via `get_thread` but cannot be downloaded. Workaround: reconstruct from available email data if confidence is high. |
| 2026-06-03 | Remote cloud environment has no access to local machine filesystem (`file:///Users/...`). Desktop files require manual upload or local export to become accessible. |
| 2026-06-03 | Canva has an official MCP (Anthropic partnership). Free tier covers design generation, search, and export — no additional cost beyond existing Canva account. |
| 2026-06-03 | Google's official GA4 MCP server (Apache 2.0, v0.4.0) is the correct path for analytics data. Free, open source — not a third-party connector. |
| 2026-06-03 | GBP API approval requires: Google Cloud project + 60+ day verified business profile. Apply early — approval can take weeks. |
| 2026-06-03 | n8n self-hosted = zero cost, unlimited automations, 400+ integrations, native AI nodes. Correct Zapier/Make alternative for agencies with client data security requirements. |
| 2026-06-03 | Ahrefs + Semrush MCPs exist but require paid subscriptions ($99–$119+/mo). Google Search Console MCP covers 80% of the same SEO data at zero cost. |
| 2026-06-03 | HIM-001 core operating principle: "Maor is busy. How do I keep moving without him?" Default assumption = Maor is unavailable. Solve it. Only escalate after exhausting all 8 self-resolution steps. |
| 2026-06-03 | Gmail MCP create_draft does not support programmatic file attachments. Workaround: include attachment checklist in draft body; Maor attaches manually before sending. |
| 2026-06-03 | Maor also goes by "Moe" (nickname). Same person. |
| 2026-06-04 | WebFetch returns 403 on monaempoweryou.com (Wix-hosted). Use Wix MCP `CallWixSiteAPI` for all site data access. |
| 2026-06-04 | Wix Blog API: updating published post titles requires a draft cycle (create draft → update → publish). Category assignment to existing posts also requires this cycle. |
| 2026-06-04 | Wix Site Properties `update-business-profile`: field mask uses root field names only (e.g., `"description"` not `"businessProfile.description"`). |
| 2026-06-04 | Wix `list-published-site-urls` returns only the primary domain URL, not individual page paths. Use `blog/v3/posts` for blog content inventory. |
| 2026-06-04 | monaempoweryou.com: phone number (916) 473-3131 is a Sacramento area code on an LA business — kills local SEO. Fix is Wix Dashboard → Settings → Business Info. Address also missing. |
| 2026-06-04 | AI Power Studio highest-scored opportunities (June 2026): HeyGen Avatar Video Production (25) > AI Readiness Audit (24) > Video Translation (24). All three are executable with current tool stack. |
| 2026-06-04 | Wix Blog category creation is fully autonomous (POST /blog/v3/categories). But assigning categories to existing published posts requires a draft cycle — not a single API call. |
| 2026-06-04 | MONA "007" Chrome profile = empty accidental profile. No operational access. No business value. Never connect to it. Always verify a browser profile contains real operational accounts before connecting. |
| 2026-06-04 | BROWSER-001 refined: operational profile requires BOTH business access AND full Claude control via MCP/extension. A profile with the right account but no Claude control is not operational. Verify all 4 checklist items before any browser task: active profile, logged-in account, MCP connector status, end-to-end workflow control. |
| 2026-06-04 | BROWSER-001 root cause: the failure was not merely selecting the wrong profile — it was failing to verify whether the selected profile was both useful AND controllable. Future browser selection is a 4-step sequence: (1) verify business value, (2) verify Claude control, (3) connect, (4) execute. If either (1) or (2) fails: stop, report the deficiency, request corrective action. The objective is autonomous execution, not mere browser connectivity. |
| 2026-06-04 | MASTER-001: a rule without a trigger is incomplete. Every rule must define Trigger + Timing + Scope + Action + Failure Handling before it is operational. Documented rules without these 5 components are notes, not rules. |
| 2026-06-04 | DELIVERABLES-001A: storage location alone is not organizational memory. Every REPORT_INDEX entry must include 8 metadata fields: Timestamp, Business Owner, Client/Project, Deliverable Type, Producing Agent, Workflow, File, Status. Unknown fields → [REVIEW_X] prefix, never silently omitted or guessed. |
