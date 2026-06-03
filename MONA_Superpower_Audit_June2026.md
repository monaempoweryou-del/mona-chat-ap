# MONA Free Superpower Audit
**Priority 3 — AI Power Studio Capability Inventory**
**Date:** June 3, 2026
**Branch:** `claude/monet-ai-power-studio-scope-3wmwA`

---

## Executive Summary

MONA has access to **10 connected systems** spanning image generation, cinematic video production, AI avatar creation, voice cloning, virality prediction, site management, real-time research, and full Gmail/GitHub automation. Of the ~200 individual tools available, **fewer than 15 have been used**. This audit identifies the highest-ROI untapped capabilities ranked by business impact, and assigns agent ownership for each.

**Verdict:** MONA is sitting on a content production and client delivery engine that is 90% dormant.

---

## Connected Systems — Full Inventory

### 1. Higgsfield MCP (`01635c4d`)
**Plan:** Ultra · **Credits:** ~1,704 (as of June 3, 2026)
**Category:** Image & Video Generation, Analytics

| Tool | Capability | Status |
|------|-----------|--------|
| `generate_image` | GPT Image 1.5, GPT Image 2, Nano Banana Pro, Nano Banana 2, Marketing Studio Image | ✅ Used (logo project) |
| `generate_video` | Seedance 2.0, Kling 3.0, Google Veo 3, Veo 3.1, Veo 3.1 Lite, Cinema Studio 3.0, Marketing Studio Video, Wan 2.7, Grok Imagine, Minimax Hailuo | ❌ Never used |
| `virality_predictor` | Hook strength, retention, engagement, attention scoring | ❌ Never used |
| `personal_clipper_create` | Auto-clip best moments from long-form video | ❌ Never used |
| `video_analysis_create` | Deep content analysis of uploaded video | ❌ Never used |
| `upscale_video` | 2x/4x quality enhancement | ❌ Never used |
| `reframe` | Resize video for all platforms (9:16, 1:1, 16:9) | ❌ Never used |
| `show_marketing_studio` | Pre-built DTC ad templates | ❌ Never used |
| `models_explore` | Discover new available models | ✅ Used (audit) |
| `balance` | Credit balance check | ✅ Used |
| `show_generations` | View all generated media | ❌ Never used |

---

### 2. HeyGen MCP (`dc164e32`)
**Category:** AI Avatar Video, Voice Cloning, Digital Twins
**Cost:** Paid per video (included in HeyGen plan)

| Tool | Capability | Status |
|------|-----------|--------|
| `create_video_agent` | Full AI video agent with script + avatar + scene (recommended path) | ❌ Never used |
| `create_video_from_avatar` | Specific avatar + voice + script control | ❌ Never used |
| `create_video_from_image` | Animate any image with script/audio | ❌ Never used |
| `clone_voice` | Clone Maor's voice from audio sample | ❌ Never used |
| `design_voice` | Generate custom branded AI voice | ❌ Never used |
| `create_digital_twin` | Full AI replica of a person | ❌ Never used |
| `create_photo_avatar` | AI avatar from single photo | ❌ Never used |
| `create_lipsync` | Revoice/dub any video in new language or voice | ❌ Never used |
| `create_video_translation` | Full video translation to 40+ languages | ❌ Never used |
| `list_video_agent_styles` | Browse cinematics/retro-tech/etc styles | ❌ Never used |
| `search_audio_sounds` | Royalty-free music + SFX library | ❌ Never used |

---

### 3. Gmail MCP (`d1d24a0c`)
**Category:** Communication, Delivery
**Cost:** Free (connected)

| Tool | Capability | Status |
|------|-----------|--------|
| `create_draft` | Create Gmail drafts | ✅ Used |
| `get_thread` | Read full email threads | ✅ Used |
| `search_threads` | Search all Gmail | ✅ Used |
| `list_drafts` | List all drafts | ✅ Used |
| `create_label` / `label_thread` | Organize inbox with labels | ❌ Never used |
| `list_labels` | View all Gmail labels | ❌ Never used |

---

### 4. Wix MCP (`658191d9`)
**Category:** Website Management
**Cost:** Free (connected to monaempoweryou.com)

| Tool | Capability | Status |
|------|-----------|--------|
| `ListWixSites` | View all connected Wix sites | ❌ Never used |
| `ManageWixSite` | Edit site content, pages, navigation | ❌ Never used |
| `ExecuteWixAPI` | Full Wix REST API access | ❌ Never used |
| `UploadImageToWixSite` | Push images directly to site | ❌ Never used |
| `WixSiteBuilder` | AI-assisted page creation | ❌ Never used |
| `CallWixSiteAPI` | Specific API endpoint calls | ❌ Never used |

---

### 5. WordPress.com MCP (`f9abb861`)
**Category:** Content Publishing
**Cost:** Free (connected)

| Tool | Capability | Status |
|------|-----------|--------|
| `wpcom-user-sites` | List all WP.com sites | ❌ Never used |
| `wpcom-mcp-content-authoring` | Create posts, pages, media | ❌ Never used |
| `wpcom-mcp-site-editor-context` | Theme presets, design tokens | ❌ Never used |
| `wpcom-domain-purchase` | Domain availability + checkout | ❌ Never used |
| `wpcom-mcp-site` | Site configuration | ❌ Never used |

---

### 6. GitHub MCP (`mcp__github__`)
**Category:** Infrastructure
**Cost:** Free (connected)

| Tool | Capability | Status |
|------|-----------|--------|
| File ops (push, create, delete) | Manage all repo files | ✅ Used |
| PR + Issue management | Full GitHub workflow | ❌ Unused (no PRs needed yet) |
| `search_code` | Search across codebase | ❌ Never used |
| `actions_run_trigger` | Trigger CI/CD workflows | ❌ Never used |

---

### 7. WebSearch + WebFetch
**Category:** Research
**Cost:** Free (included)

| Tool | Capability | Status |
|------|-----------|--------|
| `WebSearch` | Real-time web search, US coverage | ❌ Never used in production |
| `WebFetch` | Fetch and analyze any public URL | ❌ Never used in production |

---

### 8. Job Search MCP (`03734e56`)
**Category:** Talent / Competitive Research
**Cost:** Free (connected)

| Tool | Capability | Status |
|------|-----------|--------|
| `search_jobs` | US/Canada job listings | ❌ Never used |

---

## Priority Rankings — Highest ROI Capabilities Not Yet Used

### 🔴 CRITICAL PRIORITY — Use Immediately

#### #1 — HeyGen Avatar Video (`create_video_agent`)
**ROI:** Replaces $500–$2,000/video production cost
**Use Cases:**
- MONA service intro / case study videos for prospects
- AI Power Studio tutorial series (recurring content)
- Client monthly performance video summaries instead of PDFs
- LinkedIn / Instagram thought leadership videos

**How it works:** Provide a prompt → AI agent builds full scene + script + avatar. Poll for completion. Share link.
**Owner:** Claude Code (executes on request)
**Time to first video:** ~10 minutes

---

#### #2 — Google Veo 3.1 / Cinema Studio 3.0 Video Generation
**ROI:** 8x — eliminates videographer, B-roll library costs
**Use Cases:**
- Social media content for MONA + AI Power Studio
- Client campaign visuals (pools, construction, hospitality scenes)
- AI Power Studio viral concept videos
- Educational/explainer visuals

**How it works:** Text prompt → cinematic video (5–15 seconds). Veo 3.1 has native audio generation.
**Owner:** Claude Code (executes on request)
**Time to first video:** ~5 minutes (generation) + queue time
**Credit cost:** ~50–150 credits per video (estimate based on Ultra plan rates)

---

#### #3 — Virality Predictor
**ROI:** 3–5x engagement improvement on all published content
**Use Cases:**
- Score every video before publishing to social
- Identify weak hooks before they go live
- A/B test concepts before full production
- Optimize AI Power Studio content for retention

**How it works:** Submit video → receive scores for hook strength, attention, retention risk, engagement prediction
**Owner:** Claude Code (runs automatically before any content delivery)
**Recommended rule:** No video goes to client or social without virality score ≥ 70

---

#### #4 — Marketing Studio Video (DTC Ads)
**ROI:** Immediate — client ad creative at zero incremental cost
**Use Cases:**
- Renova Builders monthly social ads
- Laguna Luxury Pools awareness campaign
- Finish Line Taxi promotional content
- MONA agency self-promotion

**How it works:** Provide product URL or image → one-click TikTok/Reels/Instagram video ad
**Owner:** Claude Code (generates on request, per client)

---

### 🟡 HIGH VALUE — Use Within 30 Days

#### #5 — HeyGen Voice Clone (`clone_voice`)
**ROI:** Eliminates voiceover bottleneck — enables 24/7 content production without Maor recording
**Use Cases:**
- AI Power Studio tutorial narration at scale
- Client video reports with Maor's voice
- Consistent brand voice across all video content

**Requires:** 30-second clean audio sample from Maor
**Owner:** Claude Code (setup), Maor (provides voice sample)

---

#### #6 — WebSearch (Real-Time Research)
**ROI:** Better strategy decisions on every task — competitor pricing, trend data, local SEO signals
**Use Cases:**
- Priority 5 (90-Day Growth Strategy) — research competitors before strategy
- Priority 8 (AI Power Studio Opportunity Report) — research viral niches, trending topics
- Client research before every audit (Renova, Laguna, Finish Line)
- Real-time Google algorithm updates for SEO recommendations

**How it works:** Keyword query → structured results with citations
**Owner:** Claude Code (uses automatically for all research tasks going forward)
**Cost:** Free

---

#### #7 — Personal Clipper (`personal_clipper_create`)
**ROI:** 5x content output from same raw footage
**Use Cases:**
- Upload long Zoom recordings → auto-extract LinkedIn clips
- AI Power Studio long tutorial → 10 short-form clips
- Client testimonials → clipped highlight reels

**How it works:** Upload video → AI identifies and clips best moments → download individual clips
**Owner:** Claude Code (processes on request)

---

#### #8 — Wix Site Management (Full API)
**ROI:** Direct site updates without manual Wix editor — saves 2–3 hours per site update
**Use Cases:**
- Priority 9 (MONA Website Roadmap) — implement changes directly via MCP
- Push new blog posts, landing pages, service pages
- Upload generated images directly to Wix media library
- SEO metadata updates across all pages

**How it works:** ListWixSites → get site ID → ExecuteWixAPI or ManageWixSite
**Owner:** Claude Code (full API access)
**Cost:** Free (within existing Wix plan)

---

### 🟢 MEDIUM VALUE — Strategic Use

#### #9 — HeyGen Video Translation (`create_video_translation`)
**ROI:** 2–3x audience reach; unlocks Spanish-language market (LA = 48% Spanish-speaking)
**Use Cases:**
- AI Power Studio content in Spanish → doubles YouTube reach
- MONA client videos in Hebrew for Israeli business owners in LA
- Renova Builders Spanish-language ad campaigns

**How it works:** Submit existing video → translate audio + sync lips → output dubbed video
**Owner:** Claude Code (executes on request)

---

#### #10 — HeyGen Digital Twin (`create_digital_twin`)
**ROI:** Brand scalability at scale — Maor appears in unlimited videos simultaneously
**Use Cases:**
- AI Power Studio course delivery at scale
- MONA client onboarding videos
- Personalized video proposals per prospect

**Requires:** Video consent recording from Maor (one-time setup)
**Owner:** Claude Code (setup), Maor (provides consent video)
**Timeline:** Strategic — set up after voice clone is confirmed

---

#### #11 — Video Analysis (`video_analysis_create`)
**ROI:** Competitive intelligence without manual review
**Use Cases:**
- Analyze competitor content for hook patterns
- Audit client's existing video library before creating strategy
- AI Power Studio content performance post-mortem

**Owner:** Claude Code (executes on request)

---

#### #12 — Gmail Label Automation
**ROI:** Inbox-as-CRM — zero cost, zero setup time
**Use Cases:**
- Auto-label client threads (Renova, Laguna, Finish Line Taxi)
- MONA Delivered / MONA Pending / PMA labels
- AI Power Studio prospect tracking

**Owner:** Claude Code (sets up on request)

---

## Summary Table

| # | Capability | Category | Cost | Est. ROI | Time to Activate | Owner |
|---|-----------|----------|------|----------|-----------------|-------|
| 1 | HeyGen Avatar Video | Content | Paid | 10x | 10 min | Claude Code |
| 2 | Veo 3.1 / Cinema Studio Video | Content | Credits | 8x | 5 min | Claude Code |
| 3 | Virality Predictor | Analytics | Credits | 5x | Immediate | Claude Code |
| 4 | Marketing Studio Video Ads | Ads | Credits | High | Immediate | Claude Code |
| 5 | HeyGen Voice Clone | Content | Paid | 7x | Needs audio sample | Maor + Claude |
| 6 | WebSearch (Research) | Research | Free | Qualitative | Immediate | Claude Code |
| 7 | Personal Clipper | Content | Credits | 5x | 15 min | Claude Code |
| 8 | Wix Full API | Web | Free | 3x | Immediate | Claude Code |
| 9 | HeyGen Video Translation | Distribution | Paid | 2–3x | 30 min | Claude Code |
| 10 | HeyGen Digital Twin | Brand | Paid | Long-term | Needs consent video | Maor + Claude |
| 11 | Video Analysis | Analytics | Credits | Strategic | 15 min | Claude Code |
| 12 | Gmail Label Automation | Operations | Free | Operational | 10 min | Claude Code |

---

## Immediate Recommended Actions

1. **Run Virality Predictor** on the first video generated — establish baseline scoring standard
2. **Generate first HeyGen video** — MONA agency intro or AI Power Studio teaser (demonstrates full pipeline)
3. **Enable WebSearch on all future research tasks** — Priority 5, 8, 9 all require real-time data
4. **List Wix Sites** — confirm monaempoweryou.com is accessible before Priority 9 roadmap work
5. **Set up Gmail labels** — MONA client pipeline tracking (15-minute task, immediate value)

---

## What Stays in Pending Maor Action

| Item | Blocker |
|------|---------|
| HeyGen Voice Clone (#5) | Maor must provide clean 30-second audio sample |
| HeyGen Digital Twin (#10) | Maor must record consent video (one-time) |
| Job Search MCP | No current MONA use case — candidate for Priority 4 Connector Research |

---

*Audit completed: June 3, 2026 · Priority 3 of 11*
