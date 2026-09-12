import base64
import httpx

GITHUB_API = "https://api.github.com"


async def list_repos(token: str) -> list[dict]:
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{GITHUB_API}/user/repos",
            headers={"Authorization": f"Bearer {token}"},
            params={"per_page": 100, "type": "owner"},
        )
    response.raise_for_status()
    return response.json()


async def get_readme(token: str, owner: str, repo: str) -> str | None:
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{GITHUB_API}/repos/{owner}/{repo}/readme",
            headers={"Authorization": f"Bearer {token}"},
        )
    if response.status_code == 404:
        return None
    response.raise_for_status()
    encoded = response.json()["content"]
    return base64.b64decode(encoded).decode("utf-8", errors="ignore")


async def get_languages(token: str, owner: str, repo: str) -> dict[str, int]:
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{GITHUB_API}/repos/{owner}/{repo}/languages",
            headers={"Authorization": f"Bearer {token}"},
        )
    response.raise_for_status()
    return response.json()


async def build_repo_dataset(token: str) -> list[dict]:
    repos = await list_repos(token)
    dataset = []
    for repo in repos:
        owner = repo["owner"]["login"]
        name = repo["name"]
        readme_text = await get_readme(token, owner, name)
        languages = await get_languages(token, owner, name)
        dataset.append({
            "repo_name": name,
            "description": repo.get("description"),
            "readme_text": readme_text,
            "languages": languages,
            "url": repo["html_url"],
            "is_fork": repo.get("fork", False),
            "topics": repo.get("topics", []),
            "stars": repo.get("stargazers_count", 0),
        })
    return dataset