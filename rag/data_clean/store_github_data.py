import asyncio
import json
from github_data import build_repo_dataset
from clean_github_data import clean_repo_dataset


async def main(token: str):
    raw = await build_repo_dataset(token)
    cleaned = clean_repo_dataset(raw)
    with open("github_clean.json", "w", encoding="utf-8") as f:
        json.dump(cleaned, f, indent=2, ensure_ascii=False)
    print(f"Stored {len(cleaned['repos'])} repos to github_clean.json")


if __name__ == "__main__":
    import sys
    asyncio.run(main(sys.argv[1]))