# MONA Agency — Permanent Rules & Standards

> These rules govern how Claude Code operates as the AI backbone of Mona Digital Marketing.
> Rules are permanent until explicitly revised by Maor.

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
