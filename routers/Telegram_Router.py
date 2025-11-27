from fastapi import APIRouter
from fastapi import Request
from controllers.Telegram_Controller import telegram_webhook_controller
import os
import requests
import dotenv
from supabase_client import supabase

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
    chat_id = body.get("message", {}).get("chat", {}).get("id", "")
    response = requests.post(
        f"https://api.telegram.org/bot{TOKEN}/sendMessage",
        data={"chat_id": chat_id, "text": "היי! מחברים אותך, כמה רגעים..."},
    )
    print("body: ", body)
    text = body.get("message", {}).get("text", "")  # "/start PAYLOAD"
    print("text: ", text)
    payload = text.split(" ")[1] if " " in text else None
    print("chat_id: ", chat_id)
    print("payload: ", payload)
    response_supabase = (
        supabase.table("user_chat_ids")
        .upsert({"user_id": payload, "chat_id": chat_id}, on_conflict="user_id")
        .execute()
    )
    print("response: ", response)
    print("response_supabase: ", response_supabase.data)
    return {"message": "Telegram webhook received successfully"}
    # return await telegram_webhook_controller(body)
