# MONA Chat Infrastructure — Root Cause Report
**Date:** June 3, 2026
**Branch:** `claude/monet-ai-power-studio-scope-3wmwA`

---

## System Overview

The MONA Chat app (`app.py`) is a Flask SSE application deployed on Render. Nataly uses it via `chat-widget.html`. The system routes her requests through two AI layers:

1. **Mona (intake)** — Claude Sonnet, max 256 tokens, collects request info
2. **Agency Manager (COO)** — Claude Haiku, generates the actual deliverable as HTML
3. **Email delivery** — Gmail SMTP (port 465, SSL) using `GMAIL_APP_PASSWORD`

---

## Root Cause Analysis

### Bug 1 — GMAIL_APP_PASSWORD Not Set (Primary Failure)
**File:** `app.py` line 146
**Status:** ⚠️ Unresolved — requires PMA

```python
smtp_pass = os.environ.get("GMAIL_APP_PASSWORD")
if not smtp_pass:
    return False  # was: silently failed with no detail
```

**Root cause:** The `GMAIL_APP_PASSWORD` environment variable is not configured in Render. Every email send attempt silently returns `False`. Nataly sees no error — she believes her request succeeded.

**Fix required (PMA-012):** Maor must:
1. Enable 2FA on Gmail (if not already): myaccount.google.com/security
2. Generate an App Password: myaccount.google.com/apppasswords → Select app: Mail → Select device: Other → name it "MONA Chat Render" → copy the 16-character password
3. In Render Dashboard → mona-chat-ap → Environment → Add env var:
   - Key: `GMAIL_APP_PASSWORD`
   - Value: the 16-character App Password (no spaces)
4. Trigger a Render redeploy (automatic after env var save)

**Important:** The App Password is NOT your Gmail account password. It is a separate 16-character token generated specifically for app access.

---

### Bug 2 — Misleading Success Signal on Failure (Fixed)
**File:** `app.py` line 268–269 (original)
**Status:** ✅ Fixed in this session

**Before:**
```python
status = "✓ Sent to your inbox." if sent else "✓ Done. (Email not configured — check GMAIL_APP_PASSWORD)"
```

Both outcomes showed "✓" — Nataly could not distinguish a sent email from a failed one.

**After:**
```python
if sent:
    status = "✓ Delivered to your inbox."
else:
    status = f"⚠️ Email not sent — {send_err}"
```

Now failure shows ⚠️ with the specific reason (missing env var, auth failure, SMTP error).

---

### Bug 3 — No Error Detail on Authentication Failure (Fixed)
**File:** `app.py` `send_to_email()` function
**Status:** ✅ Fixed in this session

**Before:** All SMTP errors caught as generic `Exception`, logged to server console only, returned bare `False`.

**After:** Three distinct exception handlers:
- `SMTPAuthenticationError` → specific message about App Password vs. account password
- `SMTPException` → SMTP-level error with detail
- `Exception` → catch-all with error type and message

All errors now: (1) logged to console with detail, (2) returned as string to the caller, (3) surfaced to Nataly via the ⚠️ status message.

---

### Bug 4 — No Draft Preservation on Send Failure (Fixed)
**File:** `app.py` pipeline section
**Status:** ✅ Fixed in this session

**Before:** If email failed, the generated deliverable content was lost with no record.

**After:** On send failure, the full HTML deliverable is written to `/tmp/mona_draft_<timestamp>.html` on the Render server, and the path is logged:
```
Draft preserved to /tmp/mona_draft_20260603_214315.html
```

**Limitation:** `/tmp` on Render is ephemeral — files do not persist across deploys or instance restarts. This is a fallback for debugging, not permanent storage. True draft preservation would require writing to a persistent store (S3, Supabase, or Gmail drafts via API).

---

### Bug 5 — Pipeline Error Swallowed (Fixed)
**File:** `app.py` line 272 (original)
**Status:** ✅ Fixed in this session

**Before:**
```python
yield f"data: {json.dumps({'text': ' (Pipeline error — check logs)'})}\n\n"
```

**After:**
```python
yield f"data: {json.dumps({'text': f' ⚠️ Pipeline error: {type(e).__name__} — check server logs'})}\n\n"
```

Nataly now sees the error type. Maor sees the full traceback in Render logs.

---

## Fix Summary

| # | Bug | Status | Requires |
|---|-----|--------|---------|
| 1 | GMAIL_APP_PASSWORD not configured | ⚠️ Open | PMA-012: Maor sets in Render |
| 2 | "✓ Done" shown on email failure | ✅ Fixed | — |
| 3 | No error detail on SMTP auth failure | ✅ Fixed | — |
| 4 | Generated content lost on send failure | ✅ Fixed (partial — /tmp only) | Supabase/persistent store for full fix |
| 5 | Pipeline error type hidden from user | ✅ Fixed | — |

---

## Gmail Attachment Limitation

**Finding:** The Gmail MCP (`d1d24a0c`) does not support creating drafts with attachments. The tool description explicitly states: *"Creating drafts with attachments is not supported yet."*

**Impact on Renova email:** The 4 PDF reports cannot be programmatically attached to the Gmail draft. They must be manually attached by Maor from `MONA Deliverables/Clients/Renova Builders/` before sending.

**Future workaround options:**
1. Upload PDFs to Google Drive → insert Drive links into email body
2. Use a different Gmail API method (requires custom OAuth integration, not MCP)
3. Use SendGrid or Mailgun API (supports attachments natively, free tiers available)

---

## Pending Maor Actions

| PMA | Task | Steps |
|-----|------|-------|
| PMA-012 | Set GMAIL_APP_PASSWORD on Render | 1. myaccount.google.com/apppasswords → generate App Password → 2. Render Dashboard → Environment → Add `GMAIL_APP_PASSWORD` = 16-char token → 3. Redeploy |

---

## What Remains After Fix

Once PMA-012 is complete:
- Nataly's requests will generate deliverables AND email them to monaempoweryou@gmail.com in the same session
- Failures will show a specific error message (not ✓)
- Draft content is preserved to /tmp on failure as a debugging backstop

For persistent draft storage and attachment support: requires either Supabase integration (PMA-004 is blocked on credentials) or switching the email transport to SendGrid/Mailgun.

---

*Report completed: June 3, 2026*
