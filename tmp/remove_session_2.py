import sqlite3
import os
from pathlib import Path

def remove_session(session_id):
    # Determine the database path relative to this script
    # It's in the project root: d:\web-spector\dashboard.db
    db_path = Path("dashboard.db")
    
    if not db_path.exists():
        print(f"Database not found at {db_path.absolute()}")
        return

    conn = sqlite3.connect(str(db_path))
    cursor = conn.cursor()
    
    try:
        print(f"Purging all data for Session ID: {session_id}")
        
        # We manually handle cascading deletes since we aren't using SQLAlchemy here
        # and standard SQLite might not have foreign_keys enabled by default.
        cursor.execute("PRAGMA foreign_keys = ON;")
        
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
    remove_session(2)
