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
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
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

# ─── Routes ────────────────────────────────────────────────────────────────────

@app.route("/", methods=["GET"])
def index():
    return send_file("chat-widget.html")

@app.route("/health", methods=["GET"])
def health():
    return {"status": "ok", "agent": "Mona"}

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
                    plan = run_coo(message, history)
                    agent = plan.get("agent", "unknown")
                    client_name = plan.get("client", "agency").title()
                    needs_approval = plan.get("needs_approval", False)

                    if needs_approval:
                        # Content production — flag for Maor, don't auto-execute
                        subject = f"[APPROVAL NEEDED] {agent.replace('-', ' ').title()} — {client_name}"
                        body = format_email_body(plan, approval_required=True)
                    else:
                        # Text-based — execute immediately
                        subject = f"[Mona] {agent.replace('-', ' ').title()} — {client_name}"
                        body = format_email_body(plan, approval_required=False)

                    sent = send_to_email(subject, body)
                    status = "✓ Sent to your inbox." if sent else "✓ Done. (Email not configured — check GMAIL_APP_PASSWORD)"
                    yield f"data: {json.dumps({'text': f' {status}'})}\n\n"
                except Exception as e:
                    print(f"Agency Manager pipeline error: {e}")

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
