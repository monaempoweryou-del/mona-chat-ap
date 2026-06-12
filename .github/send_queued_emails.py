"""
Mona Agency OS — Email Queue Processor

SENDER ARCHITECTURE (permanent):
  Outbound sender:  nataly@monadigitalmarketing.com  (GitHub secret: SMTP_USER)
  Approval inbox:   monaempoweryou@gmail.com          (all test emails)
  Customer delivery: to_customer field in queue file

GitHub Secrets required:
  SMTP_USER     = nataly@monadigitalmarketing.com
  SMTP_PASSWORD = App Password for nataly@monadigitalmarketing.com

Queue file format (email_queue/pending/[id].json):
{
  "id":          "descriptive-kebab-case-name",
  "brand":       "mona | unveiled",
  "subject":     "Email subject",
  "stage":       "test | send",
  "to_test":     "monaempoweryou@gmail.com",
  "to_customer": "customer@email.com",
  "html":        "<full HTML>"
}

stage=test → sends to to_test  (approval review)
stage=send → sends to to_customer (customer delivery)

On success: moved to email_queue/sent/    (sent_to field added)
On failure: moved to email_queue/failed/  (error field added, retryable)
"""

import os
import json
import smtplib
import sys
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from pathlib import Path
from datetime import datetime, timezone

SMTP_USER = os.environ.get("SMTP_USER", "")
SMTP_PASS = os.environ.get("SMTP_PASSWORD", "")
PENDING   = Path("email_queue/pending")
SENT      = Path("email_queue/sent")
FAILED    = Path("email_queue/failed")

for d in (PENDING, SENT, FAILED):
    d.mkdir(parents=True, exist_ok=True)


def smtp_send(subject: str, to: str, html: str) -> tuple[bool, str]:
    if not SMTP_USER or not SMTP_PASS:
        return False, (
            "SMTP_USER or SMTP_PASSWORD secret is missing. "
            "Add them at: github.com/monaempoweryou-del/mona-chat-ap/settings/secrets/actions"
        )
    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"]    = f"Mona Digital Marketing <{SMTP_USER}>"
    msg["To"]      = to
    msg.attach(MIMEText(html, "html"))
    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, timeout=30) as s:
            s.login(SMTP_USER, SMTP_PASS)
            s.sendmail(SMTP_USER, to, msg.as_string())
        return True, ""
    except Exception as e:
        return False, str(e)


def write_summary(lines: list[str]):
    path = os.environ.get("GITHUB_STEP_SUMMARY", "")
    if path:
        with open(path, "a") as f:
            f.write("\n".join(lines) + "\n")


def main():
    pending = sorted(PENDING.glob("*.json"))
    if not pending:
        print("No pending emails in queue.")
        write_summary(["## Email Queue", "_No pending emails._"])
        return

    summary  = ["## Email Queue Results", "",
                "| Email | Brand | Stage | Recipient | Status |",
                "|-------|-------|-------|-----------|--------|"]
    all_ok   = True
    ts       = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    for path in pending:
        data     = json.loads(path.read_text())
        email_id = data.get("id", path.stem)
        brand    = data.get("brand", "?").upper()
        stage    = data.get("stage", "test")
        subject  = data["subject"]

        if stage == "send":
            recipient   = data.get("to_customer", "")
            stage_label = "CUSTOMER"
        else:
            recipient   = data.get("to_test", "monaempoweryou@gmail.com")
            stage_label = "TEST/APPROVAL"

        print(f"\n[{brand}] {stage_label}: {subject}")
        print(f"  From: {SMTP_USER or '(not set)'}")
        print(f"  To:   {recipient}")

        ok, error = smtp_send(subject, recipient, data["html"])
        data["processed_at"] = ts

        if ok:
            data["sent_to"] = recipient
            dest = SENT / path.name
            path.rename(dest)
            dest.write_text(json.dumps(data, indent=2))
            print(f"  ✓ SENT")
            summary.append(f"| `{email_id}` | {brand} | {stage_label} | `{recipient}` | ✅ Sent |")
        else:
            data["error"] = error
            dest = FAILED / path.name
            path.rename(dest)
            dest.write_text(json.dumps(data, indent=2))
            print(f"  ✗ FAILED: {error}")
            summary.append(f"| `{email_id}` | {brand} | {stage_label} | `{recipient}` | ❌ {error} |")
            all_ok = False

    write_summary(summary)

    if not all_ok:
        print("\nSome emails failed. Check email_queue/failed/ to diagnose and retry.")
        sys.exit(1)

    print(f"\nAll emails sent. From: {SMTP_USER}")


if __name__ == "__main__":
    main()
