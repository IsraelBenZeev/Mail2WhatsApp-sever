from fastapi import APIRouter
from fastapi import Request

# from controllers.Telegram_Controller import telegram_webhook_controller
import os
import requests
import dotenv
from supabase_client import supabase
import httpx
from controllers.Telegram_Controller import (
    save_chat_id_to_supabase,
    send_message_to_telegram,
)

dotenv.load_dotenv(override=True)

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
routerTelegram = APIRouter()


@routerTelegram.post("/webhook")
async def telegram_webhook(request: Request):
    print("telegram_webhook called👉")
    body = await request.json()
    print("body: ", body)
    message_text = body.get("message", {}).get("text", "")
    print("message_text: ", message_text)

    chat_id = body.get("message", {}).get("chat", {}).get("id", "")

    parts = message_text.split()
    if len(parts) < 2:
        print("Error: No user_id provided in /start command")
        await send_message_to_telegram(
            chat_id, "שגיאה: לא התקבל מזהה משתמש. אנא נסה להתחבר שוב דרך הקישור באתר."
        )
        return

    user_id = parts[1]
    print("user_id extracted: ", user_id)

    await send_message_to_telegram(chat_id, "היי! מחברים אותך, כמה רגעים...")
    if await save_chat_id_to_supabase(chat_id, user_id):
        # client_url = os.getenv('CLIENT_URL')
        # client_url = os.getenv("CLIENT_URL")
        client_url = os.getenv("CLIENT_URL")
        text = f'החיבור עבר בהצלחה!\nחזור לאתר בכדי להגדיר כל כמה זמן תרצה לקבל מיילים לבוט\n\n <a href="{client_url}/connection-telegram">לחץ כאן כדי לפתוח את האתר</a> או העתק את הקישור {client_url}/connection-telegram'
        await send_message_to_telegram(chat_id, text, parse_mode="HTML")
    else:
        await send_message_to_telegram(chat_id, "החיבור נכשל. נסה שנית מאוחר יותר.")
