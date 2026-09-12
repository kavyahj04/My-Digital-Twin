import os 
import httpx
from fastapi import APIRouter, HTTPException
from fastapi.responses import RedirectResponse
from dotenv import load_dotenv

load_dotenv(override=True)

router = APIRouter()

CLIENT_ID = os.getenv("GITHUB_CLIENT_ID")
CLIENT_SECRET = os.getenv("GITHUB_CLIENT_SECRET")
REDIRECT_URI = os.getenv("GITHUB_REDIRECT_URI")


@router.get("/auth/login")
def login():
    github_url = (
        "https://github.com/login/oauth/authorize"
        f"?client_id={CLIENT_ID}"
        f"&redirect_uri={REDIRECT_URI}"
        f"&scope="
    )
    return RedirectResponse(github_url)

@router.get("/auth/callback")
async def callback(code:str):
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "https://github.com/login/oauth/access_token",
            data={
                "client_id": CLIENT_ID,
                "client_secret": CLIENT_SECRET,   
                "code": code,
                "redirect_uri": REDIRECT_URI,     
            },
            headers={"Accept": "application/json"},
        )
        data = response.json()

    if "access_token" not in data:
            raise HTTPException(status_code=400, detail=data.get("error_description", "OAuth failed"))
    else:
        return {"access_token": data["access_token"]}