import sqlite3
from typing import List, Dict, Any

DB_NAME = "C:/2024/h/Moshi/Moshi.MyMusic/spotify.db"

def execute_query(query: str, params: tuple = ()) -> List[Dict[str, Any]]:
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute(query, params)
    result = [dict(row) for row in cursor.fetchall()]
    conn.commit()
    conn.close()
    return result

def execute_insert(query: str, params: tuple = ()) -> int:
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute(query, params)
    last_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return last_id

def execute_update_delete(query: str, params: tuple = ()) -> int:
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute(query, params)
    affected_rows = cursor.rowcount
    conn.commit()
    conn.close()
    return affected_rows