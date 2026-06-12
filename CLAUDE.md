# Mona Agency OS — Permanent Operational Rules

## Two-Brand System

This system operates two completely separate businesses. Before generating ANY external communication, run this pre-flight check:

1. **Who is receiving this email?**
2. **Which company is sending this email?**
3. **Which brand should be represented?**
4. **Which template/tone applies?**

---

## Business #1 — MONA Digital Marketing

**Identity:** Internal agency. Los Angeles. Full-service digital marketing.  
**Email:** monaempoweryou@gmail.com  
**Colors:** Navy #1B2D4F, Blue #2E86C1  
**Voice:** Professional, efficient, agency-grade  
**Clients:** Renova Builders, Finish Line Taxi, Mona Digital Marketing (internal)

**MONA handles:**
- Agency proposals, invoices, monthly reports
- Client SEO audits, ad campaigns, social content
- Internal operations (all Nataly ↔ agency flows)

**MONA email standard:**
- Full proposal/invoice/report as HTML in email body
- Mona branding in header + footer
- Pricing, deliverables, timelines included upfront
- Produced by Mona Agency OS pipeline

---

## Business #2 — UNVEILED

**Identity:** Separate company. Builds websites as complete digital experiences.  
**Voice:** Premium, minimal, confident. Let the work speak.  
**Purpose:** Outreach to prospects who receive a demo website built for them.

### UNVEILED Communication Model

The website IS the proposal. The website IS the sales presentation.  
**Never attach PDFs, pricing sheets, proposals, or service menus to initial outreach.**

**UNVEILED email structure (permanent standard):**

```
1. UNVEILED branded header (own visual identity — NOT Mona navy)
2. Personalized 2–3 sentence intro: "We built something for [Business]..."
3. What was created + why it matters to them specifically
4. Single prominent CTA button → their demo website
5. Short value statement (1 line)
6. Secondary CTA: "Reply to this email" or "Schedule a call"
7. UNVEILED branded footer + signature
```

**Pricing rule — ABSOLUTE:**  
- NO pricing in initial UNVEILED email  
- NO pricing on the demo website  
- Pricing ONLY after prospect engages and requests it

**Primary CTAs for UNVEILED:**
- "See what we built for you"
- "Let's talk"
- "Request a walkthrough"
- "Schedule a call"
- "Reply to this email"

**Goal:** Start a conversation. Not negotiate price before value is demonstrated.

**The recipient should instantly know:**
- Who sent it (UNVEILED — clear sender identity)
- Why they received it (we built something for them)
- What was created (demo website)
- What to do next (one clear action)

---

## Pre-Flight Rule — Every External Email

```
IF recipient = client/prospect of MONA agency work:
    → Use MONA template, MONA branding, MONA colors
    → Include full deliverable in email body
    → Pricing and details upfront

IF recipient = UNVEILED prospect (website demo outreach):
    → Use UNVEILED template, UNVEILED branding
    → Link to demo website — that IS the proposal
    → NO pricing, NO attachments
    → CTA = start a conversation
```

**The customer should never wonder: Who sent this? What company is this from?**

---

## Platinum Pool & Property Services LLC

**Contact:** John Dithommaso Jr — johndithommasojr@gmail.com — (909) 970-1982  
**Website:** https://mona-chat-ap.onrender.com/platinum-pool  
**Agency relationship:** UNVEILED client (website demo built)  
**Status:** Website approved, deployed live  

**Email standard for Platinum Pool:** UNVEILED model — link to website, no pricing upfront, CTA = schedule a call

---

## Email Delivery Infrastructure — Permanent Standard

**Method:** GitHub Actions pipeline. Credentials in GitHub secrets. Never in code.

**Required GitHub secrets (one-time setup):**
- `GMAIL_USER` = monaempoweryou@gmail.com
- `GMAIL_APP_PASSWORD` = Gmail App Password (myaccount.google.com → Security → App Passwords)

**Queue file format** (`email_queue/pending/[id].json`):
```json
{
  "id": "descriptive-kebab-case-name",
  "brand": "unveiled | mona",
  "subject": "Email subject line",
  "stage": "test | send",
  "to_test": "monaempoweryou@gmail.com",
  "to_customer": "customer@email.com",
  "html": "<complete HTML email>"
}
```

**Two-stage delivery workflow:**
1. Create queue file with `"stage": "test"` → sends to monaempoweryou@gmail.com for approval
2. Review and approve in inbox
3. Change `"stage": "test"` → `"stage": "send"` and move back to pending/ → sends to customer
4. Same HTML, same content — no rebuilding

**Directory structure:**
- `email_queue/pending/` — emails waiting to send (workflow triggers on push here)
- `email_queue/sent/` — successfully sent (moved automatically, `sent_to` field added)
- `email_queue/failed/` — failed sends (moved automatically, `error` field added, retryable)

**To retry a failed email:** move from `failed/` back to `pending/` and push.

**Workflow:** `.github/workflows/send-email.yml` → triggers on push to `email_queue/pending/*.json`
**Script:** `.github/send_queued_emails.py` → reads queue, sends, moves files, writes GitHub summary

**End state:** "Boss, the email hit your inbox."

## Render Deployment

**Service:** mona-chat-api on Render.com (free tier — spins down after inactivity)  
**URL:** https://mona-chat-ap.onrender.com  
**Branch:** main (auto-deploys on push)  
**SMTP credentials:** Set in Render env vars (GMAIL_USER, GMAIL_APP_PASSWORD)  
**Send trigger:** POST /send-platinum-proposal with {"token":"platinum2024"}
