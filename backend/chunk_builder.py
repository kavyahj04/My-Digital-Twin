import json

def format_percent_langs(languages:dict) -> str:
    if not languages:
        return "Unknown"
    return ",".join(f"{lang} ({pct}%)" for lang, pct in sorted(languages.items(), key = lambda x: -x[1]))

def build_github_chunks(github_data: dict) -> list[dict]:
    chunks = []
    for repo in github_data["repos"]:
        breadcrumb = (
            f"Repo: {repo["repo_name"]}\n"
            f"Languages : {format_percent_langs(repo["languages"])}\n"
            f"Topics: {",".join(repo["topics"]) if repo["topics"] else 'None'}\n\n"
        )
        body = repo["description"] or ""
        if repo["readme_text"]:
            body += ("\n\n" if body else "") + repo["readme_text"]
        chunks.append({
            "text": breadcrumb + body,
            "source_type" : "github",
            "entity_name" : repo["repo_name"],
            "url" : repo["url"]
        })
    return chunks

def build_linkedin_chunks(linkedin_data:dict) -> list[dict]:
    chunks = []
    identity = linkedin_data["identity"]
    profile_url = identity.get("profile_url")

    if identity.get("about"):
        chunks.append({
            "text": f"About {identity["name"]}:\n{identity["headline"]}\n\n{identity["about"]}",
            "source_type" : "linkedin",
            "entity_name" : "summary",
            "url" : profile_url
    })
    
    for exp in linkedin_data["experience"]:
        breadcrumb = f"Role: {exp["title"]} at {exp["company"]} ({exp['start']}\u2013{exp["end"] or "Present"})\n\n"
        body = exp["description"] or "No detailed description provided."
        chunks.append({
            "text": breadcrumb + body,
            "source_type": "linkedin",
            "entity_name": f"{exp['title']} at {exp['company']}",
            "url": profile_url,
        })
    
    for edu in linkedin_data["education"]:
        breadcrumb = f"Education: {edu['degree']} in {edu['field_of_study']},{edu['school']} ({edu['start']}\u2013{edu['end'] or 'Present'})\n\n"
        chunks.append({
            "text": breadcrumb + (edu["description"] or ""),
            "source_type": "linkedin",
            "entity_name": edu["school"],
            "url": profile_url,
        })
    if linkedin_data["skills"]:
        skill_names = ", ".join(s["name"] for s in linkedin_data["skills"])
        chunks.append({
            "text": f"Skills:\n{skill_names}",
            "source_type": "linkedin",
            "entity_name": "Skills",
            "url": profile_url,
        })
    if linkedin_data["certifications"]:
        cert_lines = "\n".join(
            f"- {c['name']} ({c['issuer']}, {c['issued_date']})" for c in linkedin_data["certifications"]
        )
        chunks.append({
            "text": f"Certifications:\n{cert_lines}",
            "source_type": "linkedin",
            "entity_name": "Certifications",
            "url": profile_url,
        })
    if linkedin_data.get("featured_links"):
        usable_links = [f for f in linkedin_data["featured_links"] if f.get("url") and "/overlay/" not in f["url"]]
        if usable_links:
            links_text = "\n".join(f"- {f['title']} ({f['description']}): {f['url']}" for f in usable_links)
            chunks.append({
                "text": f"Featured links:\n{links_text}",
                "source_type": "linkedin",
                "entity_name": "Featured Links",
                "url": profile_url,
            })

    return chunks

def main():
    github_data = json.load(open("../rag/data/github_clean.json", encoding="utf-8"))
    linkedin_data = json.load(open("../rag/data/linkedin_clean.json", encoding="utf-8"))

    chunks = build_github_chunks(github_data) + build_linkedin_chunks(linkedin_data)

    with open("../rag/data/chunks.json", "w", encoding="utf-8") as f:
        json.dump(chunks, f, indent=2, ensure_ascii=False)

    print(f"Built {len(chunks)} chunks total ({len(github_data['repos'])} repos, {len(chunks) - len(github_data['repos'])} LinkedIn chunks)")


if __name__ == "__main__":
    main()