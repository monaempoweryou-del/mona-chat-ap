"""
Mona Agency OS — Email Queue Processor

Queue file format (email_queue/pending/[id].json):
{
  "id": "unique-name",
  "brand": "unveiled" | "mona",
  "subject": "Email subject",
  "stage": "test" | "send",
  "to_test": "monaempoweryou@gmail.com",
  "to_customer": "customer@example.com",
  "html": "<full HTML email body>"
}

stage=test  → sends to to_test  (for approval review)
stage=send  → sends to to_customer (actual delivery)

On success: moved to email_queue/sent/[id].json  + "sent_to" field added
On failure: moved to email_queue/failed/[id].json + "error" field added
"""

import os
import json
import smtplib
import sys
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from pathlib import Path
from datetime import datetime, timezone

GMAIL_USER = os.environ.get("GMAIL_USER", "")
GMAIL_PASS = os.environ.get("GMAIL_APP_PASSWORD", "")
PENDING_DIR = Path("email_queue/pending")
SENT_DIR    = Path("email_queue/sent")
FAILED_DIR  = Path("email_queue/failed")

PENDING_DIR.mkdir(parents=True, exist_ok=True)
SENT_DIR.mkdir(parents=True, exist_ok=True)
FAILED_DIR.mkdir(parents=True, exist_ok=True)


def smtp_send(subject: str, to: str, html: str) -> tuple[bool, str]:
    if not GMAIL_USER or not GMAIL_PASS:
        return False, "GMAIL_USER or GMAIL_APP_PASSWORD secret is not set in GitHub repository secrets"
    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"]    = GMAIL_USER
    msg["To"]      = to
    msg.attach(MIMEText(html, "html"))
    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, timeout=30) as s:
            s.login(GMAIL_USER, GMAIL_PASS)
            s.sendmail(GMAIL_USER, to, msg.as_string())
        return True, ""
    except Exception as e:
        return False, str(e)


def write_summary(lines: list[str]):
    summary_path = os.environ.get("GITHUB_STEP_SUMMARY", "")
    if summary_path:
        with open(summary_path, "a") as f:
            f.write("\n".join(lines) + "\n")


def main():
    pending = sorted(PENDING_DIR.glob("*.json"))
    if not pending:
        print("No pending emails.")
        write_summary(["## Email Queue", "No pending emails found."])
        return

    summary_lines = ["## Email Queue Results", ""]
    all_ok = True
    timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    for path in pending:
        data = json.loads(path.read_text())
        email_id = data.get("id", path.stem)
        stage    = data.get("stage", "test")
        subject  = data["subject"]
        brand    = data.get("brand", "unknown").upper()

        if stage == "send":
            recipient = data.get("to_customer", "")
            stage_label = "CUSTOMER DELIVERY"
        else:
            recipient = data.get("to_test", "monaempoweryou@gmail.com")
            stage_label = "TEST / APPROVAL"

        print(f"\n[{brand}] {stage_label}: {subject}")
        print(f"  → {recipient}")

        ok, error = smtp_send(subject, recipient, data["html"])

        data["processed_at"] = timestamp
        if ok:
            data["sent_to"] = recipient
            dest = SENT_DIR / path.name
            path.rename(dest)
            dest.write_text(json.dumps(data, indent=2))
            print(f"  ✓ SENT")
            summary_lines.append(f"| ✅ `{email_id}` | `{stage_label}` | `{recipient}` | Sent |")
        else:
            data["error"] = error
            dest = FAILED_DIR / path.name
            path.rename(dest)
            dest.write_text(json.dumps(data, indent=2))
            print(f"  ✗ FAILED: {error}")
            summary_lines.append(f"| ❌ `{email_id}` | `{stage_label}` | `{recipient}` | {error} |")
            all_ok = False

    header = ["| Email | Stage | Recipient | Status |", "|-------|-------|-----------|--------|"]
    write_summary(summary_lines[:2] + header + summary_lines[2:])

    if not all_ok:
        print("\nOne or more emails failed. Check email_queue/failed/ to retry.")
        sys.exit(1)
    else:
        print("\nAll emails sent successfully.")


if __name__ == "__main__":
    main()
