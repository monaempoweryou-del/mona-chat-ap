# MONA Agency — Permanent Rules & Standards

> These rules govern how Claude Code operates as the AI backbone of Mona Digital Marketing.
> Rules are permanent until explicitly revised by Maor.

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
