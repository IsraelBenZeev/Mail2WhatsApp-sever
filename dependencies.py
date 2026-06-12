import os
import httpx
from fastapi import HTTPException, Header

SUPABASE_URL = os.getenv("SUPABASE_URL", "")
SUPABASE_ROLE_KEY = os.getenv("SUPABASE_ROLE_KEY", "")


async def verify_supabase_token(authorization: str = Header(default=None)) -> str:
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Unauthorized")

    token = authorization.removeprefix("Bearer ").strip()

    try:
        async with httpx.AsyncClient() as client:
            r = await client.get(
                f"{SUPABASE_URL}/auth/v1/user",
                headers={
                    "Authorization": f"Bearer {token}",
                    "apikey": SUPABASE_ROLE_KEY,
                },
                timeout=5.0,
            )

        if r.status_code != 200:
            print("auth failed:", r.status_code, r.text[:150])
            raise HTTPException(status_code=401, detail="Unauthorized")

        return r.json()["id"]
    except HTTPException:
        raise
    except Exception as e:
        print("auth error:", type(e).__name__, str(e)[:100])
        raise HTTPException(status_code=401, detail="Unauthorized")
