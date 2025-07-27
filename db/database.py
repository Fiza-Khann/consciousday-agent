import sqlite3
from datetime import date

def init_db(db_name="reflections.db"):
    conn = sqlite3.connect(db_name)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS reflections (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            entry_date TEXT,
            journal TEXT,
            intention TEXT,
            dream TEXT,
            priorities TEXT,
            reflection TEXT,
            strategy TEXT
        )
    ''')
    conn.commit()
    conn.close()

def insert_entry(journal, intention, dream, priorities, reflection, strategy, db_name="reflections.db"):
    conn = sqlite3.connect(db_name)
    c = conn.cursor()
    c.execute('''
        INSERT INTO reflections (entry_date, journal, intention, dream, priorities, reflection, strategy)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (str(date.today()), journal, intention, dream, priorities, reflection, strategy))
    conn.commit()
    conn.close()

def get_entries_by_date(date_str=None, db_name="reflections.db"):
    if date_str is None:
        date_str = str(date.today())
    conn = sqlite3.connect(db_name)
    c = conn.cursor()
    c.execute('''
        SELECT * FROM reflections WHERE entry_date = ?
    ''', (date_str,))
    entries = c.fetchall()
    conn.close()
    return entries
