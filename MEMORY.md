# Mona Digital Marketing — Institutional Memory

## Last Updated: 2026-06-12

This file is the persistent organizational memory for the MONA agency. Every session must read this before touching any client work. Update this file when new institutional knowledge is established.

---

## THE OPERATION

Mona Digital Marketing is a full-service digital marketing and creative production agency.

**Owner/Operator:** Mona (Moe) — internal review authority  
**Approval authority:** Nataly — must approve before client delivery  
**Agency email:** monaempoweryou@gmail.com

---

## DELIVERY CHAIN — UNIVERSAL

```
Moe review → Nataly approval → Client delivery
```

This chain applies to every client-facing asset. No exceptions. No assumptions about who approves what.

**Email addresses on file:**
- Moe (internal review): monaempoweryou@gmail.com [CONFIRM if separate Moe review address exists]
- Nataly (approval authority): UNKNOWN — flag as delivery blocker
- Do not send to client without both gates cleared

---

## HOW AGENTS MUST BEHAVE

A new session inherits full organizational context. The expected starting point is:

1. Read `CLAUDE.md`
2. Read `MEMORY.md` (this file)
3. Read `asset-registry.json`
4. Understand current priorities
5. Execute — do not ask for basic context that exists in these files

**Clarification mode is a failure mode.** A detailed client brief is sufficient to begin execution. Missing email addresses are delivery blockers, not production blockers. Flag them and continue building.

---

## ACTIVE CLIENTS

### Renova Builders
- **Contact:** Omri Dror | renovabuilders@gmail.com
- **Google Ads ID:** 630-398-6974
- **WordPress site:** renovabuilders.com (ID: 248781405) — live, active
- **PPC Authority:** Full execution authority on A-items (conversion tracking, negatives, geo, ad schedule, assets, hygiene, monitoring). B-items require Maor approval.
- **Budget cap:** $5,000/month
- **Active:** PPC Management (Phases 1+2 in progress) + Houzz Gallery (20 images, ~5 approved in prior sessions)
- **Execution order date:** June 12, 2026
- **Weekly monitor script:** renova-weekly-monitor.js — deploy Monday 8:00 AM in Google Ads Scripts
- **Pending (requires Omri UI action):** Demote "All Pages Views" to Secondary in Conversions settings

### Eti Mealev (אתי מעלב)
- **Type:** Luxury architecture + interior design firm, Haifa, Israel
- **Contact:** UNKNOWN — must be established
- **Deliverable:** Full WordPress website — architecture, design system, content, Hebrew copy, client presentation
- **Creative direction:** Sister website to EDNE Group (ednegroup.com). "Related, not replicated."
- **Language:** Hebrew primary (RTL), English secondary
- **WordPress site:** NOT YET CREATED
- **Registry entry:** CREATED June 12, 2026 (see asset-registry.json)
- **Status:** In production — presentation package being built

### Finish Line Taxi
- **Location:** Temecula, CA
- **Status:** No active projects in registry — clarify with Moe

### Best Garage Door & Gates OT INC
- **WordPress site:** bestgaragedoorandgateotinc.com (ID: 251256427) — live, active
- **Status:** Unknown — not in registry, no active brief

### Goldsmith (UNKNOWN PROJECT)
- **Status:** Referenced as "Goldsmith final QA" — top priority per standing orders
- **Problem:** ZERO context in session. No files in repo. No registry entry.
- **Action needed:** Moe to provide brief, deliverable file, or QA definition before this can be executed

---

## WORDPRESS ACCESS

WordPress.com MCP (mcp__f9abb861) is active with admin access.

| Site | Blog ID | Domain | Status |
|---|---|---|---|
| Renova Builders | 248781405 | renovabuilders.com | Live, active |
| Best Garage Door | 251256427 | bestgaragedoorandgateotinc.com | Live, active |
| Eti Mealev | NOT CREATED | TBD | Must create |

---

## WEBSITE QUALITY STANDARDS

Every website built by MONA must meet these standards before it goes to Moe for review:

### Visual
- Photography: editorial quality only — no stock, no lifestyle filler, no distortion
- Typography: intentional hierarchy, never default fonts, generous spacing
- Color: palette defined before build begins, consistent throughout
- Mobile: must be tested and flawless before review

### Architecture
- Max 5-6 main navigation items
- Every page has a clear purpose and a clear next action
- Portfolio/work sections: project as event, not thumbnail gallery
- Contact must be effortless — one click from any page

### Luxury Standard
- Does not look like a template
- Does not over-explain the value proposition
- Photography and typography do the selling
- Copy is precise, not verbose

### Hebrew/RTL Sites
- `dir="rtl"` implemented correctly
- Hebrew font size: 10% larger than equivalent English
- Hebrew text: 20-30% more space than English equivalent
- Language switcher: small, top corner, non-intrusive
- Both language versions feel native — not translated

---

## CREATIVE REFERENCES

### EDNE Group (Sister brand to Eti Mealev)
- **URL:** ednegroup.com
- **Tagline:** "Elevate Your Earthly Possessions"
- **Philosophy:** "We don't follow trends, we create them"
- **Positioning:** Non-conformist luxury interior design, edgy, rule-breaking
- **Visual:** Bold luxury, dark/rich palette, assertive typography, statement photography
- **Relationship to Eti Mealev:** Sister brand — same premium ecosystem, shared visual DNA, distinct identities. Someone opening both sites should recognize they belong to the same family.

---

## TOOLS AND INTEGRATIONS

| Tool | Purpose | Status |
|---|---|---|
| WordPress.com MCP | Site creation and content management | Active |
| Gmail MCP | Draft creation only (cannot send) | Active — drafts only |
| Higgsfield MCP | Image + video generation | Active |
| GitHub MCP | Repository management | Active |
| WebFetch | Web research | Active (some sites block: 403) |

**Gmail limitation:** Gmail MCP can CREATE drafts but CANNOT send. Final delivery requires manual send from Gmail UI.

---

## ASSET REGISTRY PROTOCOL

Before ANY deliverable is submitted for review:
1. Add entry to `asset-registry.json` with `status: "pending_approval"`
2. `git add asset-registry.json && git commit -m "Registry: [client] [type] [status]"`
3. Present to Moe with registry ID referenced

Registry IDs follow pattern: `[client-abbreviation]-[project]-NNN`
- Renova: `renova-houzz-NNN`, `renova-ppc-NNN`
- Eti Mealev: `eti-web-NNN`
- Goldsmith: `goldsmith-NNN`

---

## ESCALATION RULES

Surface to Moe immediately if:
- Account spend approaches $4,500/month (Renova $5,000 cap early warning)
- An approved asset cannot be located by registry entry
- A generation tool fails after 2 attempts
- Client has not responded to submitted deliverable in 48+ hours
- Anomalous spend or performance on any client account

Do NOT wait for Moe to:
- Find where assets are stored (check the registry)
- Confirm what template to use (check the registry)
- Ask what was previously approved (check the registry)
- Approve PPC A-items within full execution authority (Renova only)

---

## STANDING ORDERS

- Execute A-items immediately; surface B-items with recommendation
- Do NOT produce another audit before executing what is already authorized
- Do NOT optimize only to save money — optimize for lead growth and revenue
- Do NOT ask clarifying questions when a brief provides enough to begin
- Do NOT flag unknown email addresses as production blockers — stage delivery, flag address gap
- Update this file whenever new institutional knowledge is established
