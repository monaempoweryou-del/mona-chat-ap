# MONA Connector Research — Priority 4
**New MCPs, Automations & Tools Not Yet in Stack**
**Date:** June 3, 2026
**Branch:** `claude/monet-ai-power-studio-scope-3wmwA`

---

## Executive Summary

7 high-value connectors identified that are either free or have a free tier adequate for MONA's current stage. Adding these would close the most critical gaps in MONA's operational stack: analytics reporting, local SEO management, social media scheduling, design production, and workflow automation.

**Current gap:** MONA can generate content and deliver reports, but cannot yet: pull live GA4/GBP data, schedule posts programmatically, create branded Canva assets on demand, or automate multi-step workflows between tools.

---

## Tier 1 — FREE, High ROI, Activate Now

### 1. Canva MCP (Official)
**Cost:** Free on all Canva plans · Pro unlocks resizing · Enterprise unlocks brand kits
**Source:** Canva's official MCP server — launched with Anthropic partnership

**What it does:**
- Generate Canva designs from text descriptions (prompt → branded graphic)
- Edit existing designs with natural language
- Resize designs to any platform format (free tier: limited; Pro: unlimited)
- Search your Canva media library
- Export finalized designs as PNG/PDF
- On Enterprise: brand kit autofill, branded templates

**MONA Use Cases:**
- Social media graphics for Renova Builders, Laguna, Finish Line Taxi — on demand from Claude
- Monthly report cover pages, infographic inserts
- MONA agency pitch decks generated from briefs
- AI Power Studio thumbnails and promotional graphics
- Logo lockup variations in Canva (once vector file approved post-PMA-006)

**How to connect:** `claude mcp add canva` → authenticate with Canva account → done

**Estimated ROI:** Replaces ~4 hours/week of manual Canva work; enables client asset delivery without leaving the session

---

### 2. Google Analytics 4 MCP (Official, Open Source)
**Cost:** Free (Google open source, Apache 2.0 — no API cost for standard GA4)
**Source:** Official Google Analytics team — github.com/googleanalytics/google-analytics-mcp (v0.4.0, May 2026)

**What it does:**
- Pull live GA4 data: traffic, sessions, conversions, user behavior
- Run custom reports with date ranges, dimensions, segments
- Run funnel reports (conversion path analysis)
- Access real-time data
- Query custom dimensions and metrics

**MONA Use Cases:**
- Automate client monthly performance reports (pull GA4 → generate PDF → Gmail draft)
- Before/after analysis for every client campaign
- Renova Builders monthly reports: replace manual data pulling with one command
- Priority 5 (90-Day Growth Strategy): use real MONA GA4 data for self-assessment
- Priority 9 (MONA Website Roadmap): pull monaempoweryou.com traffic data for evidence-based recommendations

**How to connect:** Install official MCP → authenticate with Google OAuth → provide GA4 Property ID

**Estimated ROI:** Saves 2–3 hours per client per month on manual reporting; makes reporting 100% data-accurate vs. manually typed

---

### 3. Google Business Profile MCP
**Cost:** Free (multiple options; n8n workflow is self-hosted free; LobeHub community server is free)
**Source:** Multiple implementations — n8n template (9 operations), LobeHub GBP Review Agent, Zapier MCP

**What it does:**
- Fetch GBP reviews and ratings
- Generate AI-written review responses
- Auto-post responses to reviews
- Manage GBP posts (updates, offers, events)
- Pull GBP performance metrics

**MONA Use Cases:**
- Renova Builders GBP review management — respond to reviews from Claude automatically
- Laguna Luxury Pools review response drafting
- Finish Line Taxi reputation management
- GBP posts as part of every client's monthly deliverable
- Priority 5 (90-Day Growth Plan): local SEO via consistent GBP posting schedule

**Important:** Requires GBP API approval (Google Cloud project + verified business + 60+ day old GBP). Process takes days to weeks — start now so it's ready for client campaigns.

**How to connect (recommended):** n8n self-hosted workflow template (all 9 GBP operations, MCP-compatible trigger)

**Estimated ROI:** Local SEO impact for every client; GBP is the #1 local ranking factor — this is a direct service deliverable

---

### 4. Google Search Console MCP (Community)
**Cost:** Free
**Source:** Community server — included in Claude SEO free bundle (claude-seo.md)

**What it does:**
- Pull search performance data: impressions, clicks, CTR, position by keyword
- Index coverage reports
- Keyword ranking trends over time
- Page-level performance breakdown

**MONA Use Cases:**
- SEO reporting section of monthly client reports — pull real GSC data automatically
- Track Renova Builders keyword rankings month-over-month
- Priority 9 (MONA Website Roadmap): diagnose which pages need SEO attention
- Priority 5 (Growth Strategy): identify quick-win keywords with high impression / low CTR

**How to connect:** Install community GSC MCP → Google OAuth → provide site property URL

**Estimated ROI:** Replaces Ahrefs/Semrush need for basic keyword tracking — real Google data, zero cost

---

### 5. Slack MCP (Official Anthropic Reference)
**Cost:** Free (Anthropic maintains official Slack MCP)
**Source:** Anthropic reference servers — model context protocol/servers repo

**What it does:**
- Post messages to channels
- Read channel history
- Look up team members
- Create and manage threads

**MONA Use Cases:**
- Priority 6 (USER-001): Maor operating profile — log decisions and approvals to Slack thread automatically
- Client milestone notifications ("Renova report delivered — waiting on Maor approval")
- PMA (Pending Maor Action) alerts piped to Slack instead of only in TASK_TRACKER.md
- AI Power Studio team coordination when team grows

**How to connect:** Configure Slack Bot with workspace token → `claude mcp add slack`

**Estimated ROI:** Operational — closes the loop between Claude Code actions and Maor's real-time awareness

---

## Tier 2 — FREE with MONA Use Case, Activate Within 30 Days

### 6. Meta Business MCP (Official — Facebook + Instagram Ads)
**Cost:** Free to connect (ad spend is separate)
**Source:** Meta's official MCP — launched April 29, 2026

**What it does:**
- Create ad campaigns from Claude
- Pull ad performance breakdowns (ROAS, CPC, CTR, reach)
- Manage audiences
- Run A/B analysis across ad sets
- Pause/resume/budget ad campaigns

**MONA Use Cases:**
- Future Renova Builders paid campaigns: build + manage from Claude session
- Laguna Luxury Pools Facebook remarketing
- MONA agency self-promotion ads
- Client reporting: pull Meta ad performance → include in monthly PDF automatically

**Note:** Currently no paid ad clients confirmed — connect now, activate when needed. Zero cost to connect.

**How to connect:** Meta Developer portal → create app → get access token → configure MCP

---

### 7. n8n Self-Hosted Automation
**Cost:** FREE (self-hosted, zero execution limits, zero software cost)
**Source:** Open source — n8n.io, 400+ built-in integrations

**What it does:**
- Visual workflow builder connecting 400+ apps
- Native AI nodes (plug Claude API directly into workflows)
- Triggers: webhooks, schedules, form submissions, email, API
- For agencies: automate onboarding, reporting, lead management, content pipeline
- Client data stays within your own infrastructure (not routed through Zapier servers)

**MONA Use Cases:**
- Monthly auto-report trigger: "On the 1st of every month → pull GA4 + GSC + GBP data → generate PDF → Gmail draft to client" — fully automated
- Lead intake: New Wix form submission → create draft proposal → notify Maor on Slack
- Content calendar: Schedule → trigger Claude content generation → Canva design → social post
- GBP posting schedule: automated posts across all clients on a weekly cadence

**Setup:** Requires hosting (Render free tier, Railway free tier, or locally on Mac Mini). Setup time: 2–4 hours initial.

**Estimated ROI:** Saves 3–5 hours per client per month (per n8n agency benchmarks). At 3 clients = 9–15 hrs/month returned.

---

## Tier 3 — LOW COST, High Strategic Value

### 8. Zernio Social MCP
**Cost:** First 2 accounts FREE · $6/account from account 3+
**Coverage:** 15 platforms: Instagram, TikTok, Twitter/X, LinkedIn, YouTube, Facebook, Threads, Pinterest, Reddit, Bluesky, Telegram, Google Business, WhatsApp, Snapchat, Discord

**What it does:**
- Schedule and publish posts across all platforms from Claude
- Read analytics per platform
- Manage content queue

**MONA Use Cases:**
- Client social media management from Claude session (no Hootsuite/Buffer login required)
- AI Power Studio multi-platform content distribution in one command
- Monthly content calendar → auto-schedule 30 posts across platforms in one session

**Cost decision:** Use Buffer free plan for MONA's own accounts now. Upgrade to Zernio when managing client accounts at scale.

---

### 9. HubSpot MCP (CRM)
**Cost:** Free CRM tier · Paid unlocks more API features
**Source:** Official HubSpot MCP

**What it does:**
- Manage contacts, companies, deals
- Pull pipeline status
- Create and update deals from Claude

**MONA Use Cases:**
- Track Laguna Luxury Pools, Renova Builders, Finish Line Taxi as contacts
- Log every client interaction and deliverable in CRM
- Priority 6 (USER-001): Maor Operating Profile — track how Maor approves / revises deliverables per client
- Pipeline visibility: "What's the status of each prospect?"

**Note:** Currently Gmail + TASK_TRACKER.md is the CRM. HubSpot is worth connecting once client count exceeds 5.

---

## What to Skip (For Now)

| Tool | Why Skip |
|------|---------|
| Ahrefs MCP | Requires paid Ahrefs plan ($99+/mo) — GSC + community tools cover current needs |
| Semrush MCP | Requires paid Semrush plan ($119+/mo) — same coverage from free tools at this stage |
| Hootsuite | No free plan; $199/mo — Zernio/Buffer fully replace at a fraction of the cost |
| Klaviyo MCP | Email/SMS automation — no email list yet; add when MONA has a subscriber base |
| Linear/Jira | Overkill for current team size — TASK_TRACKER.md is sufficient |

---

## Activation Roadmap

| Priority | Connector | Cost | Effort | When |
|----------|-----------|------|--------|------|
| **Now** | Canva MCP | Free | 5 min | This session |
| **Now** | Google Analytics 4 MCP | Free | 15 min | This session |
| **Now** | Google Search Console MCP | Free | 15 min | This session |
| **Now** | Slack MCP | Free | 20 min | This session (if Slack workspace exists) |
| **Week 1** | Google Business Profile MCP | Free | 1–2 days (API approval) | Submit API application today |
| **Week 2** | Meta Business MCP | Free | 1 hr | After GBP setup |
| **Week 2–3** | n8n self-hosted | Free | 3–4 hrs | When ready to automate reporting pipeline |
| **Month 2** | Zernio Social MCP | $0–$12/mo | 30 min | When managing client social accounts |
| **Month 3** | HubSpot MCP | Free | 1 hr | When client count > 5 |

---

## Biggest Single Unlock

**Google Analytics 4 + Google Search Console + Google Business Profile combined = automated, data-accurate client reporting with zero manual data entry.**

This trio directly upgrades every Renova Builders, Laguna, and Finish Line Taxi deliverable from a reconstructed estimate to a live data report. It's the foundation for Priority 5 (90-Day Growth Strategy) and Priority 9 (Website Roadmap).

Canva MCP + HeyGen video = full content production pipeline running entirely from Claude Code.

---

## Learning Engine Updates

| Date | Lesson |
|------|--------|
| 2026-06-03 | Canva has an official MCP (Anthropic partnership). Free tier covers design creation, search, export. No additional cost beyond existing Canva account. |
| 2026-06-03 | Google's official GA4 MCP server (v0.4.0, Apache 2.0) is the correct path for analytics data — not a third-party connector. |
| 2026-06-03 | GBP API approval requires: Google Cloud project + 60+ day verified GBP. Apply early — approval can take weeks. |
| 2026-06-03 | n8n self-hosted = zero cost for unlimited automations. Correct alternative to Zapier/Make for an agency with data security needs. |
| 2026-06-03 | Ahrefs + Semrush both have official MCPs but require paid subscriptions. Free alternative: GSC MCP + community tools cover 80% of the same use cases at zero cost. |

---

*Research completed: June 3, 2026 · Priority 4 of 11*
