import os
import sys
from pathlib import Path

# Add project root to sys.path
project_root = Path(__file__).resolve().parent
sys.path.append(str(project_root))

from dashboard.app import create_app
from dashboard.db import get_session, TestSession, Issue, Screenshot

app = create_app()

with app.app_context():
    db = get_session()
    try:
        # Try to export session 19
        session_id = 19
        sess = db.query(TestSession).get(session_id)
        if not sess:
            print(f"Session {session_id} not found")
            sys.exit(1)
            
        from sqlalchemy.orm import joinedload
        issues = db.query(Issue).options(joinedload(Issue.screenshot)).filter(Issue.session_id == session_id).order_by(Issue.id).all()
        
        import csv
        from io import StringIO, BytesIO
        
        output = StringIO()
        writer = csv.writer(output)
        writer.writerow(["id", "url"])
        for issue in issues:
            writer.writerow([issue.id, issue.screenshot.url if issue.screenshot else ""])
            
        csv_bytes = output.getvalue().encode("utf-8")
        stream = BytesIO(csv_bytes)
        print("CSV generation successful.")
        
    except Exception as e:
        import traceback
        traceback.print_exc()
    finally:
        db.close()
