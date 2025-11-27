from supabase_client import supabase
from fastapi.responses import RedirectResponse
import os
import dotenv

dotenv.load_dotenv(override=True)

async def telegram_webhook_controller(body: dict):
    print("telegram_webhook_controller: ", body)
    return {"message": "Telegram webhook received successfully"}