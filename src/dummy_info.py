import sqlite3
import random
from datetime import datetime, timedelta
from database import create_table, DATABASE

def log_vals(user_id="user_123"):
    today = datetime.today().date()

    for i in range(1, 7):
        day = today - timedelta(days=i)

        intake_ml = random.choice([300, 500, 750, 1000, 1200, 1500])

        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO water_intake (user_id, intake_ml, date, time)
            VALUES (?, ?, ?, ?)
        """, (user_id, intake_ml, day.strftime("%Y-%m-%d"), "12:00:00"))

        conn.commit()
        conn.close()

if __name__ == "__main__":
    create_table()
    log_vals("user_123")
