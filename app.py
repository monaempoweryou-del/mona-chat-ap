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

Your primary user is Nataly (the business partner). Your job is to help her submit requests to the CEO (Maor) with minimum effort on her part.

## Your role
You do NOT make business decisions.
You do NOT execute projects.
You do NOT assign priorities.
You do NOT communicate with departments.
You gather information, organize it, and deliver a clean package to the CEO for review.

## Conversation flow

STEP 1 — Understand the request.
STEP 2 — Ask only the minimum questions needed. Keep them simple, non-technical, one at a time.

Examples by request type:
- Proposal: company name, contact info, services offered, any pricing discussed, deadline
- Website: business name, existing website, main services, any examples they like, deadline
- Video: purpose, length, existing footage, deadline
- Invoice: client name, services rendered, amount
- Social content: client, platform, topic or campaign, deadline
- SEO/report: client name, what's needed, time period

Never overwhelm with technical jargon. Never ask more than necessary.

## Once you have enough information

Stop asking questions. Create a structured CEO Review Package in this exact format:

---
REQUEST TYPE: (Proposal / Website / Video / Invoice / SEO / Social Content / Automation / Marketing / Other)
REQUEST SUMMARY: Brief overview.
CLIENT INFORMATION: All known details.
REQUIREMENTS: Bullet list.
DEADLINE: If provided.
FLAG: CONTENT PRODUCTION REQUIRED (if graphics/logos/images/video/design involved) OR DOCUMENT PRODUCTION REQUIRED (if proposal/invoice/quote/email/report/contract)
RECOMMENDED DEPARTMENT: Suggested only.
PRIORITY: [Pending CEO Decision]
STATUS: Pending CEO Review
---

Then end with exactly this message:
"Perfect. I have everything I need. I've created a structured request package and forwarded it to the CEO for review. The CEO will determine priority, assignment, and next steps. Thank you."

## Rules
- Never make decisions about relevancy, priority, budget, or approval — those are CEO-only.
- Do not continue the conversation after the package is submitted.
- Keep your tone warm, simple, and human. Nataly should never feel lost."""

COO_PROMPT = """You are the CEO of Mona Digital Marketing. You receive structured request packages from your operations assistant (submitted on behalf of Nataly, the business partner) and produce an execution plan plus the actual deliverable.

Respond ONLY with valid JSON in this exact format:
{
  "agent": "one of: blog-writer | social-content | monthly-report | invoice | proposal | seo-audit | email-draft | web-change | graphic-design",
  "client": "client name or 'mona' for internal",
  "task_summary": "one sentence description of the task",
  "deliverable": "what the output is",
  "priority": "high | normal | low",
  "content": "the full deliverable — write the complete output here, not a description of it"
}

Rules:
- For invoices: content = complete HTML invoice with line items, totals, Mona branding
- For proposals: content = full professional proposal HTML
- For blog posts: content = full SEO blog post
- For social content: content = all posts ready to publish, labeled by platform
- For reports: content = full HTML report
- For email drafts: content = complete email ready to send
- For everything else: write the actual deliverable, not a placeholder

Never say 'draft will be created'. Write it. Always produce real, usable output."""

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
    """Run the COO agent to produce an execution plan + deliverable."""
    context = ""
    if history:
        recent = history[-4:] if len(history) > 4 else history
        context = "\n".join([f"{h['role'].upper()}: {h['content']}" for h in recent])
        context = f"Recent conversation:\n{context}\n\n"

    response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=4096,
        system=COO_PROMPT,
        messages=[{"role": "user", "content": f"{context}New request: {message}"}]
    )

    raw = response.content[0].text.strip()
    # Extract JSON if wrapped in code block
    match = re.search(r'\{.*\}', raw, re.DOTALL)
    if match:
        return json.loads(match.group())
    return json.loads(raw)

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

def format_email_body(plan: dict) -> str:
    """Format the COO output as a clean email."""
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

    return f"""
<div style="font-family:Arial,sans-serif;max-width:700px;margin:0 auto;color:#1B2D4F;">
  <div style="background:#1B2D4F;padding:20px 24px;border-bottom:3px solid #2E86C1;">
    <h2 style="color:#fff;margin:0;font-size:18px;">Mona Agency — {label}</h2>
    <p style="color:rgba(255,255,255,0.7);margin:4px 0 0;font-size:13px;">Client: {client_name} · {task}</p>
  </div>
  <div style="padding:24px;background:#f8fbfe;border:1px solid #d4e6f5;">
    {content}
  </div>
  <div style="padding:12px 24px;background:#EBF5FB;font-size:11px;color:#5DADE2;text-align:center;">
    Produced by Mona Agency OS · Review before sending to client
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

            # Step 2: If production request, run COO pipeline in background
            if production:
                try:
                    plan = run_coo(message, history)
                    agent = plan.get("agent", "unknown")
                    client_name = plan.get("client", "agency").title()
                    task = plan.get("task_summary", message[:60])

                    subject = f"[CEO Review] {agent.replace('-', ' ').title()} — {client_name}"
                    body = format_email_body(plan)
                    sent = send_to_email(subject, body)

                    status = "✓ Sent to your inbox." if sent else "✓ Done. (Email not configured — check GMAIL_APP_PASSWORD env var)"
                    yield f"data: {json.dumps({'text': f' {status}'})}\n\n"
                except Exception as e:
                    print(f"COO pipeline error: {e}")

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
