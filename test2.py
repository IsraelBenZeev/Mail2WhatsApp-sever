import schedule
import time
import asyncio
from datetime import datetime
from supabase_client import supabase
from test import get_emails

def do_action(user):
    print(f"מבצע פעולה על היוזר {user['user_id']} בשעה {user['time']}")
    asyncio.run(get_emails(user['user_id'], user['chat_id']))
    print("--------------------------------")

def check_users():
    now = datetime.now().strftime("%H:%M")
    users = supabase.from_("user_chat_ids").select("*").execute()
    for user in users.data:
        user_time = user['time'][:5]
        print("now: ", now)
        print("user_time: ", user_time)
        if now == user_time:
            do_action(user)

schedule.every(2).seconds.do(check_users)

try:
    while True:
        schedule.run_pending()
        time.sleep(1)
except KeyboardInterrupt:
    print("התוכנית הופסקה ידנית")
