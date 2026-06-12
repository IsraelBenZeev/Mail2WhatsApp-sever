from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
import os
from dotenv import load_dotenv

load_dotenv(override=True)
# print("GOOGLE_CLIENT_SECRETS_JSON: ", os.getenv("GOOGLE_CLIENT_SECRET_JSON"))
from routers.LLM_Router import routerLLM
from routers.OAuth_Callback_Router import routerOAuthCallback
from routers.Users_Router import routerUsers
from routers.Auth_signin_Router import routerAuthSignin
from routers.Telegram_Router import routerTelegram
from routers.Nutrition_Router import routerNutrition
from limiter import limiter
# from supabase_client import supabase

app = FastAPI()
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
# origins = [
#     "http://localhost:5173",
#     "http://localhost:5174",
# ]
origins = [
    os.getenv("CLIENT_URL"),
    # for dev
    "http://localhost:5173",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():

    print("root endpoint called!🙌")
    os.system('cls')
    return {"message": "Welcome to the Mail2WhatsApp server!", "version": "1.0"}


app.include_router(routerLLM, prefix="/llm", tags=["llm"])
# app.include_router(routerOAuthCallback, prefix="/isr", tags=["isr"])
app.include_router(routerOAuthCallback, prefix="/OAuth", tags=["OAuth"])
app.include_router(routerAuthSignin, prefix="/Auth", tags=["Auth"])
app.include_router(routerUsers, prefix="/users", tags=["users"])
app.include_router(routerTelegram, prefix="/telegram", tags=["telegram"])
app.include_router(routerNutrition, prefix="/nutrition", tags=["nutrition"])

HOST = os.getenv("HOST")

if __name__ == "__main__":
    if os.getenv("ENVIRONMENT") == "development":
        import uvicorn

        port = int(os.getenv("PORT", "8000"))
        print(f"Server running on {HOST}:{port}")
        print("Registered routes:")
        for route in app.routes:
            if hasattr(route, "path") and hasattr(route, "methods"):
                print(f"  {list(route.methods)} {route.path}")
        uvicorn.run(app, host="0.0.0.0", port=port, reload=True)


# פקודת הרצה uv run uvicorn app:app --reload
# פקודת הרצה uv run python -m uvicorn app:app --host 127.0.0.1 --port 8000 --reload
