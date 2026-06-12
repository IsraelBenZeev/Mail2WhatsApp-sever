import base64
import json
import time
from fastapi import HTTPException, Header


def _decode_jwt_payload(token: str) -> dict:
    parts = token.split('.')
    if len(parts) != 3:
        raise ValueError("not a JWT")
    payload = parts[1]
    payload += '=' * (4 - len(payload) % 4)
    return json.loads(base64.urlsafe_b64decode(payload))


async def verify_supabase_token(authorization: str = Header(default=None)) -> str:
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Unauthorized")

    token = authorization.removeprefix("Bearer ").strip()

    try:
        payload = _decode_jwt_payload(token)

        user_id = payload.get("sub")
        if not user_id:
            raise HTTPException(status_code=401, detail="Unauthorized")

        exp = payload.get("exp", 0)
        if exp and time.time() > exp:
            raise HTTPException(status_code=401, detail="Unauthorized")

        return user_id
    except HTTPException:
        raise
    except Exception as e:
        print("auth error:", type(e).__name__, str(e)[:50])
        raise HTTPException(status_code=401, detail="Unauthorized")
