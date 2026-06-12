from fastapi import HTTPException, Header
from supabase_client import supabase


def verify_supabase_token(authorization: str = Header(default=None)) -> str:
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Unauthorized")

    token = authorization.removeprefix("Bearer ").strip()

    try:
        result = supabase.auth.get_user(token)
        if not result.user:
            raise HTTPException(status_code=401, detail="Unauthorized")
        return result.user.id
    except HTTPException:
        raise
    except Exception as e:
        print("verify_supabase_token error:", type(e).__name__, str(e))
        raise HTTPException(status_code=401, detail="Unauthorized")
