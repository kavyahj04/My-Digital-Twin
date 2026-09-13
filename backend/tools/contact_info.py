import json
from datetime import datetime, timezone


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

LEADS_FILE = "leads.jsonl"

def collect_contact_info(name:str, email:str, phone:str| None = None, reason:str|None = None) -> dict:
    lead = {
        "name" : name,
        "email" : email,
        "phone" : phone,
        "reason" : reason,
        "captured_at" : datetime.now(timezone.utc).isoformat(),
    }

    with open(LEADS_FILE, "a", encoding="utf-8") as f:
        f.write(json.dumps(lead) + "\n")
    
    return {
        "status" : "success",
        "message" : "Thanks {name}, your info has been recorded"
    }