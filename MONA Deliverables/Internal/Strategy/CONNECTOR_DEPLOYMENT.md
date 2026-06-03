# MONA Connector Deployment Guide
**Date:** June 3, 2026
**Status:** Active deployment tracker

---

## Desktop Access Limitation — Context

This session runs in a **remote cloud environment**. Claude Code cannot:
- Access `~/Desktop/` or any local Mac filesystem path
- Run `claude mcp add` on Maor's local installation
- Submit OAuth flows on Maor's behalf
- Create Google Cloud projects or API applications

**What Claude CAN do remotely:** Create files, call already-connected MCPs, write config files to the repo, provide exact commands for Maor to run locally.

**How to get MONA Deliverables on your Mac Desktop:**
```bash
# If repo is not yet cloned locally:
git clone https://github.com/monaempoweryou-del/mona-chat-ap ~/Desktop/MONA\ Deliverables

# If repo is already cloned somewhere:
git pull origin claude/monet-ai-power-studio-scope-3wmwA
# Then the MONA Deliverables/ folder will be in your local repo directory.
```

For local Claude Code sessions (Mac desktop app), Claude will have filesystem access and can save directly to any path.

---

## READY TO DEPLOY NOW
*Maor runs these commands once. Takes < 30 minutes total.*

---

### 1. Canva MCP (Official)
**Time:** 5 minutes · **Cost:** Free

```bash
# On your Mac, in terminal:
claude mcp add canva

# Claude Code will prompt for authentication.
# Sign in with your Canva account (same one you use at canva.com).
# Done. Claude can now generate, edit, and export Canva designs.
```

**What unlocks:** Prompt → branded graphic, design resizing, template access, export to PNG/PDF.

**Status:** ⬜ Not yet deployed

---

### 2. Google Analytics 4 MCP (Official, Open Source)
**Time:** 10 minutes · **Cost:** Free

```bash
# Step 1: Install the official GA4 MCP server
npm install -g @google/google-analytics-mcp

# Step 2: Add to Claude Code
claude mcp add google-analytics -- npx @google/google-analytics-mcp

# Step 3: Authenticate when prompted (Google OAuth — your Google account)

# Step 4: Provide your GA4 Property ID
# Find it: analytics.google.com → Admin → Property Settings → Property ID
# Format: 123456789
```

**What unlocks:** Pull live GA4 traffic, sessions, conversions, user behavior directly into Claude sessions. Automates client report data.

**Status:** ⬜ Not yet deployed

---

### 3. Google Search Console MCP (Community)
**Time:** 10 minutes · **Cost:** Free

```bash
# Install community GSC MCP
npm install -g @modelcontextprotocol/server-google-search-console

# Add to Claude Code
claude mcp add google-search-console -- npx @modelcontextprotocol/server-google-search-console

# Authenticate with Google OAuth when prompted
# Provide site property URL: https://monaempoweryou.com or sc-domain:monaempoweryou.com
```

**What unlocks:** Real keyword rankings, click-through rates, index coverage, impressions — directly from Google. No Ahrefs needed.

**Status:** ⬜ Not yet deployed

---

### 4. Slack MCP (Official Anthropic Reference)
**Time:** 15 minutes · **Cost:** Free

**Step 1:** Create a Slack Bot
1. Go to api.slack.com/apps → Create New App → From scratch
2. Name: "MONA Bot" · Workspace: your MONA workspace
3. Add OAuth scopes: `channels:history`, `channels:read`, `chat:write`, `users:read`
4. Install to workspace → copy Bot Token (starts with `xoxb-`)

```bash
# Step 2: Add to Claude Code with token
claude mcp add slack -e SLACK_BOT_TOKEN=xoxb-your-token-here -- npx @modelcontextprotocol/server-slack
```

**What unlocks:** Post PMA alerts to Slack, log client milestones, receive notifications from Claude directly in Slack.

**Status:** ⬜ Not yet deployed (requires Slack workspace)
**Blocker:** Does MONA have a Slack workspace? If not, skip for now.

---

## REQUIRES MAOR
*These cannot be deployed without credentials, approvals, or account access.*

---

### 5. Google Business Profile MCP
**Blocker:** Google API approval process (takes days to weeks)

**What Maor must do:**
1. Go to console.cloud.google.com → Create new project "MONA GBP"
2. Enable "My Business Business Information API" and related GBP APIs
3. Create OAuth credentials (Web application)
4. Submit API access request form — requires verified GBP + active business website
5. Wait for Google approval (typically 5–15 business days)
6. Once approved, provide: Client ID + Client Secret to Claude

**Why this matters:** GBP is the #1 local ranking factor. Review management + weekly posts for all clients. Start the application today — every week waiting is a week without automated GBP management.

**Status:** ⬜ Application not yet submitted · **Start this today**

---

### 6. Meta Business MCP (Facebook + Instagram)
**Blocker:** Facebook Developer account + Meta Business access

**What Maor must do:**
1. developers.facebook.com → Create App → Business type
2. Add "Marketing API" product
3. Generate a System User access token with ads_management permission
4. Provide token to Claude

**When to activate:** When first paid ad campaign is ready (Renova, Laguna, or MONA self-promo).

**Status:** ⬜ Not started · Low urgency (no paid campaigns currently)

---

### 7. n8n Self-Hosted Automation
**Blocker:** Hosting decision + initial setup time (~3–4 hours)

**Options:**
| Option | Cost | Effort | Recommended? |
|--------|------|--------|-------------|
| Mac Mini Pro (local) | Free (hardware owned) | High (port forwarding, uptime mgmt) | ❌ Not ideal for always-on |
| Render.com free tier | Free | Medium (15 min deploy) | ✅ Best for start |
| Railway.app free tier | $5 credit/mo then $0.01/hr | Low | ✅ Good alternative |
| n8n Cloud | €24/mo | Very low | ❌ Defeats free-tier goal |

**Deploy on Render (recommended):**
```bash
# On your Mac:
# 1. Fork n8n's official render deploy template at render.com/deploy
# 2. Connect to GitHub account
# 3. Set env vars: N8N_BASIC_AUTH_USER, N8N_BASIC_AUTH_PASSWORD
# 4. Deploy — takes ~10 minutes
# 5. Share the Render URL with Claude for workflow configuration
```

**What unlocks:** Full automation backbone. Monthly report auto-generation. GBP posting scheduler. Lead notification pipeline.

**Status:** ⬜ Not started · **High priority — activate after GBP API approved**

---

### 8. HeyGen Voice Clone
**Blocker:** Maor must provide audio sample

**What Maor must do:**
- Record 30 seconds of clean speech (minimal background noise)
- Upload as a WAV or MP3 file to this chat session
- Claude will use `clone_voice` MCP tool to create the voice model

**What unlocks:** Maor's voice on unlimited AI-generated videos for MONA + AI Power Studio.

**Status:** ⬜ Waiting for PMA-007 (audio sample from Maor)

---

### 9. Zernio Social MCP (Multi-Platform Posting)
**Blocker:** Zernio account + platform OAuth tokens

**When to activate:** When ready to schedule client social media posts at scale.
**Free tier:** First 2 social accounts included.

**Status:** ⬜ Not started · Activate when Content Machine (Priority 7) is deployed

---

## Deployment Status Dashboard

| Connector | Category | Status | Blocker | Priority |
|-----------|----------|--------|---------|----------|
| Canva MCP | Design | ⬜ Ready | None — run command | **High** |
| GA4 MCP | Analytics | ⬜ Ready | None — run command | **High** |
| GSC MCP | SEO | ⬜ Ready | None — run command | **High** |
| Slack MCP | Ops | ⬜ Ready | Need Slack workspace | Medium |
| GBP API | Local SEO | ⬜ Waiting | Google API approval | **Critical — apply now** |
| Meta Business | Ads | ⬜ Waiting | FB Developer account | Low (no paid campaigns yet) |
| n8n Automation | Backbone | ⬜ Waiting | Hosting decision | High (after GBP) |
| HeyGen Voice | Content | ⬜ Waiting | Audio sample from Maor | High — PMA-007 |
| Zernio Social | Content | ⬜ Waiting | Account setup | Low (after Content Machine) |

---

## Already Connected (Active MCPs)

| MCP | What It Does | Status |
|-----|-------------|--------|
| Higgsfield (`01635c4d`) | Image + video generation, virality prediction | ✅ Active |
| HeyGen (`dc164e32`) | Avatar video, lipsync, voice cloning, digital twin | ✅ Active |
| Gmail (`d1d24a0c`) | Draft creation, thread search, label management | ✅ Active |
| Wix (`658191d9`) | Full site management, API access | ✅ Active |
| WordPress.com (`f9abb861`) | Content authoring, domain management | ✅ Active |
| GitHub (`mcp__github__`) | Full repo + PR + issue management | ✅ Active |
| Job Search (`03734e56`) | US/Canada job listings | ✅ Active |
| WebSearch | Real-time web search | ✅ Active |
| WebFetch | Public URL content fetching | ✅ Active |

---

*Last updated: June 3, 2026*
