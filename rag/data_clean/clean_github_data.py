import re


def compute_language_percentages(languages: dict) -> dict:
    total = sum(languages.values())
    if total == 0:
        return {}
    return {lang: round(bytes_ * 100 / total, 1) for lang, bytes_ in languages.items()}


def clean_readme(text: str | None) -> str:
    if not text:
        return ""
    text = re.sub(r"!\[[^\]]*\]\([^)]*\)", "", text)          # strip badge/image markdown
    text = re.sub(r"<!--.*?-->", "", text, flags=re.DOTALL)    # strip HTML comments
    text = re.sub(r"\n{3,}", "\n\n", text)                     # collapse repeated blank lines
    return text.strip()


def clean_repo_dataset(raw_repos: list[dict], exclude_forks: bool = True) -> dict:
    cleaned = []
    for r in raw_repos:
        if exclude_forks and r.get("is_fork"):
            continue
        cleaned.append({
            "repo_name": r["repo_name"],
            "description": r.get("description"),
            "readme_text": clean_readme(r.get("readme_text")),
            "languages": compute_language_percentages(r.get("languages", {})),
            "topics": r.get("topics", []),
            "stars": r.get("stars", 0),
            "url": r["url"],
        })
    return {
        "source_type": "github",
        "repos": cleaned,
    }