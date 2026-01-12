from dashboard.app import create_app
from dashboard.db import get_session, TestSession, Screenshot, Issue
from pathlib import Path
import os

app = create_app()
app.app_context().push()
db = get_session()

session_id = 5
sess = db.query(TestSession).get(session_id)

if not sess:
    print(f"Session {session_id} not found!")
else:
    print(f"Session {sess.id}: {sess.url} ({sess.status})")
    print(f"Created: {sess.created_at}")
    
    issues = db.query(Issue).filter(Issue.session_id == session_id).all()
    print(f"Issues found: {len(issues)}")
    
    screenshots = db.query(Screenshot).filter(Screenshot.session_id == session_id).all()
    print(f"Screenshots found: {len(screenshots)}")
    
    for s in screenshots:
        print(f"  Screenshot {s.id}: {s.file_path} (Viewport: {s.viewport_name})")
        # Check if file exists
        full_path = Path(app.config['CAPTURES_ROOT']) / s.file_path
        print(f"    Full path: {full_path}")
        print(f"    Exists: {full_path.exists()}")
        
        # List dir to see what's actually there
        parent = full_path.parent
        if parent.exists():
            print(f"    Files in {parent}: {list(parent.glob('*'))}")
        else:
            print(f"    Parent dir {parent} does not exist")
