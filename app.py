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

# ─── Platinum Pool Proposal Email ─────────────────────────────────────────────

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
