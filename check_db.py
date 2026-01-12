
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parents[0]))

from dashboard.db import init_engine, get_session, TestSession, Issue, Screenshot

def check_latest():
    init_engine("sqlite:///dashboard.db")
    db = get_session()
    try:
        sess = db.query(TestSession).order_by(TestSession.id.desc()).first()
        if not sess:
            print("No sessions found.")
            return

        print(f"Latest Session ID: {sess.id}")
        print(f"URL: {sess.url}")
        print(f"Status: {sess.status}")
        
        issues = db.query(Issue).filter(Issue.session_id == sess.id).all()
        print(f"Issues found: {len(issues)}")
        
        screenshots = db.query(Screenshot).filter(Screenshot.session_id == sess.id).all()
        print(f"Screenshots found: {len(screenshots)}")
        for s in screenshots:
            print(f"  - ID: {s.id}, Path: {s.screenshot_path} ({s.width}x{s.height})")
            p = Path("captures") / s.screenshot_path
            if p.exists():
                print(f"    [OK] File exists: {p}")
            else:
                print(f"    [MISSING] File not found: {p}")

    finally:
        db.close()

if __name__ == "__main__":
    check_latest()
