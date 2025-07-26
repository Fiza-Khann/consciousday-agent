import sqlite3
from datetime import date
from pathlib import Path

# Ensure the 'db' directory exists
Path("db").mkdir(exist_ok=True)

def init_db():
    # Create the database and table if they don't already exist
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
    # Insert a new entry for the current date
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
    # Fetch all entries for a given date
    conn = sqlite3.connect("db/entries.db")
    c = conn.cursor()
    c.execute("SELECT * FROM entries WHERE date = ?", (entry_date,))
    data = c.fetchall()
    conn.close()
    return data
