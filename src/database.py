import sqlite3
from pathlib import Path
from datetime import datetime


BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "db" / "leads.db"


def init_db():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS leads (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT,
            company TEXT,
            role_interest TEXT,
            recruiter_message TEXT,
            top_project TEXT,
            created_at TEXT NOT NULL
        )
        """
    )

    conn.commit()
    conn.close()


def add_lead(name, email, company, role_interest, recruiter_message, top_project):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO leads (
            name,
            email,
            company,
            role_interest,
            recruiter_message,
            top_project,
            created_at
        )
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        (
            name,
            email,
            company,
            role_interest,
            recruiter_message,
            top_project,
            datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        )
    )

    conn.commit()
    conn.close()


def get_all_leads():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT
            id,
            name,
            email,
            company,
            role_interest,
            recruiter_message,
            top_project,
            created_at
        FROM leads
        ORDER BY created_at DESC
        """
    )

    rows = cursor.fetchall()
    conn.close()

    return rows