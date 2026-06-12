# Mona Digital Marketing — Operating Rules

## READ THIS FIRST ON EVERY SESSION START

Before doing anything else, read `asset-registry.json`. It is the source of truth for all client work.

Answer these questions from the registry before touching anything:
- What was the last approved asset for each active client?
- What is pending approval?
- What is in production?
- What was rejected and why?

Do not ask the human where assets are. The registry is the answer. If the registry does not have the answer, that is a system failure to fix — not a question to ask the human.

---

## THE FUNDAMENTAL RULE

**No deliverable is complete until it is saved, cataloged, and recoverable.**

Generated ≠ Complete.  
Sent ≠ Complete.  
Approved verbally ≠ Complete.  

Complete = Logged in asset-registry.json + committed to git + recoverable by any future session without human input.

This rule applies to every asset type:
- Images
- Proposals
- Invoices
- Emails
- Websites
- Presentations
- Templates
- Brand assets
- Strategy documents
- Research documents
- Client deliverables of any kind

---

## ASSET LIFECYCLE — MANDATORY STEPS

Every asset must pass through these stages. No skipping.

```
GENERATE → LOG (pending_approval) → SUBMIT → DECISION → CATALOG → DELIVER → ARCHIVE
```

### 1. GENERATE
Asset is created using any tool (Higgsfield, Claude, Gmail, manual, etc.)

### 2. LOG IMMEDIATELY
Before submitting for approval, add entry to asset-registry.json with:
- status: "pending_approval"
- All known fields populated
- Commit to git

### 3. SUBMIT
Present to approver (Maor or Nataly or client) with the registry ID referenced.

### 4. DECISION
- Approved → update status to "approved", add approval_date and approved_by, commit
- Rejected → update status to "rejected", add rejection reason in notes, commit
- Revision requested → create new version entry, keep old entry with status "superseded"

### 5. CATALOG
Approved assets are committed to git immediately. The generation_id, file_path, and image_url must be permanent and resolvable.

### 6. DELIVER
When delivered to client, update status to "delivered", add delivered_to and delivery_date. Commit.

### 7. ARCHIVE
Completed projects move to archived status. Never deleted — always recoverable.

---

## CLIENTS & ACTIVE PROJECTS

### Renova Builders
- Contact: Omri Dror (renovabuilders@gmail.com)
- Google Ads Customer ID: 630-398-6974
- Active: Houzz Gallery (20 images — ~5 approved in prior sessions, 15 remaining)
- Active: PPC Campaign Management (access confirmed via monaempoweryou@gmail.com)
- Houzz Gallery Brand Standard: square 1:1, Renova logo bottom-left, horizontal rectangular dark banner, luxury photorealistic style

### Finish Line Taxi
- Location: Temecula, CA
- Active projects: see registry

### Mona Digital Marketing (Internal)
- Brand identity assets tracked in registry

---

## BRAND CONSISTENCY RULE

Once a template is approved, it becomes a locked standard.

- Do NOT modify an approved template
- Do NOT regenerate from scratch when an approved template exists
- Do NOT change logo placement, sizing, or style without explicit approval
- Always check the registry for the approved template before generating anything

The system maintains brand identity. The human approves. That is the only division of responsibility.

---

## RENOVA GALLERY — CURRENT OPERATING RULE

- Target: 20 images total
- Approved template: LOCKED (horizontal rectangular dark banner, logo bottom-left)
- Strategy: Resurface existing approved images first. Generate new only when no existing asset qualifies.
- Approval gate: One image at a time. Approval before proceeding to next.
- Every generated image logged immediately in registry under client: renova_builders, project: houzz_gallery

---

## HOW TO ADD A REGISTRY ENTRY

When any deliverable is created, add to asset-registry.json under the correct client/project:

```json
{
  "id": "client-project-NNN",
  "asset_type": "image|proposal|invoice|email|website|template|brand_asset|strategy|document",
  "name": "descriptive name",
  "file_name": "filename.ext",
  "file_path": "storage location or URL",
  "version": "v1",
  "status": "pending_approval",
  "source_tool": "Higgsfield|Claude|Gmail|Manual",
  "template_used": "registry ID of template, or null",
  "intended_use": "what this is for",
  "submitted_date": "YYYY-MM-DD",
  "approval_date": null,
  "approved_by": null,
  "delivered_to": null,
  "delivery_date": null,
  "generation_id": "tool-specific ID if applicable",
  "file_url": "direct URL if applicable",
  "notes": "context, feedback, version history",
  "next_action": "what happens next"
}
```

Then: `git add asset-registry.json && git commit -m "Registry: [client] [asset-type] [status]"`

---

## RENOVA BUILDERS — PPC EXECUTION AUTHORITY
### Formal Execution Order — June 12, 2026

**Budget Cap:** $5,000/month total. Do not exceed without explicit approval.

**Success Metric:** Qualified leads generated for Renova Builders. Every recommendation, optimization, and report must support this objective.

**Reporting Chain:** Internal Moe report → Nataly approval → Client delivery (Omri Dror)

#### FULL AUTHORITY (execute immediately, no approval needed):
- Conversion tracking: demote page view events to Secondary, verify form/quote/call tag triggers
- Negative keywords: add/update negative keyword lists at campaign and account level
- Geo targeting: add/remove locations within Bay Area CA scope
- Ad schedule: adjust day/hour bid modifiers
- Ad extensions / assets: add, update, or remove sitelinks, callouts, call assets
- Tracking and attribution improvements
- Recurring monitoring and diagnostic systems
- Account hygiene: pause zero-impression ad groups, remove duplicate/irrelevant keywords
- Search term quality management: weekly review and negative addition
- Landing page audit and recommendations (recommendations only — no site edits)

#### REQUIRES APPROVAL BEFORE EXECUTING:
- New campaigns (any type)
- Deleting campaigns (even dead ones)
- Pausing active campaigns that have ANY recent spend
- Increasing total monthly budget above $5,000
- Major structural rebuilds (ad group restructure, keyword strategy overhaul)
- Bid strategy changes on active KEEP campaigns

#### ACTIVE KEEP CAMPAIGNS (as of June 12, 2026):
- "Leads Service base--13"
- "full home remodel"
All other campaigns are dead/zero-impression and subject to pause only with approval.

#### EXECUTION PHASES:
1. **Measurement Integrity** — Fix conversion tracking, verify phone/form/call signals, remove page view pollution
2. **Traffic Quality** — Negative keywords, irrelevant traffic removal, geo targeting, weekly search term review
3. **Lead Capture** — Landing page audit, mobile click-to-call, form functionality review
4. **Growth Optimization** — Device/geo/schedule performance analysis, budget reallocation within cap

#### STANDING ORDERS:
- Do NOT open new diagnostic tracks or research cycles after authorized A-items are complete
- Do NOT optimize only to save money — optimize to create predictable lead growth
- Do NOT produce another audit before executing what is already authorized
- Do NOT surface B-items as blockers — execute A-items, then return with B-item recommendations

---

## ESCALATION RULES

Surface to Maor immediately if:
- An approved asset cannot be located by its registry entry
- A generation tool fails after 2 attempts
- A client has not responded to a submitted deliverable in 48+ hours
- A Google Ads campaign shows anomalous spend or performance
- Account spend approaches $4,500/month (early warning before $5,000 cap)

Do NOT surface to Maor:
- Questions about where assets are stored (check the registry)
- Questions about what template to use (check the registry)
- Questions about what was previously approved (check the registry)
- Routine status updates (update the registry and continue)
- PPC A-items within full execution authority (execute, then report)
