import os
import json
import re
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from flask import Flask, request, Response, stream_with_context, send_file
from flask_cors import CORS
import anthropic

app = Flask(__name__)
CORS(app, origins="*")

client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

# ─── System Prompts ────────────────────────────────────────────────────────────

MONA_PROMPT = """You are Mona — the internal operations assistant for Mona Digital Marketing agency, Los Angeles.

Your primary user is Nataly (business partner). She should be able to describe anything she needs in plain language and you handle the rest. She never needs to understand the agency structure, tools, or workflows.

## Your role
You are the intake layer. You gather information from Nataly, then hand off to the agency system for execution.
- Text-based work (proposals, invoices, emails, reports, blog posts, social copy, SEO) → executes automatically, result delivered to email.
- Content work (images, video, graphics, design) → flagged for Maor's approval before production starts.

You do NOT explain the system to Nataly. You do NOT mention agents, routing, or approvals. You just ask what you need and say "On it."

## Conversation flow

STEP 1 — Understand what she needs.
STEP 2 — Ask only the minimum questions, one at a time, in plain language:

- Proposal: client name, contact info, services being offered, any pricing discussed, deadline
- Invoice: client name, services rendered, amount
- Email: who it's going to, what it's about, any specific tone or details
- Blog post: topic, which client/website it's for, any keywords or focus
- Social content: which client, platform(s), topic or campaign, deadline
- Report: which client, what period, what to include
- Website change: which site, what to change, any examples or notes
- Video/image: what it's for, style or reference, deadline

Never ask more than needed. Never use technical language.

## Once you have enough

Say: "Got it. I'm on it — you'll have this shortly."
Then stop. The backend takes over from here.

If the request involves images, video, or graphic design, say:
"Got it. This needs visual production — I'll flag it for Maor to approve before we move forward."

## Tone
Warm, confident, human. Like a capable assistant who has everything handled. Nataly should always feel like things are moving."""

COO_PROMPT = """You are the Agency Manager of Mona Digital Marketing, Los Angeles. You receive requests that came in through the agency's intake assistant and you execute them — fully and completely, without waiting for human approval.

Agency clients: Renova Builders (remodeling, Bay Area), Finish Line Taxi (taxi, Temecula), Mona Digital Marketing (the agency itself, Los Angeles).
Agency services: SEO, Google Ads, Meta Ads, Social Media, Web Design, AI content, Monthly Reports, Invoices, Proposals, Email campaigns.
Agency email for deliverables: monaempoweryou@gmail.com

Your job: read the request, route it to the right function, and produce the actual deliverable. No placeholders. No "a draft will follow." Write the real thing.

Respond ONLY with valid JSON in this exact format:
{
  "agent": "one of: blog-writer | social-content | monthly-report | invoice | proposal | seo-audit | email-draft | web-change | graphic-design",
  "client": "client name or 'mona' for internal",
  "task_summary": "one sentence",
  "deliverable": "what this is",
  "needs_approval": false,
  "content": "the complete deliverable — full HTML invoice, full proposal, full blog post, all social posts ready to publish, complete email, etc."
}

Set needs_approval to true ONLY if the request requires image, video, or graphic design production. For all text-based work, needs_approval is always false — execute immediately.

Deliverable standards:
- Invoice: complete HTML with Mona branding, client info, line items, totals, payment terms
- Proposal: full professional HTML proposal with scope, deliverables, pricing, timeline
- Blog post: full SEO-optimized post with title, intro, headings, body, conclusion
- Social content: every post written out, labeled by platform, ready to copy-paste
- Report: complete HTML report with all relevant data sections
- Email: complete email, subject line included, ready to send
- Web change: exact copy/content/instructions needed to make the change"""

# ─── COO Router ────────────────────────────────────────────────────────────────

def is_production_request(message: str) -> bool:
    """Determine if this is a task to execute vs an information request."""
    keywords = [
        "write", "create", "make", "generate", "build", "draft",
        "invoice", "report", "proposal", "blog", "post", "social",
        "email", "send", "audit", "design", "update", "add", "publish"
    ]
    msg_lower = message.lower()
    return any(kw in msg_lower for kw in keywords)

def run_coo(message: str, history: list) -> dict:
    """Run the Agency Manager: first get routing plan, then generate content separately."""
    context = ""
    if history:
        recent = history[-4:] if len(history) > 4 else history
        context = "\n".join([f"{h['role'].upper()}: {h['content']}" for h in recent])
        context = f"Recent conversation:\n{context}\n\n"

    # Step 1: Get routing plan (small JSON, no content yet)
    routing_prompt = """You are the Agency Manager of Mona Digital Marketing. Given a request, respond ONLY with this JSON (no content field yet):
{
  "agent": "blog-writer|social-content|monthly-report|invoice|proposal|seo-audit|email-draft|web-change|graphic-design",
  "client": "client name or mona",
  "task_summary": "one sentence",
  "deliverable": "what this is",
  "needs_approval": false
}
Set needs_approval true ONLY for image/video/graphic-design requests."""

    plan_resp = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=300,
        system=routing_prompt,
        messages=[{"role": "user", "content": f"{context}Request: {message}"}]
    )
    raw = plan_resp.content[0].text.strip()
    match = re.search(r'\{.*\}', raw, re.DOTALL)
    plan = json.loads(match.group() if match else raw)

    # Step 2: Generate the actual content separately (clean text, not inside JSON)
    if not plan.get("needs_approval", False):
        content_resp = client.messages.create(
            model="claude-haiku-4-5-20251001",
            max_tokens=2000,
            system=COO_PROMPT,
            messages=[{"role": "user", "content": f"Write the complete {plan.get('deliverable','deliverable')} for this request: {message}\nClient: {plan.get('client','')}\nOutput the full deliverable as HTML, ready to email. No JSON wrapper."}]
        )
        plan["content"] = content_resp.content[0].text.strip()
    else:
        plan["content"] = f"<p><strong>Request:</strong> {message}</p><p>This requires visual/content production. Awaiting approval to proceed.</p>"

    return plan

def send_to_email(subject: str, body_html: str):
    """Send execution result to monaempoweryou@gmail.com via Gmail SMTP."""
    smtp_user = os.environ.get("GMAIL_USER", "monaempoweryou@gmail.com")
    smtp_pass = os.environ.get("GMAIL_APP_PASSWORD")

    if not smtp_pass:
        return False

    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = smtp_user
    msg["To"] = smtp_user
    msg.attach(MIMEText(body_html, "html"))

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, timeout=15) as server:
            server.login(smtp_user, smtp_pass)
            server.sendmail(smtp_user, smtp_user, msg.as_string())
        return True
    except Exception as e:
        print(f"Email error: {e}")
        return False

def format_email_body(plan: dict, approval_required: bool = False) -> str:
    """Format the Agency Manager output as a clean email."""
    agent_labels = {
        "blog-writer": "Blog Post",
        "social-content": "Social Media Content",
        "monthly-report": "Monthly Report",
        "invoice": "Invoice",
        "proposal": "Proposal",
        "seo-audit": "SEO Audit",
        "email-draft": "Email Draft",
        "web-change": "Web Change Request",
        "graphic-design": "Design Brief",
    }
    label = agent_labels.get(plan.get("agent", ""), "Deliverable")
    client_name = plan.get("client", "").title()
    task = plan.get("task_summary", "")
    content = plan.get("content", "")

    if approval_required:
        banner = """
  <div style="background:#F39C12;padding:12px 24px;color:#fff;font-size:13px;font-weight:600;">
    ACTION REQUIRED — Visual/content production requested. Review and approve before execution.
  </div>"""
        footer_note = "Awaiting Maor approval before production begins"
    else:
        banner = ""
        footer_note = "Produced by Mona Agency OS · Review before sending to client"

    return f"""
<div style="font-family:Arial,sans-serif;max-width:700px;margin:0 auto;color:#1B2D4F;">
  <div style="background:#1B2D4F;padding:20px 24px;border-bottom:3px solid #2E86C1;">
    <h2 style="color:#fff;margin:0;font-size:18px;">Mona Agency — {label}</h2>
    <p style="color:rgba(255,255,255,0.7);margin:4px 0 0;font-size:13px;">Client: {client_name} · {task}</p>
  </div>{banner}
  <div style="padding:24px;background:#f8fbfe;border:1px solid #d4e6f5;">
    {content}
  </div>
  <div style="padding:12px 24px;background:#EBF5FB;font-size:11px;color:#5DADE2;text-align:center;">
    {footer_note}
  </div>
</div>
"""

# ─── UNVEILED Communication System ────────────────────────────────────────────
# Brand: Dark #111111, Gold #C4A35A, White #F5F5F5
# Rule: Website = proposal. Email = bridge. No pricing. CTA = start conversation.

def unveiled_outreach_email(
    first_name: str,
    business_name: str,
    business_type: str,
    location: str,
    website_url: str,
    what_we_built: str,
    why_it_matters: str,
) -> str:
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>UNVEILED</title>
</head>
<body style="margin:0;padding:0;background:#0C0C0C;font-family:'Helvetica Neue',Helvetica,Arial,sans-serif;">

<!-- OUTER WRAPPER -->
<table width="100%" cellpadding="0" cellspacing="0" border="0" style="background:#0C0C0C;">
<tr><td align="center" style="padding:40px 16px 60px;">

<table width="620" cellpadding="0" cellspacing="0" border="0" style="max-width:620px;width:100%;">

  <!-- HEADER -->
  <tr>
    <td style="padding:0 0 1px 0;background:#0C0C0C;">
      <table width="100%" cellpadding="0" cellspacing="0" border="0">
        <tr>
          <td style="padding:36px 40px 28px;border-bottom:1px solid #C4A35A;">
            <p style="margin:0;color:#C4A35A;font-size:10px;font-weight:700;letter-spacing:5px;text-transform:uppercase;">DIGITAL EXPERIENCES</p>
            <h1 style="margin:8px 0 0;color:#F5F5F5;font-size:32px;font-weight:800;letter-spacing:8px;text-transform:uppercase;line-height:1;">UNVEILED</h1>
          </td>
        </tr>
      </table>
    </td>
  </tr>

  <!-- BODY -->
  <tr>
    <td style="background:#111111;padding:44px 40px 40px;">

      <p style="margin:0 0 28px;color:#F5F5F5;font-size:17px;font-weight:400;line-height:1.7;">{first_name},</p>

      <p style="margin:0 0 22px;color:#D0D0D0;font-size:15px;line-height:1.85;font-weight:300;">{what_we_built}</p>

      <p style="margin:0 0 36px;color:#D0D0D0;font-size:15px;line-height:1.85;font-weight:300;">{why_it_matters}</p>

      <!-- DIVIDER -->
      <table width="100%" cellpadding="0" cellspacing="0" border="0" style="margin-bottom:36px;">
        <tr><td style="border-top:1px solid #2A2A2A;"></td></tr>
      </table>

      <!-- BUSINESS TAG -->
      <p style="margin:0 0 12px;color:#888888;font-size:11px;letter-spacing:3px;text-transform:uppercase;">Built for</p>
      <p style="margin:0 0 6px;color:#F5F5F5;font-size:20px;font-weight:700;letter-spacing:-0.3px;">{business_name}</p>
      <p style="margin:0 0 36px;color:#888888;font-size:13px;">{business_type} &nbsp;·&nbsp; {location}</p>

      <!-- PRIMARY CTA -->
      <table cellpadding="0" cellspacing="0" border="0" style="margin-bottom:16px;">
        <tr>
          <td style="border:1px solid #C4A35A;border-radius:4px;">
            <a href="{website_url}" style="display:block;padding:15px 36px;color:#C4A35A;text-decoration:none;font-size:13px;font-weight:700;letter-spacing:3px;text-transform:uppercase;white-space:nowrap;">See What We Built For You &nbsp;→</a>
          </td>
        </tr>
      </table>

      <!-- SECONDARY CTA -->
      <p style="margin:0 0 36px;color:#666666;font-size:13px;">Or <a href="mailto:monaempoweryou@gmail.com" style="color:#C4A35A;text-decoration:none;font-weight:600;">reply to this email</a> — we read every response.</p>

      <!-- DIVIDER -->
      <table width="100%" cellpadding="0" cellspacing="0" border="0" style="margin-bottom:32px;">
        <tr><td style="border-top:1px solid #2A2A2A;"></td></tr>
      </table>

      <!-- CONFIDENCE STATEMENT -->
      <p style="margin:0;color:#555555;font-size:13px;line-height:1.8;font-style:italic;">No obligation. No pressure. We built this because we believe your business deserves a digital presence that actually works for you. Take a look — if it resonates, let's talk.</p>

    </td>
  </tr>

  <!-- FOOTER -->
  <tr>
    <td style="background:#0C0C0C;padding:28px 40px;border-top:1px solid #C4A35A;">
      <table width="100%" cellpadding="0" cellspacing="0" border="0">
        <tr>
          <td>
            <p style="margin:0 0 4px;color:#C4A35A;font-size:11px;font-weight:700;letter-spacing:4px;text-transform:uppercase;">UNVEILED</p>
            <p style="margin:0;color:#444444;font-size:12px;line-height:1.6;">Digital experiences built before the conversation starts.<br>Los Angeles, CA &nbsp;·&nbsp; monaempoweryou@gmail.com</p>
          </td>
          <td style="text-align:right;vertical-align:top;">
            <p style="margin:0;color:#333333;font-size:11px;line-height:1.6;">Curious?<br><a href="mailto:monaempoweryou@gmail.com?subject=Re: {business_name} Website" style="color:#C4A35A;text-decoration:none;font-weight:600;">Let's talk</a></p>
          </td>
        </tr>
      </table>
    </td>
  </tr>

</table>
</td></tr>
</table>

</body>
</html>"""


def platinum_pool_unveiled_html() -> str:
    return unveiled_outreach_email(
        first_name="John",
        business_name="Platinum Pool &amp; Property Services LLC",
        business_type="Pool &amp; Property Services",
        location="Inland Empire, CA",
        website_url="https://mona-chat-ap.onrender.com/platinum-pool",
        what_we_built="We put together a custom website for Platinum Pool &amp; Property Services — designed around your services, your service area, and the customers you want to reach across the Inland Empire. It's live right now.",
        why_it_matters="Most pool and property service companies in your market have outdated websites or no website at all. This gives you a professional presence that works 24/7 — capturing leads while you're on the job, not chasing them after.",
    )


def goldsmith_unveiled_html(website_url: str) -> str:
    return unveiled_outreach_email(
        first_name="there",
        business_name="Goldsmith Financial",
        business_type="Financial Services",
        location="Los Angeles, CA",
        website_url=website_url,
        what_we_built="We built a custom website for Goldsmith Financial — a professional digital presence designed to reflect the quality and trust your clients already experience working with you.",
        why_it_matters="In financial services, first impressions close deals before the first meeting. This gives you a digital front door that matches your credibility — and converts the visitors who find you online into clients who call.",
    )


# ─── Platinum Pool Proposal Email (legacy — superseded by UNVEILED system) ────

def platinum_pool_proposal_html() -> str:
    return """<!DOCTYPE html>
<html>
<head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1"></head>
<body style="margin:0;padding:0;background:#f0f4f8;font-family:'Helvetica Neue',Arial,sans-serif;">
<div style="max-width:680px;margin:32px auto;background:#ffffff;border-radius:12px;overflow:hidden;box-shadow:0 4px 24px rgba(13,27,62,0.12);">

  <!-- HEADER -->
  <div style="background:linear-gradient(135deg,#0D1B3E 0%,#0D2B6B 60%,#0095DA 100%);padding:40px 36px 32px;text-align:center;">
    <div style="display:inline-block;background:rgba(255,255,255,0.08);border:2px solid rgba(0,149,218,0.4);border-radius:10px;padding:14px 28px;margin-bottom:20px;">
      <p style="margin:0;color:#0095DA;font-size:11px;font-weight:700;letter-spacing:3px;text-transform:uppercase;">PLATINUM POOL &amp; PROPERTY SERVICES LLC</p>
    </div>
    <h1 style="margin:0 0 8px;color:#ffffff;font-size:28px;font-weight:800;letter-spacing:-0.5px;line-height:1.2;">Your Website Is Live &amp; Ready</h1>
    <p style="margin:0;color:rgba(255,255,255,0.75);font-size:15px;line-height:1.5;">A professional digital presence built to win more customers in the Inland Empire</p>
    <div style="margin-top:24px;display:inline-block;background:rgba(0,149,218,0.2);border:1px solid rgba(0,149,218,0.5);border-radius:20px;padding:6px 18px;">
      <span style="color:#00B8F0;font-size:12px;font-weight:600;letter-spacing:1px;">&#10003; APPROVED &amp; DEPLOYED</span>
    </div>
  </div>

  <!-- LIVE LINK BANNER -->
  <div style="background:#0095DA;padding:16px 36px;text-align:center;">
    <p style="margin:0;color:#fff;font-size:14px;">Your live website: <a href="https://mona-chat-ap.onrender.com/platinum-pool" style="color:#fff;font-weight:700;text-decoration:underline;">https://mona-chat-ap.onrender.com/platinum-pool</a></p>
  </div>

  <!-- BODY -->
  <div style="padding:36px;">

    <p style="margin:0 0 20px;color:#0D1B3E;font-size:16px;line-height:1.7;">Hi John,</p>
    <p style="margin:0 0 20px;color:#3a4a5c;font-size:15px;line-height:1.8;">
      Your new website for <strong>Platinum Pool &amp; Property Services</strong> is live and ready for customers to find you. It's built to rank on Google, convert visitors into booked jobs, and give your business the professional look that wins in a competitive market.
    </p>
    <p style="margin:0 0 28px;color:#3a4a5c;font-size:15px;line-height:1.8;">
      Here's what's included and what happens next.
    </p>

    <!-- WHAT'S INCLUDED -->
    <div style="background:#f0f7ff;border-left:4px solid #0095DA;border-radius:0 8px 8px 0;padding:20px 24px;margin-bottom:28px;">
      <h3 style="margin:0 0 14px;color:#0D1B3E;font-size:16px;font-weight:700;">What's Live Right Now</h3>
      <table style="width:100%;border-collapse:collapse;">
        <tr><td style="padding:5px 0;color:#3a4a5c;font-size:14px;">&#10003;&nbsp; Custom-branded hero with Pool Blue + Navy design</td></tr>
        <tr><td style="padding:5px 0;color:#3a4a5c;font-size:14px;">&#10003;&nbsp; Interactive booking calendar with time slots</td></tr>
        <tr><td style="padding:5px 0;color:#3a4a5c;font-size:14px;">&#10003;&nbsp; Full Pool Services + Property Services pages</td></tr>
        <tr><td style="padding:5px 0;color:#3a4a5c;font-size:14px;">&#10003;&nbsp; Service area map — Inland Empire, Riverside, San Bernardino</td></tr>
        <tr><td style="padding:5px 0;color:#3a4a5c;font-size:14px;">&#10003;&nbsp; Mobile-first with sticky Call &amp; Book buttons</td></tr>
        <tr><td style="padding:5px 0;color:#3a4a5c;font-size:14px;">&#10003;&nbsp; Testimonials, Gallery, Contact form wired to your email</td></tr>
      </table>
    </div>

    <!-- INVESTMENT / ANCHOR PRICING -->
    <h2 style="margin:0 0 6px;color:#0D1B3E;font-size:20px;font-weight:800;">Your Investment</h2>
    <p style="margin:0 0 20px;color:#6b7a8d;font-size:13px;">No contracts. No surprises. Priced for small business owners who need real results.</p>

    <!-- CROSSED-OUT ANCHOR -->
    <div style="background:#fff8f0;border:1px dashed #e0c080;border-radius:8px;padding:16px 20px;margin-bottom:12px;text-align:center;">
      <p style="margin:0;color:#a0855a;font-size:13px;letter-spacing:1px;text-transform:uppercase;font-weight:600;">Standard Agency Rate</p>
      <p style="margin:4px 0 0;color:#c0a060;font-size:26px;font-weight:700;text-decoration:line-through;">$4,500</p>
      <p style="margin:4px 0 0;color:#a0855a;font-size:12px;">Custom website build + branding</p>
    </div>

    <!-- FEATURED PRICE -->
    <div style="background:linear-gradient(135deg,#0D1B3E,#0D2B6B);border-radius:10px;padding:28px 24px;margin-bottom:12px;text-align:center;position:relative;overflow:hidden;">
      <div style="position:absolute;top:12px;right:12px;background:#0095DA;color:#fff;font-size:10px;font-weight:700;padding:4px 10px;border-radius:10px;letter-spacing:1px;">LAUNCH SPECIAL</div>
      <p style="margin:0 0 4px;color:rgba(255,255,255,0.7);font-size:12px;letter-spacing:2px;text-transform:uppercase;">You Invest Only</p>
      <p style="margin:0;color:#ffffff;font-size:52px;font-weight:900;line-height:1;">$997</p>
      <p style="margin:4px 0 0;color:#00B8F0;font-size:14px;font-weight:600;">One-Time · Yours to Keep</p>
      <div style="margin-top:16px;border-top:1px solid rgba(255,255,255,0.15);padding-top:16px;">
        <p style="margin:0;color:rgba(255,255,255,0.8);font-size:13px;line-height:1.6;">Custom design · All 9 sections · Mobile-optimized · Booking calendar · Contact form · Branded to your business</p>
      </div>
    </div>

    <!-- ADD-ON -->
    <div style="background:#f8f9ff;border:1px solid #d0ddf5;border-radius:10px;padding:20px 24px;margin-bottom:28px;">
      <div style="display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:10px;">
        <div>
          <p style="margin:0;color:#0D1B3E;font-size:15px;font-weight:700;">Optional: Monthly Growth Package</p>
          <p style="margin:4px 0 0;color:#6b7a8d;font-size:13px;line-height:1.6;">SEO optimization · Google Business · Monthly updates · New service pages · Review management</p>
        </div>
        <div style="text-align:right;min-width:100px;">
          <p style="margin:0;color:#0095DA;font-size:24px;font-weight:800;">$297<span style="font-size:13px;color:#6b7a8d;font-weight:400;">/mo</span></p>
          <p style="margin:2px 0 0;color:#6b7a8d;font-size:11px;">Cancel anytime</p>
        </div>
      </div>
    </div>

    <!-- WHY NOW -->
    <div style="background:#0D1B3E;border-radius:10px;padding:24px;margin-bottom:28px;">
      <h3 style="margin:0 0 12px;color:#00B8F0;font-size:15px;font-weight:700;letter-spacing:0.5px;">Why This Window Matters</h3>
      <p style="margin:0 0 10px;color:rgba(255,255,255,0.85);font-size:14px;line-height:1.7;">Pool season is here. Every day without a professional website is another customer calling your competitor. Your site is ready — you just need to say go.</p>
      <p style="margin:0;color:rgba(255,255,255,0.65);font-size:13px;line-height:1.6;">The launch special expires when the next client signs. There are no guarantees this price holds after that.</p>
    </div>

    <!-- CTA -->
    <div style="text-align:center;margin-bottom:32px;">
      <a href="https://mona-chat-ap.onrender.com/platinum-pool" style="display:inline-block;background:linear-gradient(135deg,#0095DA,#00B8F0);color:#fff;text-decoration:none;padding:16px 40px;border-radius:8px;font-size:16px;font-weight:700;letter-spacing:0.5px;box-shadow:0 4px 16px rgba(0,149,218,0.4);">View Your Live Website &rarr;</a>
      <p style="margin:12px 0 0;color:#6b7a8d;font-size:13px;">Questions? Reply to this email or call <strong>(909) 970-1982</strong></p>
    </div>

    <!-- NEXT STEPS -->
    <div style="border-top:2px solid #e8edf5;padding-top:24px;">
      <h3 style="margin:0 0 14px;color:#0D1B3E;font-size:15px;font-weight:700;">What Happens After You Say Yes</h3>
      <table style="width:100%;border-collapse:collapse;">
        <tr style="vertical-align:top;">
          <td style="padding:8px 0;width:28px;"><div style="width:22px;height:22px;background:#0095DA;border-radius:50%;color:#fff;font-size:12px;font-weight:700;text-align:center;line-height:22px;">1</div></td>
          <td style="padding:8px 0 8px 10px;color:#3a4a5c;font-size:14px;">You confirm — we send the payment link instantly</td>
        </tr>
        <tr style="vertical-align:top;">
          <td style="padding:8px 0;"><div style="width:22px;height:22px;background:#0095DA;border-radius:50%;color:#fff;font-size:12px;font-weight:700;text-align:center;line-height:22px;">2</div></td>
          <td style="padding:8px 0 8px 10px;color:#3a4a5c;font-size:14px;">We transfer the site to your own domain (e.g. platinumpoolservices.com)</td>
        </tr>
        <tr style="vertical-align:top;">
          <td style="padding:8px 0;"><div style="width:22px;height:22px;background:#0095DA;border-radius:50%;color:#fff;font-size:12px;font-weight:700;text-align:center;line-height:22px;">3</div></td>
          <td style="padding:8px 0 8px 10px;color:#3a4a5c;font-size:14px;">You start receiving booking requests from new customers</td>
        </tr>
      </table>
    </div>

  </div>

  <!-- FOOTER -->
  <div style="background:#0D1B3E;padding:24px 36px;text-align:center;">
    <p style="margin:0 0 6px;color:#ffffff;font-size:14px;font-weight:700;">Platinum Pool &amp; Property Services LLC</p>
    <p style="margin:0 0 4px;color:rgba(255,255,255,0.6);font-size:13px;">John Dithommaso Jr · (909) 970-1982</p>
    <p style="margin:0 0 16px;color:rgba(255,255,255,0.6);font-size:13px;">johndithommasojr@gmail.com · Inland Empire, CA</p>
    <p style="margin:0;color:rgba(255,255,255,0.35);font-size:11px;">Presented by Mona Digital Marketing · Digital Growth Partner</p>
  </div>

</div>
</body>
</html>"""

# ─── MONA Client Communication Standard — Renova Builders ─────────────────────
# Permanent MONA template: Navy #1B2D4F, Blue #2E86C1, clean professional structure.
# This report becomes the foundation for all MONA client update communications.

def renova_strategic_update_html() -> str:
    return """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Renova Builders — Strategic Account Review</title>
</head>
<body style="margin:0;padding:0;background:#ECF0F5;font-family:'Helvetica Neue',Helvetica,Arial,sans-serif;">

<table width="100%" cellpadding="0" cellspacing="0" border="0" style="background:#ECF0F5;">
<tr><td align="center" style="padding:32px 16px 48px;">
<table width="680" cellpadding="0" cellspacing="0" border="0" style="max-width:680px;width:100%;">

  <!-- ── MONA HEADER ── -->
  <tr>
    <td style="background:linear-gradient(135deg,#1B2D4F 0%,#1a3a6b 100%);padding:28px 36px 24px;border-bottom:3px solid #2E86C1;">
      <table width="100%" cellpadding="0" cellspacing="0" border="0">
        <tr>
          <td>
            <p style="margin:0;color:rgba(255,255,255,0.5);font-size:10px;font-weight:700;letter-spacing:4px;text-transform:uppercase;">Mona Digital Marketing</p>
            <h1 style="margin:6px 0 0;color:#ffffff;font-size:22px;font-weight:800;letter-spacing:-0.3px;">Strategic Account Review</h1>
          </td>
          <td style="text-align:right;vertical-align:middle;">
            <p style="margin:0;color:#2E86C1;font-size:11px;font-weight:700;letter-spacing:2px;text-transform:uppercase;">Google Ads</p>
            <p style="margin:4px 0 0;color:rgba(255,255,255,0.6);font-size:12px;">June 2026</p>
          </td>
        </tr>
      </table>
    </td>
  </tr>

  <!-- CLIENT NAMEPLATE -->
  <tr>
    <td style="background:#2E86C1;padding:14px 36px;">
      <table width="100%" cellpadding="0" cellspacing="0" border="0">
        <tr>
          <td>
            <p style="margin:0;color:#fff;font-size:16px;font-weight:700;">Renova Builders</p>
            <p style="margin:2px 0 0;color:rgba(255,255,255,0.75);font-size:12px;">Bay Area, CA &nbsp;·&nbsp; Residential Remodeling &amp; Construction</p>
          </td>
          <td style="text-align:right;">
            <p style="margin:0;color:rgba(255,255,255,0.6);font-size:11px;">Prepared by Mona Digital Marketing<br>monaempoweryou@gmail.com</p>
          </td>
        </tr>
      </table>
    </td>
  </tr>

  <!-- ── BODY ── -->
  <tr>
    <td style="background:#ffffff;padding:36px 36px 32px;">

      <!-- EXECUTIVE SUMMARY -->
      <table width="100%" cellpadding="0" cellspacing="0" border="0" style="margin-bottom:32px;">
        <tr>
          <td style="background:#EBF5FB;border-left:4px solid #2E86C1;border-radius:0 6px 6px 0;padding:20px 24px;">
            <p style="margin:0 0 8px;color:#1B2D4F;font-size:13px;font-weight:700;letter-spacing:2px;text-transform:uppercase;">Executive Summary</p>
            <p style="margin:0;color:#2C3E50;font-size:14px;line-height:1.8;">
              Over the past several weeks we have been monitoring your Google Ads account closely — reviewing campaign performance data, analyzing search behavior in your target market, validating our findings, and mapping out a strategic path forward. We are now at a point where we feel confident in what we see, what it means, and what we recommend. This review captures our analysis and the roadmap we are building for the next phase of growth.
            </p>
          </td>
        </tr>
      </table>

      <!-- SECTION 1: PERFORMANCE HIGHLIGHTS -->
      <table width="100%" cellpadding="0" cellspacing="0" border="0" style="margin-bottom:28px;">
        <tr>
          <td style="padding-bottom:12px;border-bottom:2px solid #EBF5FB;">
            <p style="margin:0;color:#1B2D4F;font-size:16px;font-weight:800;">01 &nbsp;—&nbsp; What's Working</p>
          </td>
        </tr>
      </table>

      <table width="100%" cellpadding="0" cellspacing="0" border="0" style="margin-bottom:8px;">
        <tr style="vertical-align:top;">
          <td width="50%" style="padding:0 8px 16px 0;">
            <table width="100%" cellpadding="0" cellspacing="0" border="0">
              <tr>
                <td style="background:#F8FBFF;border:1px solid #D4E6F5;border-radius:8px;padding:18px 20px;">
                  <p style="margin:0 0 4px;color:#2E86C1;font-size:10px;font-weight:700;letter-spacing:2px;text-transform:uppercase;">Click-Through Rate</p>
                  <p style="margin:0 0 8px;color:#1B2D4F;font-size:20px;font-weight:800;">Above Benchmark</p>
                  <p style="margin:0;color:#5D6D7E;font-size:13px;line-height:1.6;">CTR performance is tracking above standard home services benchmarks. This tells us your ads are resonating with the right search intent — people are clicking.</p>
                </td>
              </tr>
            </table>
          </td>
          <td width="50%" style="padding:0 0 16px 8px;">
            <table width="100%" cellpadding="0" cellspacing="0" border="0">
              <tr>
                <td style="background:#F8FBFF;border:1px solid #D4E6F5;border-radius:8px;padding:18px 20px;">
                  <p style="margin:0 0 4px;color:#2E86C1;font-size:10px;font-weight:700;letter-spacing:2px;text-transform:uppercase;">Search Demand</p>
                  <p style="margin:0 0 8px;color:#1B2D4F;font-size:20px;font-weight:800;">Strong &amp; Consistent</p>
                  <p style="margin:0;color:#5D6D7E;font-size:13px;line-height:1.6;">Search volume for remodeling services in the Bay Area is healthy. The market is active and your ads are showing up in the right places at the right time.</p>
                </td>
              </tr>
            </table>
          </td>
        </tr>
        <tr style="vertical-align:top;">
          <td width="50%" style="padding:0 8px 0 0;">
            <table width="100%" cellpadding="0" cellspacing="0" border="0">
              <tr>
                <td style="background:#F8FBFF;border:1px solid #D4E6F5;border-radius:8px;padding:18px 20px;">
                  <p style="margin:0 0 4px;color:#2E86C1;font-size:10px;font-weight:700;letter-spacing:2px;text-transform:uppercase;">Campaign Foundation</p>
                  <p style="margin:0 0 8px;color:#1B2D4F;font-size:20px;font-weight:800;">Producing Signals</p>
                  <p style="margin:0;color:#5D6D7E;font-size:13px;line-height:1.6;">The existing campaigns are generating meaningful performance data. We now have enough signal to make informed, data-driven decisions rather than relying on assumptions.</p>
                </td>
              </tr>
            </table>
          </td>
          <td width="50%" style="padding:0 0 0 8px;">
            <table width="100%" cellpadding="0" cellspacing="0" border="0">
              <tr>
                <td style="background:#F8FBFF;border:1px solid #D4E6F5;border-radius:8px;padding:18px 20px;">
                  <p style="margin:0 0 4px;color:#2E86C1;font-size:10px;font-weight:700;letter-spacing:2px;text-transform:uppercase;">Cost Efficiency</p>
                  <p style="margin:0 0 8px;color:#1B2D4F;font-size:20px;font-weight:800;">Well-Positioned</p>
                  <p style="margin:0;color:#5D6D7E;font-size:13px;line-height:1.6;">Cost-per-click is holding at competitive levels for this market. We are not overpaying for visibility, which gives us room to scale intelligently.</p>
                </td>
              </tr>
            </table>
          </td>
        </tr>
      </table>

      <div style="height:28px;"></div>

      <!-- SECTION 2: OPTIMIZATION PRIORITIES -->
      <table width="100%" cellpadding="0" cellspacing="0" border="0" style="margin-bottom:28px;">
        <tr>
          <td style="padding-bottom:12px;border-bottom:2px solid #EBF5FB;">
            <p style="margin:0;color:#1B2D4F;font-size:16px;font-weight:800;">02 &nbsp;—&nbsp; What We're Improving</p>
          </td>
        </tr>
      </table>

      <p style="margin:0 0 16px;color:#5D6D7E;font-size:14px;line-height:1.7;">Every mature account has areas that can be sharpened. Below are the items we are actively addressing — not because the account is broken, but because we are building for long-term performance, not just short-term results.</p>

      <table width="100%" cellpadding="0" cellspacing="0" border="0" style="margin-bottom:28px;">
        <tr style="vertical-align:top;">
          <td style="width:20px;padding:10px 12px 10px 0;">
            <div style="width:20px;height:20px;background:#2E86C1;border-radius:50%;text-align:center;line-height:20px;color:#fff;font-size:11px;font-weight:700;">1</div>
          </td>
          <td style="padding:8px 0;border-bottom:1px solid #EBF5FB;">
            <p style="margin:0 0 4px;color:#1B2D4F;font-size:14px;font-weight:700;">Conversion Tracking Refinement</p>
            <p style="margin:0;color:#5D6D7E;font-size:13px;line-height:1.7;">We are tightening up how conversions are measured so we can connect ad activity directly to lead outcomes. This is foundational — without clean conversion data, optimization decisions are made in the dark.</p>
          </td>
        </tr>
        <tr style="vertical-align:top;">
          <td style="width:20px;padding:10px 12px 10px 0;">
            <div style="width:20px;height:20px;background:#2E86C1;border-radius:50%;text-align:center;line-height:20px;color:#fff;font-size:11px;font-weight:700;">2</div>
          </td>
          <td style="padding:8px 0;border-bottom:1px solid #EBF5FB;">
            <p style="margin:0 0 4px;color:#1B2D4F;font-size:14px;font-weight:700;">Campaign Structure Expansion</p>
            <p style="margin:0;color:#5D6D7E;font-size:13px;line-height:1.7;">The existing structure does not yet reflect the full scope of Renova's service offerings. We are building dedicated campaigns for each core service category, which improves relevance, quality scores, and lead matching.</p>
          </td>
        </tr>
        <tr style="vertical-align:top;">
          <td style="width:20px;padding:10px 12px 10px 0;">
            <div style="width:20px;height:20px;background:#2E86C1;border-radius:50%;text-align:center;line-height:20px;color:#fff;font-size:11px;font-weight:700;">3</div>
          </td>
          <td style="padding:8px 0;border-bottom:1px solid #EBF5FB;">
            <p style="margin:0 0 4px;color:#1B2D4F;font-size:14px;font-weight:700;">Lead Attribution Visibility</p>
            <p style="margin:0;color:#5D6D7E;font-size:13px;line-height:1.7;">Right now, we can tell when clicks happen — but we want to see the full path from click to contact to booked job. We are implementing attribution improvements so you will have a clear picture of which campaigns are generating actual business.</p>
          </td>
        </tr>
        <tr style="vertical-align:top;">
          <td style="width:20px;padding:10px 12px 10px 0;">
            <div style="width:20px;height:20px;background:#2E86C1;border-radius:50%;text-align:center;line-height:20px;color:#fff;font-size:11px;font-weight:700;">4</div>
          </td>
          <td style="padding:8px 0;">
            <p style="margin:0 0 4px;color:#1B2D4F;font-size:14px;font-weight:700;">Call Tracking Implementation</p>
            <p style="margin:0;color:#5D6D7E;font-size:13px;line-height:1.7;">In home services, phone calls often drive more revenue than form submissions. Call tracking is on our roadmap — it will give us visibility into which ads are driving calls, call duration, and call quality, so we can optimize for the leads that actually convert.</p>
          </td>
        </tr>
      </table>

      <!-- SECTION 3: GROWTH ROADMAP -->
      <table width="100%" cellpadding="0" cellspacing="0" border="0" style="margin-bottom:28px;">
        <tr>
          <td style="padding-bottom:12px;border-bottom:2px solid #EBF5FB;">
            <p style="margin:0;color:#1B2D4F;font-size:16px;font-weight:800;">03 &nbsp;—&nbsp; Growth Roadmap</p>
          </td>
        </tr>
      </table>

      <p style="margin:0 0 20px;color:#5D6D7E;font-size:14px;line-height:1.7;">Based on our analysis of Renova's service mix and the Bay Area remodeling market, we have identified a clear set of campaign expansions that will improve coverage, capture additional demand, and position Renova ahead of competitors who are not advertising at this level of precision.</p>

      <table width="100%" cellpadding="0" cellspacing="0" border="0" style="margin-bottom:24px;">
        <tr>
          <td style="background:#1B2D4F;border-radius:8px 8px 0 0;padding:12px 20px;">
            <p style="margin:0;color:#fff;font-size:12px;font-weight:700;letter-spacing:2px;text-transform:uppercase;">Service-Specific Campaign Expansion</p>
          </td>
        </tr>
        <tr>
          <td style="border:1px solid #D4E6F5;border-top:0;border-radius:0 0 8px 8px;padding:0;">
            <table width="100%" cellpadding="0" cellspacing="0" border="0">
              <tr style="background:#F8FBFF;">
                <td style="padding:12px 20px;border-bottom:1px solid #EBF5FB;color:#1B2D4F;font-size:13px;font-weight:600;">&#9679;&nbsp; Kitchen Remodeling</td>
                <td style="padding:12px 20px;border-bottom:1px solid #EBF5FB;color:#5D6D7E;font-size:13px;">High-intent, high-value. Dedicated campaign captures buyers actively researching kitchen upgrades.</td>
              </tr>
              <tr>
                <td style="padding:12px 20px;border-bottom:1px solid #EBF5FB;color:#1B2D4F;font-size:13px;font-weight:600;">&#9679;&nbsp; Bathroom Remodeling</td>
                <td style="padding:12px 20px;border-bottom:1px solid #EBF5FB;color:#5D6D7E;font-size:13px;">Strong search volume. Separate campaign prevents budget dilution with kitchen terms.</td>
              </tr>
              <tr style="background:#F8FBFF;">
                <td style="padding:12px 20px;border-bottom:1px solid #EBF5FB;color:#1B2D4F;font-size:13px;font-weight:600;">&#9679;&nbsp; ADU Construction</td>
                <td style="padding:12px 20px;border-bottom:1px solid #EBF5FB;color:#5D6D7E;font-size:13px;">ADU demand in Bay Area is surging. This vertical alone can generate significant qualified pipeline.</td>
              </tr>
              <tr>
                <td style="padding:12px 20px;border-bottom:1px solid #EBF5FB;color:#1B2D4F;font-size:13px;font-weight:600;">&#9679;&nbsp; Garage Conversions</td>
                <td style="padding:12px 20px;border-bottom:1px solid #EBF5FB;color:#5D6D7E;font-size:13px;">Related to ADU but distinct enough in intent to warrant its own ad group and landing strategy.</td>
              </tr>
              <tr style="background:#F8FBFF;">
                <td style="padding:12px 20px;border-bottom:1px solid #EBF5FB;color:#1B2D4F;font-size:13px;font-weight:600;">&#9679;&nbsp; Luxury Remodeling</td>
                <td style="padding:12px 20px;border-bottom:1px solid #EBF5FB;color:#5D6D7E;font-size:13px;">Targets high-net-worth Bay Area homeowners. Higher CPC but significantly higher project value.</td>
              </tr>
              <tr>
                <td style="padding:12px 20px;color:#1B2D4F;font-size:13px;font-weight:600;">&#9679;&nbsp; Brand Protection</td>
                <td style="padding:12px 20px;color:#5D6D7E;font-size:13px;">Ensures competitors cannot capture prospects searching specifically for Renova Builders.</td>
              </tr>
            </table>
          </td>
        </tr>
      </table>

      <!-- SECTION 4: BUDGET RECOMMENDATION -->
      <table width="100%" cellpadding="0" cellspacing="0" border="0" style="margin-bottom:28px;">
        <tr>
          <td style="padding-bottom:12px;border-bottom:2px solid #EBF5FB;">
            <p style="margin:0;color:#1B2D4F;font-size:16px;font-weight:800;">04 &nbsp;—&nbsp; Budget Strategy &amp; Expansion Recommendation</p>
          </td>
        </tr>
      </table>

      <table width="100%" cellpadding="0" cellspacing="0" border="0" style="margin-bottom:20px;">
        <tr>
          <td style="background:#FEF9EE;border:1px solid #F4D03F;border-radius:8px;padding:20px 24px;">
            <p style="margin:0 0 8px;color:#7D6608;font-size:12px;font-weight:700;letter-spacing:2px;text-transform:uppercase;">Strategic Recommendation</p>
            <p style="margin:0;color:#2C3E50;font-size:14px;line-height:1.8;">We have identified an opportunity to deploy an additional <strong>~$2,000/month</strong> in advertising investment that would meaningfully expand campaign coverage and accelerate lead generation. However, we are recommending a measured approach — not an immediate increase.</p>
          </td>
        </tr>
      </table>

      <p style="margin:0 0 16px;color:#5D6D7E;font-size:14px;line-height:1.7;">Our philosophy on budget expansion is straightforward: <strong>more money should only move when the infrastructure is ready to use it well</strong>. Deploying additional budget before conversion tracking is clean, campaign structure is complete, and attribution is measurable would mean spending more money with less visibility into what it produces.</p>

      <table width="100%" cellpadding="0" cellspacing="0" border="0" style="margin-bottom:24px;">
        <tr>
          <td style="background:#1B2D4F;border-radius:8px 8px 0 0;padding:12px 20px;">
            <p style="margin:0;color:#fff;font-size:12px;font-weight:700;letter-spacing:2px;text-transform:uppercase;">Recommended Timeline — Next Two Weeks</p>
          </td>
        </tr>
        <tr>
          <td style="border:1px solid #D4E6F5;border-top:0;border-radius:0 0 8px 8px;">
            <table width="100%" cellpadding="0" cellspacing="0" border="0">
              <tr style="background:#F8FBFF;">
                <td style="padding:12px 20px;border-bottom:1px solid #EBF5FB;width:130px;">
                  <p style="margin:0;color:#2E86C1;font-size:12px;font-weight:700;">Week 1</p>
                </td>
                <td style="padding:12px 20px;border-bottom:1px solid #EBF5FB;color:#5D6D7E;font-size:13px;line-height:1.6;">Finalize conversion tracking setup. Complete service-specific campaign builds. Validate data accuracy.</td>
              </tr>
              <tr>
                <td style="padding:12px 20px;border-bottom:1px solid #EBF5FB;">
                  <p style="margin:0;color:#2E86C1;font-size:12px;font-weight:700;">Week 2</p>
                </td>
                <td style="padding:12px 20px;border-bottom:1px solid #EBF5FB;color:#5D6D7E;font-size:13px;line-height:1.6;">Monitor performance with new structure. Confirm tracking is capturing lead activity correctly. Assess readiness for budget scale.</td>
              </tr>
              <tr style="background:#F8FBFF;">
                <td style="padding:12px 20px;">
                  <p style="margin:0;color:#27AE60;font-size:12px;font-weight:700;">Week 3+</p>
                </td>
                <td style="padding:12px 20px;color:#5D6D7E;font-size:13px;line-height:1.6;">Deploy the additional ~$2,000/month investment with precision — allocated by service category, validated by data, and set up to scale with confidence.</td>
              </tr>
            </table>
          </td>
        </tr>
      </table>

      <table width="100%" cellpadding="0" cellspacing="0" border="0" style="margin-bottom:32px;">
        <tr>
          <td style="background:#EBF5FB;border-left:4px solid #27AE60;border-radius:0 6px 6px 0;padding:18px 24px;">
            <p style="margin:0;color:#1B2D4F;font-size:14px;line-height:1.8;"><strong>The goal is not to spend more.</strong> The goal is to spend more <em>correctly</em> — at the right time, in the right campaigns, with the right tracking in place to tell us what's working and what isn't. That discipline is how we protect your investment and build campaigns that scale.</p>
          </td>
        </tr>
      </table>

      <!-- SECTION 5: NEXT STEPS -->
      <table width="100%" cellpadding="0" cellspacing="0" border="0" style="margin-bottom:28px;">
        <tr>
          <td style="padding-bottom:12px;border-bottom:2px solid #EBF5FB;">
            <p style="margin:0;color:#1B2D4F;font-size:16px;font-weight:800;">05 &nbsp;—&nbsp; Immediate Next Steps</p>
          </td>
        </tr>
      </table>

      <table width="100%" cellpadding="0" cellspacing="0" border="0" style="margin-bottom:28px;">
        <tr style="vertical-align:top;">
          <td style="width:28px;padding:8px 12px 8px 0;vertical-align:top;">
            <div style="width:24px;height:24px;background:#2E86C1;border-radius:50%;text-align:center;line-height:24px;color:#fff;font-size:11px;font-weight:700;">&#10003;</div>
          </td>
          <td style="padding:8px 0;color:#2C3E50;font-size:14px;line-height:1.7;border-bottom:1px solid #EBF5FB;">Finalize conversion tracking across all campaigns and confirm lead measurement is accurate</td>
        </tr>
        <tr style="vertical-align:top;">
          <td style="width:28px;padding:8px 12px 8px 0;vertical-align:top;">
            <div style="width:24px;height:24px;background:#2E86C1;border-radius:50%;text-align:center;line-height:24px;color:#fff;font-size:11px;font-weight:700;">&#10003;</div>
          </td>
          <td style="padding:8px 0;color:#2C3E50;font-size:14px;line-height:1.7;border-bottom:1px solid #EBF5FB;">Build out service-specific campaigns (Kitchen, Bathroom, ADU, Garage, Luxury, Brand Protection)</td>
        </tr>
        <tr style="vertical-align:top;">
          <td style="width:28px;padding:8px 12px 8px 0;vertical-align:top;">
            <div style="width:24px;height:24px;background:#2E86C1;border-radius:50%;text-align:center;line-height:24px;color:#fff;font-size:11px;font-weight:700;">&#10003;</div>
          </td>
          <td style="padding:8px 0;color:#2C3E50;font-size:14px;line-height:1.7;border-bottom:1px solid #EBF5FB;">Review and improve landing page alignment for each service category</td>
        </tr>
        <tr style="vertical-align:top;">
          <td style="width:28px;padding:8px 12px 8px 0;vertical-align:top;">
            <div style="width:24px;height:24px;background:#2E86C1;border-radius:50%;text-align:center;line-height:24px;color:#fff;font-size:11px;font-weight:700;">&#10003;</div>
          </td>
          <td style="padding:8px 0;color:#2C3E50;font-size:14px;line-height:1.7;border-bottom:1px solid #EBF5FB;">Plan and initiate call tracking implementation</td>
        </tr>
        <tr style="vertical-align:top;">
          <td style="width:28px;padding:8px 12px 8px 0;vertical-align:top;">
            <div style="width:24px;height:24px;background:#27AE60;border-radius:50%;text-align:center;line-height:24px;color:#fff;font-size:11px;font-weight:700;">&#10003;</div>
          </td>
          <td style="padding:8px 0;color:#2C3E50;font-size:14px;line-height:1.7;">Schedule a strategy call to review findings, confirm budget expansion timeline, and align on next phase priorities</td>
        </tr>
      </table>

      <!-- CTA -->
      <table width="100%" cellpadding="0" cellspacing="0" border="0" style="margin-bottom:8px;">
        <tr>
          <td style="background:linear-gradient(135deg,#1B2D4F,#2E86C1);border-radius:8px;padding:24px;text-align:center;">
            <p style="margin:0 0 6px;color:rgba(255,255,255,0.7);font-size:12px;letter-spacing:2px;text-transform:uppercase;">Ready to discuss?</p>
            <p style="margin:0 0 16px;color:#ffffff;font-size:18px;font-weight:700;">Schedule Your Strategy Call</p>
            <p style="margin:0;color:rgba(255,255,255,0.75);font-size:13px;line-height:1.7;">Reply to this email or reach us directly at monaempoweryou@gmail.com<br>We'll walk through findings, answer questions, and map out the next 30 days.</p>
          </td>
        </tr>
      </table>

    </td>
  </tr>

  <!-- ── MONA FOOTER ── -->
  <tr>
    <td style="background:#1B2D4F;padding:24px 36px;">
      <table width="100%" cellpadding="0" cellspacing="0" border="0">
        <tr>
          <td>
            <p style="margin:0 0 2px;color:#ffffff;font-size:13px;font-weight:700;">Mona Digital Marketing</p>
            <p style="margin:0;color:rgba(255,255,255,0.5);font-size:12px;line-height:1.6;">Los Angeles, CA &nbsp;·&nbsp; monaempoweryou@gmail.com</p>
          </td>
          <td style="text-align:right;">
            <p style="margin:0;color:#2E86C1;font-size:11px;font-weight:700;letter-spacing:1px;">SEO · Google Ads · Meta Ads</p>
            <p style="margin:2px 0 0;color:rgba(255,255,255,0.35);font-size:10px;">Social Media · Web Design · AI Content</p>
          </td>
        </tr>
        <tr>
          <td colspan="2" style="padding-top:16px;border-top:1px solid rgba(255,255,255,0.1);">
            <p style="margin:0;color:rgba(255,255,255,0.25);font-size:10px;text-align:center;">This report is prepared by Mona Digital Marketing exclusively for Renova Builders. Confidential.</p>
          </td>
        </tr>
      </table>
    </td>
  </tr>

</table>
</td></tr>
</table>

</body>
</html>"""

# ─── Routes ────────────────────────────────────────────────────────────────────

@app.route("/", methods=["GET"])
def index():
    return send_file("chat-widget.html")

@app.route("/platinum-pool", methods=["GET"])
def platinum_pool():
    return send_file("platinum-pool.html")

@app.route("/health", methods=["GET"])
def health():
    return {"status": "ok", "agent": "Mona"}

def _check_token(data: dict) -> bool:
    expected = os.environ.get("SEND_TOKEN", "platinum2024")
    return data.get("token", "") == expected

@app.route("/send-queued", methods=["POST"])
def send_queued():
    """Generic endpoint: accepts any queued email payload and sends via Render SMTP.
    Body: {"token":"...","subject":"...","to":"...","html":"..."}
    This is the permanent default send method — uses Render's existing GMAIL credentials.
    """
    data = request.get_json() or {}
    if not _check_token(data):
        return {"error": "Unauthorized"}, 401
    subject = data.get("subject", "").strip()
    to      = data.get("to", "").strip()
    html    = data.get("html", "").strip()
    if not subject or not to or not html:
        return {"error": "subject, to, and html are required"}, 400

    smtp_user = os.environ.get("GMAIL_USER", "monaempoweryou@gmail.com")
    smtp_pass = os.environ.get("GMAIL_APP_PASSWORD")
    if not smtp_pass:
        return {"status": "failed", "message": "GMAIL_APP_PASSWORD not set on Render"}, 500

    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"]    = smtp_user
    msg["To"]      = to
    msg.attach(MIMEText(html, "html"))
    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, timeout=15) as s:
            s.login(smtp_user, smtp_pass)
            s.sendmail(smtp_user, to, msg.as_string())
        return {"status": "sent", "message": f"Email sent to {to}"}
    except Exception as e:
        print(f"send-queued error: {e}")
        return {"status": "failed", "message": str(e)}, 500

@app.route("/send-platinum-outreach", methods=["POST"])
def send_platinum_outreach():
    """Send UNVEILED outreach email for Platinum Pool."""
    data = request.get_json() or {}
    if not _check_token(data):
        return {"error": "Unauthorized"}, 401
    subject = "We built something for Platinum Pool & Property Services"
    body = platinum_pool_unveiled_html()
    sent = send_to_email(subject, body)
    if sent:
        return {"status": "sent", "message": "UNVEILED outreach sent to monaempoweryou@gmail.com"}
    return {"status": "failed", "message": "SMTP failed — check GMAIL_APP_PASSWORD"}, 500

@app.route("/send-renova-update", methods=["POST"])
def send_renova_update():
    """Send MONA-branded Renova strategic update email via SMTP."""
    data = request.get_json() or {}
    if not _check_token(data):
        return {"error": "Unauthorized"}, 401
    subject = "[Renova Builders] Strategic Account Review — June 2026"
    body = renova_strategic_update_html()
    sent = send_to_email(subject, body)
    if sent:
        return {"status": "sent", "message": "Renova update sent to monaempoweryou@gmail.com"}
    return {"status": "failed", "message": "SMTP failed — check GMAIL_APP_PASSWORD"}, 500

@app.route("/send-goldsmith-outreach", methods=["POST"])
def send_goldsmith_outreach():
    """Send UNVEILED outreach email for Goldsmith Financial."""
    data = request.get_json() or {}
    if not _check_token(data):
        return {"error": "Unauthorized"}, 401
    website_url = data.get("website_url", "")
    if not website_url:
        return {"error": "website_url required"}, 400
    subject = "We built something for Goldsmith Financial"
    body = goldsmith_unveiled_html(website_url)
    sent = send_to_email(subject, body)
    if sent:
        return {"status": "sent", "message": "UNVEILED outreach sent to monaempoweryou@gmail.com"}
    return {"status": "failed", "message": "SMTP failed — check GMAIL_APP_PASSWORD"}, 500

@app.route("/send-platinum-proposal", methods=["POST"])
def send_platinum_proposal():
    """Send Platinum Pool branded proposal email via SMTP."""
    data = request.get_json() or {}
    token = data.get("token", "")
    expected = os.environ.get("SEND_TOKEN", "platinum2024")
    if token != expected:
        return {"error": "Unauthorized"}, 401

    subject = "Your Website Is Live — Platinum Pool & Property Services LLC"
    body = platinum_pool_proposal_html()
    sent = send_to_email(subject, body)

    if sent:
        return {"status": "sent", "message": "Proposal email sent to monaempoweryou@gmail.com"}
    else:
        return {"status": "failed", "message": "SMTP send failed — check GMAIL_APP_PASSWORD env var"}, 500

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    if not data:
        return {"error": "No data"}, 400

    message = data.get("message", "").strip()
    history = data.get("history", [])

    if not message:
        return {"error": "No message"}, 400

    messages = []
    for h in history:
        if h.get("role") in ("user", "assistant") and h.get("content"):
            messages.append({"role": h["role"], "content": h["content"]})
    messages.append({"role": "user", "content": message})

    # Check if this is a production request — if so, trigger COO pipeline
    production = is_production_request(message)

    def generate():
        try:
            # Step 1: Mona responds to the user
            with client.messages.stream(
                model="claude-sonnet-4-6",
                max_tokens=256,
                system=MONA_PROMPT,
                messages=messages,
            ) as stream:
                for text in stream.text_stream:
                    yield f"data: {json.dumps({'text': text})}\n\n"

            # Step 2: If production request, run Agency Manager pipeline
            if production:
                try:
                    # Keep-alive ping so Render proxy doesn't close idle SSE connection
                    yield ": processing\n\n"
                    plan = run_coo(message, history)
                    yield ": sending\n\n"
                    agent = plan.get("agent", "unknown")
                    client_name = plan.get("client", "agency").title()
                    needs_approval = plan.get("needs_approval", False)

                    if needs_approval:
                        subject = f"[APPROVAL NEEDED] {agent.replace('-', ' ').title()} — {client_name}"
                        body = format_email_body(plan, approval_required=True)
                    else:
                        subject = f"[Mona] {agent.replace('-', ' ').title()} — {client_name}"
                        body = format_email_body(plan, approval_required=False)

                    sent = send_to_email(subject, body)
                    status = "✓ Sent to your inbox." if sent else "✓ Done. (Email not configured — check GMAIL_APP_PASSWORD)"
                    yield f"data: {json.dumps({'text': f' {status}'})}\n\n"
                except Exception as e:
                    print(f"Agency Manager pipeline error: {e}")
                    yield f"data: {json.dumps({'text': ' (Pipeline error — check logs)'})}\n\n"

            yield "data: [DONE]\n\n"
        except Exception as e:
            yield f"data: {json.dumps({'error': str(e)})}\n\n"
            yield "data: [DONE]\n\n"

    return Response(
        stream_with_context(generate()),
        mimetype="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "X-Accel-Buffering": "no",
            "Access-Control-Allow-Origin": "*",
        },
    )

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
