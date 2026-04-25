import sqlite3
import os
from pathlib import Path

def remove_session(db_path, session_id):
    if not os.path.exists(db_path):
        print(f"Database not found at {db_path}")
        return

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        print(f"Purging all data for Session ID: {session_id}")
        
        # 1. Delete LLM Analyses related to actions of this session
        cursor.execute("""
            DELETE FROM llm_analyses 
            WHERE action_id IN (SELECT id FROM actions WHERE session_id = ?)
        """, (session_id,))
        print(f"Deleted {cursor.rowcount} LLM analyses.")
        
        # 2. Delete Actions
        cursor.execute("DELETE FROM actions WHERE session_id = ?", (session_id,))
        print(f"Deleted {cursor.rowcount} actions.")
        
        # 3. Delete Issues
        cursor.execute("DELETE FROM issues WHERE session_id = ?", (session_id,))
        print(f"Deleted {cursor.rowcount} issues.")
        
        # 4. Delete Perceptions
        cursor.execute("DELETE FROM perceptions WHERE session_id = ?", (session_id,))
        print(f"Deleted {cursor.rowcount} perceptions.")
        
        # 5. Delete Screenshots
        cursor.execute("DELETE FROM screenshots WHERE session_id = ?", (session_id,))
        print(f"Deleted {cursor.rowcount} screenshots.")
        
        # 6. Delete the Session itself
        cursor.execute("DELETE FROM test_sessions WHERE id = ?", (session_id,))
        print(f"Deleted {cursor.rowcount} session record.")
        
        conn.commit()
        print("Surgical purge complete.")
        
    except sqlite3.Error as e:
        print(f"SQLite error: {e}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == "__main__":
    db_path = "dashboard.db"
    remove_session(db_path, 2)
