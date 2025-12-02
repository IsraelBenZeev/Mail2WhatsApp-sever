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


@routerTelegram.get("/webhook-test")
async def telegram_webhook_test():
    print("telegram_webhook_test called👉")
    return {"message": "Telegram webhook test received successfully"}


@routerTelegram.post("/webhook")
async def telegram_webhook(request: Request):
    print("telegram_webhook called👉")
    body = await request.json()
    print("body: ", body)
    text = body['message']['text'].split()[1] 
    # uuid = text.split()[1]  
    print("text: ", text)   

    chat_id = body.get("message", {}).get("chat", {}).get("id", "")
    user_id = body.get("message", {}).get("from", {}).get("id", "")
    await send_message_to_telegram(chat_id, "היי! מחברים אותך, כמה רגעים...")
    if await save_chat_id_to_supabase(chat_id, user_id):
        # client_url = os.getenv('CLIENT_URL')
        client_url = "https://vicbs-109-67-185-194.a.free.pinggy.link"
        text = f"החיבור עבר בהצלחה!\nחזור לאתר בכדי להגדיר כל כמה זמן תרצה לקבל מיילים לבוט\n\n <a href=\"{client_url}/connection-telegram\">לחץ כאן כדי לפתוח את האתר</a>"
        await send_message_to_telegram(chat_id, text, parse_mode="HTML")
    else:
        await send_message_to_telegram(chat_id, "החיבור נכשל. נסה שנית מאוחר יותר.")
