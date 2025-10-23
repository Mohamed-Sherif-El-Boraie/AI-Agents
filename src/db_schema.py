from __future__ import annotations
from pathlib import Path
import sys
sys.path.append(str(Path(__file__).resolve().parents[1]))

import sqlite3

from typing import Iterable, Optional, Tuple

from config.config import *
from config.logger import *



DB_PATH = Path(__file__).resolve().parents[1] / "database" / "database.db"
DB_PATH.parent.mkdir(parents=True, exist_ok=True)

DDL = """
CREATE TABLE IF NOT EXISTS findings (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  topic TEXT NOT NULL,
  source_url TEXT,
  snippet TEXT NOT NULL,
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_findings_topic ON findings(topic);
"""

def get_conn() -> sqlite3.Connection:
    conn = sqlite3.connect(str(DB_PATH))
    conn.execute("PRAGMA journal_mode=WAL;")
    conn.execute("PRAGMA synchronous=NORMAL;")
    conn.execute("PRAGMA foreign_keys=ON;")
    return conn

def init_db() -> None:
    """Initialize the database with the DDL schema"""
    with get_conn() as conn:
        conn.executescript(DDL)

def insert_findings(rows: Iterable[Tuple[str, Optional[str], str]]) -> int:
    """
    rows: iterable of (topic, source_url, snippet)
    returns: number of rows inserted
    """
    with get_conn() as conn:
        cur = conn.executemany(
            "INSERT INTO findings(topic, source_url, snippet) VALUES (?, ?, ?)", rows
        )
        return cur.rowcount

def read_findings(topic: str, limit: int = 10) -> list[tuple[int, str, str, str, str]]:
    '''
    Search the database for findings about the topic
    '''
    with get_conn() as conn:
        cur = conn.execute(
            "SELECT id, topic, source_url, snippet, created_at "
            "FROM findings WHERE topic=? ORDER BY id DESC LIMIT ?",
            (topic, limit),
        )
        return cur.fetchall()


if __name__ == "__main__":

    init_db()
    
    