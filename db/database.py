import sqlite3
from datetime import date
from pathlib import Path

Path("db").mkdir(exist_ok=True)

def init_db():
    conn = sqlite3.connect("db/entries.db")
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS entries (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT NOT NULL,
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

def insert_entry(journal, intention, dream, priorities, reflection, strategy):
    conn = sqlite3.connect("db/entries.db")
    c = conn.cursor()
    c.execute('''
        INSERT INTO entries 
        (date, journal, intention, dream, priorities, reflection, strategy)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (str(date.today()), journal, intention, dream, priorities, reflection, strategy))
    conn.commit()
    conn.close()

def get_entries_by_date(entry_date):
    conn = sqlite3.connect("db/entries.db")
    c = conn.cursor()
    c.execute("SELECT * FROM entries WHERE date = ?", (entry_date,))
    data = c.fetchall()
    conn.close()
    return data
