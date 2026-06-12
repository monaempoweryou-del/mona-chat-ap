# Mona Agency OS — Permanent Operational Rules

---

## COMPANY EMAIL ACCOUNT ARCHITECTURE

This is institutional knowledge. Every agent, every session, every workflow reads this first.

| Account | Type | Role |
|---------|------|------|
| `nataly@monadigitalmarketing.com` | Google Workspace | **Primary outbound sender** — all MONA client communications |
| `nataly@monadigitalmarketing.com` | Google Workspace | **UNVEILED outbound sender** — all UNVEILED prospect outreach |
| `monaempoweryou@gmail.com` | Gmail | **Approval inbox** — test emails land here before customer delivery |
| `maor@monadigitalmarketing.com` | Google Workspace | Design/visual production approvals |

**Rules that never change:**
- Customers always see `nataly@monadigitalmarketing.com` as the sender
- `monaempoweryou@gmail.com` is the approval/monitoring inbox — never the customer-facing sender
- No email goes to a customer until it has been reviewed at `monaempoweryou@gmail.com` first
- MONA and UNVEILED both send FROM `nataly@monadigitalmarketing.com` (until UNVEILED gets its own domain)

---

## EMAIL DELIVERY SOP — PERMANENT STANDARD

**Every future agent follows this exactly. No exceptions.**

### Step 1 — Build the email
Generate the HTML using the correct brand template (MONA or UNVEILED).

### Step 2 — Queue it as a test
Create `email_queue/pending/[id].json` with `"stage": "test"`.
This routes to the approval inbox (`monaempoweryou@gmail.com`), not the customer.

### Step 3 — Push to trigger delivery
`git add email_queue/pending/ && git commit && git push origin main`
GitHub Actions fires automatically. Email lands in inbox within 60 seconds.

### Step 4 — Approval
Review the email at `monaempoweryou@gmail.com` exactly as the customer would receive it.

### Step 5 — Promote to send
Change `"stage": "test"` to `"stage": "send"` in the queue file.
Move the file back to `pending/` if needed. Push. GitHub Actions sends to the customer.

### Step 6 — Confirmation
Queue file moves to `email_queue/sent/`. Report: "Boss, the email hit your inbox."

**No terminal commands. No drafts. No manual SMTP. No workarounds. Ever.**

---

## GITHUB ACTIONS EMAIL PIPELINE

**Method:** GitHub Actions — runs on GitHub's servers, outside the dev container.
Container network policy blocks smtp.gmail.com. GitHub Actions does not. This is the permanent fix.

**Workflow:** `.github/workflows/send-email.yml`
**Script:** `.github/send_queued_emails.py`
**Trigger:** Any push to `email_queue/pending/*.json`

**Required GitHub Secrets (one-time setup — Settings → Secrets → Actions):**

| Secret | Value |
|--------|-------|
| `SMTP_USER` | `nataly@monadigitalmarketing.com` |
| `SMTP_PASSWORD` | App Password for nataly@monadigitalmarketing.com |

**To generate the App Password:**
1. Sign in as nataly@monadigitalmarketing.com
2. Google Account → Security → 2-Step Verification → App passwords
3. Create one named "Mona Agency OS"
4. Copy the 16-character code — that is `SMTP_PASSWORD`

**Queue file format** (`email_queue/pending/[id].json`):
```json
{
  "id": "descriptive-kebab-case-name",
  "brand": "unveiled | mona",
  "subject": "Email subject line",
  "stage": "test | send",
  "to_test": "monaempoweryou@gmail.com",
  "to_customer": "customer@email.com",
  "html": "<complete HTML email body>"
}
```

**brand=mona** → FROM: nataly@monadigitalmarketing.com, MONA navy/blue template  
**brand=unveiled** → FROM: nataly@monadigitalmarketing.com, UNVEILED dark/gold template  
**stage=test** → sends to `to_test` (monaempoweryou@gmail.com) for approval  
**stage=send** → sends to `to_customer`  

**Queue directories:**
- `email_queue/pending/` — waiting to send (workflow trigger)
- `email_queue/sent/` — confirmed sent (file moved here automatically)
- `email_queue/failed/` — failed (file moved here with `error` field, retryable by moving back to pending/)

---

## TWO-BRAND SYSTEM

### Business #1 — MONA Digital Marketing

**Identity:** Internal agency. Los Angeles. Full-service digital marketing.
**Outbound sender:** nataly@monadigitalmarketing.com
**Colors:** Navy #1B2D4F, Blue #2E86C1
**Voice:** Professional, efficient, agency-grade
**Clients:** Renova Builders, Finish Line Taxi, Mona Digital Marketing (internal)

**MONA email standard:**
- Full deliverable (proposal/invoice/report) as HTML in email body
- MONA branding in header + footer
- Pricing, deliverables, timelines included upfront
- Subject format: `[Client Name] — [Deliverable Type]`

---

### Business #2 — UNVEILED

**Identity:** Separate company. Builds websites as complete digital experiences.
**Outbound sender:** nataly@monadigitalmarketing.com (until unveiled@ domain exists)
**Colors:** Dark #111111, Gold #C4A35A, White #F5F5F5
**Voice:** Premium, minimal, confident. Let the work speak.

**Core principle:** The website IS the proposal. The email is only the bridge.

**UNVEILED email standard (permanent):**
```
1. UNVEILED branded header (dark/gold — NOT Mona navy)
2. Personalized intro: "We built something for [Business]..."
3. What was built + why it matters to them specifically
4. Single CTA button → demo website URL
5. One-line value statement
6. Secondary CTA: "Reply to this email" or "Schedule a call"
7. UNVEILED branded footer
```

**Pricing rule — ABSOLUTE:**
- NO pricing in UNVEILED outreach email
- NO pricing on the demo website
- Pricing ONLY after prospect engages and requests it

**Primary CTAs:** "See What We Built For You" / "Let's talk" / "Request a walkthrough"

---

## PRE-FLIGHT RULE — EVERY EXTERNAL EMAIL

```
IF recipient = MONA agency client:
    FROM: nataly@monadigitalmarketing.com
    TEMPLATE: MONA (navy, full deliverable, pricing upfront)

IF recipient = UNVEILED prospect:
    FROM: nataly@monadigitalmarketing.com
    TEMPLATE: UNVEILED (dark/gold, website link only, no pricing)

ALWAYS: test email goes to monaempoweryou@gmail.com first
NEVER: send direct to customer without approval
```

---

## ACTIVE CLIENTS

### Renova Builders
- Type: MONA client
- Service area: Bay Area, CA — residential remodeling
- Services: SEO, Google Ads, social content, monthly reports
- Communication: MONA template, nataly@monadigitalmarketing.com

### Finish Line Taxi
- Type: MONA client
- Service area: Temecula, CA — taxi service
- Services: Google Ads, local SEO
- Communication: MONA template, nataly@monadigitalmarketing.com

### Platinum Pool & Property Services LLC
- Type: UNVEILED prospect
- Contact: John Dithommaso Jr — johndithommasojr@gmail.com — (909) 970-1982
- Demo website: https://mona-chat-ap.onrender.com/platinum-pool
- Status: Website approved, deployed live
- Communication: UNVEILED template, no pricing, CTA = schedule a call

### Goldsmith Financial
- Type: UNVEILED prospect
- Status: Outreach email pending — website URL required before sending
- Communication: UNVEILED template, no pricing

---

## RENDER DEPLOYMENT

**Service:** mona-chat-api on Render.com (free tier — spins down after inactivity)
**URL:** https://mona-chat-ap.onrender.com
**Branch:** main (auto-deploys on push)
**Note:** Render server has its own SMTP credentials (legacy). GitHub Actions is the permanent email method.
