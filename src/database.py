import sqlite3
from datetime import datetime
import os 

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATABASE = os.path.join(PROJECT_ROOT, "water_tracker.db")

def create_table():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS water_intake(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id TEXT,
        intake_ml INTEGER,
        date TEXT,
        time TEXT)
    """
    )

    conn.commit()
    conn.close()


def log_intake(user_id, intake_ml):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    date = datetime.today().strftime("%Y-%m-%d")
    time = datetime.now().strftime("%H:%M:%S")

    cursor.execute("""
        INSERT INTO water_intake (user_id, intake_ml, date, time) VALUES(?, ?, ?, ?)
    """, (user_id, intake_ml, date, time))

    conn.commit()
    conn.close() 

    
def get_intake(user_id):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()


    cursor.execute("SELECT intake_ml, date, time FROM water_intake WHERE user_id = ?", (user_id,))
    
    records = cursor.fetchall()

    conn.close() 
    return records

create_table()
