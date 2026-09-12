import json
import re


def format_date(d: dict) -> str | None:
    if not d:
        return None
    if "month" in d and "year" in d:
        return f"{d['month']} {d['year']}"
    if "year" in d:
        return str(d["year"])
    return None


def clean_description(text: str) -> str:
    if not text:
        return ""
    lines = [l.strip().lstrip("•").strip() for l in text.split("\n") if l.strip()]
    return " ".join(lines)


def clean_certification_name(name: str) -> str:
    # this exporter url-encodes some certificate names with "+" instead of spaces
    return re.sub(r"\s+", " ", name.replace("+", " ")).strip()


def clean_experience(entries: list[dict]) -> list[dict]:
    cleaned = []
    for e in entries:
        cleaned.append({
            "title": e.get("title"),
            "company": e.get("company"),
            "employment_type": e.get("employment_type") or None,
            "location": e.get("location") or None,
            "start": format_date(e.get("start_date", {})),
            "end": format_date(e.get("end_date", {})) or ("Present" if e.get("is_current") else None),
            "duration_text": e.get("duration"),
            "description": clean_description(e.get("description", "")),
            "skills": e.get("skills", []),
        })
    return cleaned


def clean_education(entries: list[dict]) -> list[dict]:
    cleaned = []
    for e in entries:
        cleaned.append({
            "school": e.get("school"),
            "degree": e.get("degree_name") or None,
            "field_of_study": e.get("field_of_study") or None,
            "start": format_date(e.get("start_date", {})),
            "end": format_date(e.get("end_date", {})),
            "grade": e.get("grade") or None,
            "description": clean_description(e.get("description", "")),
        })
    return cleaned


def clean_certifications(entries: list[dict]) -> list[dict]:
    cleaned = []
    for c in entries:
        issued = c.get("issued_date") or ""
        cleaned.append({
            "name": clean_certification_name(c.get("name", "")),
            "issuer": c.get("issuer"),
            "issued_date": issued.replace("Issued ", "").strip() or None,
            "skills": c.get("skills", []),
            "credential_url": c.get("credential_url") or None,
        })
    return cleaned


def clean_featured(entries: list[dict]) -> list[dict]:
    return [
        {"title": f.get("title"), "description": f.get("description"), "url": f.get("url")}
        for f in entries
    ]


def clean_skills(entries: list[dict]) -> list[dict]:
    return [
        {"name": s.get("name"), "endorsement_count": s.get("endorsement_count", 0)}
        for s in entries
    ]


def clean_linkedin_dataset(raw_path: str) -> dict:
    with open(raw_path, encoding="utf-8") as f:
        raw = json.load(f)
    record = raw[0] if isinstance(raw, list) else raw  
    basic = record.get("basic_info", {})

    return {
        "source_type": "linkedin",
        "identity": {
            "name": basic.get("fullname"),
            "headline": basic.get("headline"),
            "about": (basic.get("about") or "").strip(),
            "location": (basic.get("location") or {}).get("full"),
            "current_company": basic.get("current_company"),
            "open_to_work": basic.get("open_to_work", False),
            "profile_url": basic.get("profile_url") or record.get("profileUrl"),
        },
        "experience": clean_experience(record.get("experience", [])),
        "education": clean_education(record.get("education", [])),
        "certifications": clean_certifications(record.get("certifications", [])),
        "skills": clean_skills(record.get("skills", [])),
        "featured_links": clean_featured(record.get("featured", [])),
        "recommendations": record.get("recommendations", []),  # empty in your export - passthrough until you have a real example
    }


if __name__ == "__main__":
    result = clean_linkedin_dataset("../data/dataset_linkedin-profile-full-sections-scraper_2026-09-12_15-08-11-340.json")
    with open("linkedin_clean.json", "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)
    print(json.dumps(result, indent=2, ensure_ascii=False))