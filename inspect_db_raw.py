import sqlite3
import os

db_path = "dashboard.db"

if not os.path.exists(db_path):
    print(f"Database not found at {db_path}")
    exit(1)

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

print("--- Recent Sessions ---")
cursor.execute("SELECT id, url, status, created_at FROM test_sessions ORDER BY id DESC LIMIT 5")
sessions = cursor.fetchall()
for s in sessions:
    print(f"Session {s[0]}: {s[1]} ({s[2]}) - {s[3]}")

if sessions:
    latest_id = sessions[0][0]
    print(f"\n--- Issues for Session {latest_id} ---")
    cursor.execute("SELECT id, title, severity, issue_type, description, recommended_action FROM issues WHERE session_id = ?", (latest_id,))
    issues = cursor.fetchall()
    if issues:
        for i in issues:
            print(f"Issue {i[0]}: [{i[2]}] {i[1]}")
            print(f"  Type: {i[3]}")
            print(f"  Desc: {i[4]}")
            print(f"  Action: {i[5]}")
            print("-" * 20)
    else:
        print("NO ISSUES FOUND for this session.")

    print(f"\n--- Screenshots for Session {latest_id} ---")
    cursor.execute("SELECT id, screenshot_path FROM screenshots WHERE session_id = ?", (latest_id,))
    screenshots = cursor.fetchall()
    if screenshots:
        for s in screenshots:
            print(f"Screenshot {s[0]}: {s[1]}")
    else:
        print("NO SCREENSHOTS FOUND for this session.")

conn.close()
