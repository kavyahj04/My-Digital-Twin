import json
import os
from datetime import datetime, timezone

import gspread
from google.oauth2.service_account import Credentials


COLLECT_CONTACT_INFO_SCHEMA = {
    "type" : "function",
    "function" : {
        "name" : "collect_contact_info",
        "description" : (
            "Capture a visitor's contact information when they express interest in "
            "being contacted, followed up with, or want to connect further. Only call "
            "this when the visitor has clearly indicated they want to be reached out to "
            "- not just because they mentioned their name in passing."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "name": {"type": "string", "description": "The visitor's full name"},
                "email": {"type": "string", "description": "The visitor's email address"},
                "phone": {"type": "string", "description": "The visitor's phone number, if provided"},
                "reason": {"type": "string", "description": "Why the visitor wants to be contacted"},
            },
            "required": ["name", "email"],
        }
    }
}

SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]

_worksheet = None

def _get_worksheet():
    global _worksheet
    if _worksheet is None:
        creds_json = os.getenv("GOOGLE_SERVICE_ACCOUNT_JSON")
        sheet_id = os.getenv("LEADS_SHEET_ID")
        if not creds_json or not sheet_id:
            raise RuntimeError(
                "GOOGLE_SERVICE_ACCOUNT_JSON and LEADS_SHEET_ID must be set to record leads"
            )
        creds = Credentials.from_service_account_info(json.loads(creds_json), scopes=SCOPES)
        client = gspread.authorize(creds)
        _worksheet = client.open_by_key(sheet_id).sheet1
    return _worksheet

def collect_contact_info(name:str, email:str, phone:str| None = None, reason:str|None = None) -> dict:
    timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %I:%M %p UTC")
    row = [timestamp, name, email, phone or "", reason or ""]
    _get_worksheet().append_row(row)

    return {
        "status" : "success",
        "message" : f"Thanks {name}, your info has been recorded"
    }