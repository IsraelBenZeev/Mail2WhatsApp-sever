import schedule
import time
from datetime import datetime
from supabase_client import supabase
from controllers.Telegram_Controller import send_message_to_telegram
# פונקציה שמבצעת פעולה על המשתמש
def do_action(user):
    print(f"מבצע פעולה על היוזר {user['id']} בשעה {user['time']}")

# פונקציה שבודקת את כל היוזרים
def check_users():
    result = supabase.auth.admin.list_users()
    print("result: ", result)
    # send_message_to_telegram(chat_id=result[0]["user_id"], text="TEST TEST TEST...")
    # for user in users.data:
        # כאן אפשר לבדוק לפי שעה אם רוצים
        # if user["time"] == now:
        # do_action(user)

# קובע שיבוצע כל 3 שניות (לבדיקה)
schedule.every(2).seconds.do(check_users)

# לולאה שמריצה את ה-schedule
try:
    while True:
        print("-----------------------------------------")
        schedule.run_pending()
        time.sleep(1)
except KeyboardInterrupt:
    print("התוכנית הופסקה ידנית")
