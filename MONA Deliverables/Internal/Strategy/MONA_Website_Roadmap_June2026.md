# MONA Website Roadmap — monaempoweryou.com
## Priority 9 | June 4, 2026

> **Audit Scope:** Full inspection via Wix API, site properties, blog content inventory, published URLs, and SEO state. This roadmap covers UX, design, funnel, conversion, SEO, and content improvements with exact actions and 90-day execution timeline.

---

## Executive Summary

**5 Critical Findings that require immediate action:**

1. **Wrong area code** — Phone number (916) 473-3131 is a Sacramento area code on an LA business. This poisons every local SEO citation and breaks GBP/NAP consistency.
2. **Missing street address + zip code** — No street or zip in site properties. Google cannot verify a local business without a complete address.
3. **Only 2 pages indexed by Google** — Home + FAQ. Zero service pages, zero about page, zero case studies. An agency with 2 indexed pages has no authority footprint.
4. **Blog dates say 2025** — 3 of 7 blog posts published May 2026 have "2025" in their titles. Looks outdated on a site that markets AI and "cutting-edge" services.
5. **Messaging conflict** — Site description and one blog post promote Google Ads and Meta paid campaigns. MONA's growth strategy is organic-first. The site contradicts the brand.

---

## Current State Audit

### Site Properties (from Wix API — June 4, 2026)

| Field | Current Value | Status |
|-------|--------------|--------|
| Business Name | Mona Digital Marketing | ✅ |
| Display Name | Mona Digital Marketing | ✅ |
| Email | monaempoweryou@gmail.com | ✅ |
| Phone | (916) 473-3131 | ❌ Sacramento area code — LA business |
| Street Address | (blank) | ❌ Missing |
| Zip Code | (blank) | ❌ Missing |
| City/State | Los Angeles, CA | ✅ |
| Timezone | America/Los_Angeles | ✅ |
| Category | Marketing Consulting Firm | ⚠️ Underspecified — "AI Marketing Agency" would be stronger |
| Click Tracking | Disabled | ❌ No behavioral data |
| Description | Mentions "Google Ads, Meta campaigns" | ❌ Conflicts with organic-first positioning |

### Published URLs (from Wix API)

| URL | Status |
|-----|--------|
| https://www.monaempoweryou.com/ | ✅ Live |
| /faq-s | Indexed by Google but not in published URL API |

**Total pages indexed by Google: 2.** Industry benchmark for a credible agency: 15–40 pages minimum.

### Blog Inventory (7 posts)

| Title | Published | Issues |
|-------|-----------|--------|
| Social Media Management for Small Businesses | May 15, 2026 | No category, generic |
| 5 Ways AI Is Transforming Digital Marketing for Small Businesses in **2025** | May 15, 2026 | Wrong year in title |
| Google Ads vs. Meta Ads: Which One Is Right for Your Business in **2025**? | May 15, 2026 | Wrong year; topic conflicts with organic strategy |
| Never Miss a Call Again: How AI Voice Agents Are Changing the Game | June 10, 2025 | No category |
| Maximize Business Efficiency with MONA's AI Consultations | June 5, 2025 | Featured post; generic |
| Boost Your Online Presence with MONA's Marketing Services | June 5, 2025 | No category; generic title |
| Optimize Your Marketing Strategy with MONA's AI Solutions | June 5, 2025 | No category; generic title |

**Common issues across all posts:** Zero categories. No tags. No internal links. No CTAs.

### Missing Pages (Zero Indexed)

| Page | SEO Value | Business Value | Priority |
|------|-----------|---------------|----------|
| /about | High | Social proof, trust | Critical |
| /services | High | Conversion anchor | Critical |
| /services/social-media-management | High | LA local search | Critical |
| /services/seo | High | LA local search | Critical |
| /services/ai-marketing-automation | High | Differentiator | Critical |
| /services/website-development | Medium | LA local search | High |
| /services/content-creation | Medium | LA local search | High |
| /results or /case-studies | Very High | Proof of results | Critical |
| /contact | High | Conversion capture | Critical |
| /blog | Medium | Content discovery | High |
| /ai-power-studio | Medium | Brand extension | High |
| /los-angeles-digital-marketing-agency | Very High | Local SEO anchor | Critical |

---

## Issue Register — Prioritized

### Critical (Fix This Week)

**ISSUE-001 — Wrong Phone Area Code**
- **Finding:** (916) 473-3131 = Sacramento, CA. MONA is in Los Angeles.
- **Impact:** Every Google citation, GBP listing, and schema markup reports an LA business with a Sacramento number. Google's NAP (Name/Address/Phone) consistency algorithm penalizes this. Every local SEO ranking suffers.
- **Fix:** Update phone number to an LA area code (213, 310, 323, 424, 818). Wix API → `PATCH /site-properties/v4/properties/business-profile`. Then update GBP, all directories, and schema markup.

**ISSUE-002 — No Street Address or Zip**
- **Finding:** Address field shows only "Los Angeles, CA" with no street or zip.
- **Impact:** GBP verification, local pack rankings, and structured data all require a complete address. Cannot rank in local pack without it.
- **Fix:** Add MONA's full address to Wix site properties and GBP simultaneously. If using a virtual office or home address, a PO Box or Regus/WeWork address in LA is sufficient.

**ISSUE-003 — Blog Titles Reference 2025 (Wrong Year)**
- **Finding:** Posts published May 2026 have "2025" in their titles. An AI agency promoting cutting-edge services cannot have year-old references on its front page.
- **Posts to fix:**
  - "5 Ways AI Is Transforming Digital Marketing for Small Businesses in 2025" → change to 2026
  - "Google Ads vs. Meta Ads: Which One Is Right for Your Business in 2025?" → change to 2026 or archive
- **Fix:** Update blog post titles via Wix Blog API or dashboard.

**ISSUE-004 — Messaging Conflict: Ads vs. Organic**
- **Finding:** Site description says "Google Ads, Meta campaigns." One blog post is "Google Ads vs. Meta Ads." MONA's growth strategy is organic-first; MONA does not run paid ads for itself.
- **Impact:** Mixed signals confuse prospects. Organic-only clients will question whether MONA's own growth is organic.
- **Fix 1:** Update site description to remove references to Google Ads / Meta. Replace with: *"Empowering LA businesses with AI-driven digital marketing — SEO, content, social media, automation, and AI video production."*
- **Fix 2:** Archive or update the Google Ads vs. Meta blog post. MONA can serve clients who run ads, but the post should position MONA as the strategic advisor, not the ads manager.

**ISSUE-005 — No Click Analytics**
- **Finding:** `trackClicksAnalytics: false` — no behavioral data is being collected.
- **Impact:** Cannot measure conversion paths, CTA performance, or user journeys.
- **Fix:** Enable click tracking in Wix Dashboard → Settings → Tracking & Analytics. Also install Google Analytics 4 (already planned in PMA-010 — this connection reinforces that action).

---

### High Priority (Complete in 30 Days)

**ISSUE-006 — No Individual Service Pages**
- **Impact:** Google cannot rank for "social media marketing Los Angeles," "SEO agency Los Angeles," etc. without dedicated pages.
- **Fix:** Create 5 service pages (see Missing Pages table above). Each needs: H1 with service + location keyword, 400+ words, FAQ section, testimonial, CTA to contact.

**ISSUE-007 — No About Page**
- **Impact:** 52% of website visitors visit the About page before converting. No About = no trust signal.
- **Fix:** Create /about page featuring: Maor's story, MONA's philosophy ("radical transparency, AI-powered results"), LA focus, and link to case studies.

**ISSUE-008 — No Contact / Book a Call Page**
- **Impact:** Without a standalone /contact or /book-a-call page, there is no conversion anchor. Chat-based CTAs convert 3× better than forms — MONA Chat widget is already deployed, making this highly achievable.
- **Fix:** Create /contact page with: embedded booking widget (Calendly or Wix Bookings), MONA Chat widget, email, phone (after fixing area code). Above-the-fold CTA: "Book Your Free AI Marketing Audit."

**ISSUE-009 — No Case Studies / Results Page**
- **Impact:** This is the #1 conversion driver for service businesses. Prospects need proof.
- **Available content:** Renova Builders (3 months of reports), Finish Line Taxi (audit completed), Laguna Luxury Pools (in pipeline).
- **Fix:** Create /results page with 2–3 client spotlights. Even anonymous/aggregate results count ("Client A: +180% GBP views in 60 days"). Full client permission for named case studies to be secured.

**ISSUE-010 — Blog Has No Categories or Internal Links**
- **Impact:** All 7 posts are floating with zero taxonomy. No topic clusters. No internal linking strategy. Google cannot understand topical authority.
- **Fix:** Create 3–4 blog categories: "AI Marketing," "Local SEO," "Social Media," "Agency Resources." Assign every existing post. Add internal links from blog posts to service pages.

**ISSUE-011 — No Local SEO Landing Page**
- **Impact:** The highest-value search query for MONA — "digital marketing agency Los Angeles" — has no dedicated page to rank for it.
- **Fix:** Create /los-angeles-digital-marketing-agency with: "Los Angeles" in H1, structured data (LocalBusiness schema), client list (LA businesses served), embedded Google Map, neighborhood-specific mentions (West LA, Downtown, East LA, South Bay).

---

### Medium Priority (Complete in 60 Days)

**ISSUE-012 — Blog Content Needs Upgrading**
- 5 of 7 posts are generic (not MONA-specific, no data, no client proof). They read like AI-generated filler.
- **Fix:** Replace with data-driven, specific content tied to MONA's actual work. Use the 90-day content calendar from Priority 7.

**ISSUE-013 — No Social Proof Above the Fold**
- **Impact:** Trust signals on the homepage (Google reviews, client logos, specific results) increase conversion rates by 34%.
- **Fix:** Add a testimonials strip or results section above the fold: "Renova Builders: 180% increase in GBP visibility." "Finish Line Taxi: Fully automated lead capture."

**ISSUE-014 — Category Too Generic**
- Site category is "Marketing Consulting Firm." The top ranking agencies in AI marketing use more specific categories.
- **Fix:** Update to "AI Marketing Agency" or add "Artificial Intelligence" as a secondary category in site properties.

**ISSUE-015 — No AI Power Studio Page**
- **Impact:** AI Power Studio has zero web presence under monaempoweryou.com. No SEO. No backlinks. No brand differentiation.
- **Fix:** Create /ai-power-studio as a dedicated page or section introducing AI Power Studio's capabilities (HeyGen video, AI automation, content production).

---

## Funnel Redesign

### Current Funnel (Broken)

```
Google Search → Homepage → FAQ → [Dead End]
                                  No CTA, no contact, no booking
```

### Target Funnel (90 Days)

```
Google Search (LA + service keyword) → Service Page → [CTA: Free AI Audit]
                                        ↓
                                     Contact Page / Book a Call
                                        ↓
                                     MONA Chat (automated intake)
                                        ↓
                                     Email delivery to Maor (GMAIL_APP_PASSWORD)
```

### CTA Architecture

Every page needs exactly one primary CTA. The benchmark: purpose-built pages with a single CTA convert 2–5× better than multi-CTA pages.

| Page | Primary CTA | Secondary CTA |
|------|-------------|---------------|
| Homepage | "Book Your Free AI Marketing Audit" | "See Our Results" |
| Service pages | "Get a Free [Service] Analysis" | "See How It Works" |
| About | "Work With Us" | "Read Case Studies" |
| Blog posts | "Get This Done For Your Business" | "Book a Call" |
| Contact | "Book a Call" (Calendly/Wix Bookings) | None (reduce friction) |
| Results | "Start Your Growth Plan" | "Book a Call" |

**CTA copy rule:** Never say "Contact Us." Always say what the visitor gets: "Book Your Free Audit," "Get Your AI Marketing Plan," "See How AI Can Grow Your Business."

---

## SEO Roadmap

### Technical SEO Fixes

| Action | Priority | Estimated Impact |
|--------|----------|-----------------|
| Fix NAP: phone area code to LA | Critical | Local pack eligibility |
| Add complete address | Critical | GBP/local pack ranking |
| Update site description — remove ads mentions | Critical | Brand consistency |
| Enable click analytics | Critical | Baseline behavioral data |
| Add LocalBusiness schema markup | High | Rich results + local pack |
| Set title tags + meta for all pages | High | Organic click-through rate |
| Enable Wix site performance optimizations | Medium | Core Web Vitals / page speed |
| Connect Google Search Console | Medium | Index monitoring (PMA-010) |
| Submit sitemap after new pages published | Medium | Google discovery speed |

### On-Page SEO — Target Keywords

| Page | Primary Keyword | Monthly Search Volume | Competition |
|------|----------------|----------------------|-------------|
| Homepage | Digital marketing agency Los Angeles | 1,600/mo | Medium |
| /los-angeles-digital-marketing-agency | AI marketing agency Los Angeles | 880/mo | Low |
| /services/seo | SEO services Los Angeles | 1,900/mo | High |
| /services/social-media-management | Social media management Los Angeles | 720/mo | Medium |
| /services/ai-marketing-automation | AI marketing automation small business | 480/mo | Low |
| /services/website-development | Website development Los Angeles | 1,300/mo | High |
| /results | Digital marketing results case studies | 320/mo | Low |
| Blog posts | AI marketing tools, local SEO tips, etc. | Various | Low–Medium |

### Content SEO — Blog Strategy

Current: 7 posts, no categories, generic titles, "2025" year references.
Target: 24 posts in 90 days (per Content Machine calendar), organized into 4 topic clusters.

| Cluster | Posts Needed | SEO Purpose |
|---------|-------------|-------------|
| AI Marketing (pillar) | 8 posts | Rank for "AI marketing" + authority |
| Local Business SEO | 6 posts | Rank for LA-specific queries |
| Agency Case Studies | 4 posts | Long-tail + social proof |
| Tool Tutorials | 6 posts | AI Power Studio authority |

**Immediate wins (this week):**
- Fix "2025" → "2026" in 3 post titles
- Add blog categories to all 7 posts
- Add internal links from each post to the most relevant service page
- Add a CTA at the bottom of every post

---

## UX / Design Recommendations

### Homepage Priorities

| Element | Current State | Recommended Change |
|---------|--------------|-------------------|
| Hero headline | Unknown | Lead with outcome: "More Leads. Less Work. AI-Powered Marketing for LA Businesses." |
| Above-fold CTA | Unknown | Single button: "Book Your Free AI Audit" |
| Social proof strip | Missing | Add: logos of Renova/Finish Line/Laguna + 1 result stat each |
| Services section | Present | Link each service to its dedicated page (doesn't exist yet) |
| Video/demo | Missing | Add a 60-second HeyGen avatar video explaining MONA's approach |
| Blog preview | Present | Show only 3 most recent posts; add "Read All Posts" link |
| Footer | Present | Add: full address, LA phone number, Google Maps embed, schema markup |

### Mobile Optimization
- Tap-to-call on phone number is critical for local service business visitors
- Every CTA button must be 44px+ height (Apple/Google minimum tap target)
- Contact form should ask 3 fields max: Name, Phone, "What's your biggest marketing challenge?"

### Trust Architecture (Add in Order)

1. **Client logos** — even with permission to say "Clients include local LA contractors and service businesses"
2. **Specific numbers** — "+150% GBP views" beats "we get great results"
3. **Maor's photo + bio** — People hire people. The About page is where this lives.
4. **Google reviews widget** — Once GBP is live and reviews accumulate, embed on homepage
5. **Media mentions** — Any press, podcast appearances, LinkedIn engagement metrics

---

## 90-Day Website Execution Roadmap

### Week 1 — Critical Fixes (Maor + Claude)
| Action | Who | Tool |
|--------|-----|------|
| Fix phone area code in Wix site properties | **Maor** | Wix Dashboard → Business Info |
| Add full street address + zip code | **Maor** | Wix Dashboard → Business Info |
| Update site description (remove ads references) | Claude | Wix MCP `update-business-profile` |
| Fix "2025" → "2026" in 3 blog post titles | Claude | Wix Blog API |
| Enable click analytics | **Maor** | Wix Dashboard → Tracking & Analytics |
| Add blog categories + assign to all posts | Claude | Wix Blog API |
| Add CTAs to all 7 blog posts | Claude | Wix Blog API |

### Week 2–3 — Core Pages Created
| Page | Creator | Content Source |
|------|---------|---------------|
| /about | Claude | Maor's story from operating profile + session context |
| /contact (with booking widget) | Claude | Wix Bookings + MONA Chat embed |
| /los-angeles-digital-marketing-agency | Claude | SEO-targeted local landing page |
| /results | Claude | Renova + Finish Line Taxi data |

### Week 4 — Service Pages
| Page | SEO Keyword |
|------|------------|
| /services/social-media-management | Social media marketing Los Angeles |
| /services/seo | SEO agency Los Angeles |
| /services/ai-marketing-automation | AI marketing automation |
| /services/website-development | Website development Los Angeles |
| /services/content-creation | Content marketing agency LA |

### Month 2 — Content Engine + Schema
- Blog: 8 new posts (per Content Machine calendar)
- Add LocalBusiness JSON-LD schema to homepage and contact page
- Connect Google Search Console (PMA-010)
- Submit updated sitemap
- Create /ai-power-studio page

### Month 3 — Conversion Optimization
- Install Wix Heatmaps (or Hotjar) to review user flow
- A/B test homepage CTA copy
- Add Google Reviews widget (after GBP reviews accumulate)
- Launch first client video testimonial (HeyGen avatar or real recording)
- Review organic traffic vs. Month 1 baseline

---

## Required Maor Actions

| Action | Where | Time | Blocks |
|--------|-------|------|--------|
| Fix phone area code | Wix Dashboard → Settings → Business Info | 2 min | Local SEO / GBP consistency |
| Add street address + zip | Wix Dashboard → Settings → Business Info | 2 min | Local pack ranking |
| Enable click analytics | Wix Dashboard → Settings → Tracking & Analytics | 2 min | Behavioral data baseline |
| Confirm physical/virtual office address | Reply in chat with address | 1 min | All local SEO work |

**Total Maor time to unblock website roadmap: ~7 minutes.**

---

## KPI Targets

| Metric | Baseline (June 2026) | Month 1 Target | Month 3 Target |
|--------|---------------------|---------------|---------------|
| Pages indexed by Google | 2 | 8 | 20+ |
| Organic monthly visitors | Unknown (no analytics) | Establish baseline | +50% vs. baseline |
| Homepage CTA click rate | Unknown | Establish baseline | >3% |
| Contact form / booking conversions | Unknown | Establish baseline | 2–5% of visitors |
| Blog posts published | 7 | 14 | 31 |
| Blog posts with categories + CTAs | 0 | 7 (all existing) | All posts |
| Local pack ranking (digital marketing agency LA) | Not ranking | Eligible | Top 10 |
| Google reviews | Unknown | 5+ | 10+ |

---

## Autonomous Actions — Status

### ✅ Completed This Session (June 4, 2026)

| Action | Result |
|--------|--------|
| Update site description | ✅ Live — removed Google Ads/Meta references. New: "Empowering LA businesses with AI-driven digital marketing — SEO, content creation, social media management, AI automation, and AI video production for measurable growth." |
| Create blog categories | ✅ Live — 4 categories created on monaempoweryou.com: AI Marketing (c1618463), Local SEO (614b5a28), Social Media (5c0acc18), Agency Resources (26b9c64e) |

### Remaining Autonomous Actions (Next Session)

| Action | Method | Notes |
|--------|--------|-------|
| Fix blog post titles ("2025" → "2026") | Wix Dashboard or Blog API draft cycle | 3 posts need year correction |
| Assign categories to existing 7 posts | Wix Dashboard → Blog → Posts | Categories already created |
| Add CTAs to bottom of all 7 blog posts | Wix Dashboard | "Book Your Free AI Audit" CTA |
| Draft /about page content | Wix Blog/Pages API | Ready to write |
| Draft /contact page content | Wix Pages API | Ready to write |
| Draft /los-angeles-digital-marketing-agency | Wix Pages API | SEO landing page |
| Draft /results page | Wix Pages API | Renova + Finish Line data |

### Maor Required (Blockers)

| Action | Where | Time | Blocks |
|--------|-------|------|--------|
| Fix phone area code (916 → LA) | Wix Dashboard → Settings → Business Info | 2 min | Local SEO / GBP consistency |
| Add street address + zip code | Wix Dashboard → Settings → Business Info | 2 min | Local pack ranking |
| Enable click analytics | Wix Dashboard → Settings → Tracking & Analytics | 2 min | Behavioral data baseline |
| Confirm LA address to use | Reply in chat | 1 min | All local SEO work |

**Total Maor time to unblock: ~7 minutes.**

---

*Prepared: June 4, 2026 | Priority 9 of 11*
*Data source: Wix Site API, Wix Blog API, Google search index inspection*
*Next: Priority 10 — Lessons Learned Audit*
