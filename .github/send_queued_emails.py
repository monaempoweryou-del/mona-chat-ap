import os
import json
import smtplib
import glob
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from pathlib import Path

GMAIL_USER = os.environ["GMAIL_USER"]
GMAIL_PASS = os.environ["GMAIL_APP_PASSWORD"]
QUEUE_DIR = Path("email_queue")


def send(subject: str, to: str, html: str) -> bool:
    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = GMAIL_USER
    msg["To"] = to
    msg.attach(MIMEText(html, "html"))
    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, timeout=30) as s:
            s.login(GMAIL_USER, GMAIL_PASS)
            s.sendmail(GMAIL_USER, to, msg.as_string())
        return True
    except Exception as e:
        print(f"SMTP error: {e}")
        return False


def main():
    pending = sorted(QUEUE_DIR.glob("*.json"))
    if not pending:
        print("No pending emails.")
        return

    for path in pending:
        if path.name.startswith("sent_"):
            continue
        data = json.loads(path.read_text())
        subject = data["subject"]
        to = data.get("to", GMAIL_USER)
        html = data["html"]

        print(f"Sending: {subject} → {to}")
        ok = send(subject, to, html)

        if ok:
            print(f"  ✓ Sent")
            sent_path = path.parent / f"sent_{path.name}"
            path.rename(sent_path)
        else:
            print(f"  ✗ Failed: {path.name}")
            raise SystemExit(1)


if __name__ == "__main__":
    main()
