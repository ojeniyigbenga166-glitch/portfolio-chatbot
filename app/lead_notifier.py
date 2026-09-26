import os
import json
import logging
import urllib.request
from typing import Dict, Any

logger = logging.getLogger("lead_notifier")


def send_lead_notification(lead_data: Dict[str, Any]) -> bool:
    """
    Send a notification when a new potential client lead is received.
    Supports Webhook notification (e.g. Discord/Slack/Formspree/Zapier) 
    or falls back to structured logging.
    """
    name = lead_data.get("name", "Anonymous")
    email = lead_data.get("email", "No Email")
    message = lead_data.get("message", "No Message")
    service = lead_data.get("service", "General Inquiry")

    logger.info(f"New Lead Captured: Name={name}, Email={email}, Service={service}")

    webhook_url = os.getenv("LEAD_WEBHOOK_URL", "").strip()
    if not webhook_url:
        # Webhook not configured; lead is safely logged and processed
        return True

    try:
        payload = {
            "content": f"🚀 **New Lead Received for Olugbenga!**\n**Name:** {name}\n**Email:** {email}\n**Service:** {service}\n**Message:** {message}"
        }
        req = urllib.request.Request(
            webhook_url,
            data=json.dumps(payload).encode("utf-8"),
            headers={"Content-Type": "application/json", "User-Agent": "FastAPI-LeadNotifier/1.0"},
            method="POST"
        )
        with urllib.request.urlopen(req, timeout=5) as response:
            return response.status in (200, 201, 204)
    except Exception as e:
        logger.error(f"Failed to send lead webhook notification: {e}")
        return False
