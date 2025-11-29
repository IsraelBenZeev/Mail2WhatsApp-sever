from supabase_client import supabase
from fastapi.responses import RedirectResponse
import os
import dotenv
import httpx

dotenv.load_dotenv(override=True)

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")


async def save_chat_id_to_supabase(chat_id: str, user_id: str):
    try:
        supabase.table("user_chat_ids").upsert(
            {"user_id": user_id, "chat_id": chat_id}
        ).execute()
        print(f"Chat ID {chat_id} saved successfully for user {user_id}")
        return True
    except Exception as e:
        print(f"Error saving chat ID {chat_id} to Supabase for user {user_id}: {e}")
        return False


async def send_message_to_telegram(chat_id: str, text: str, parse_mode: str = "HTML"):
    try:
        response = await httpx.AsyncClient().post(
            url=f"https://api.telegram.org/bot{TOKEN}/sendMessage",
            json={"chat_id": chat_id, "text": text, "parse_mode": parse_mode},
        )
        if response.status_code != 200:
            print(f"Telegram API Error: {response.status_code} - {response.text}")

        return {"message": "Message sent successfully"}
    except Exception as e:
        print(f"Error sending message to Telegram: {e}")
        return {"message": "Error sending message to Telegram"}
