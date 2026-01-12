
import os
import sys
from pathlib import Path
from datetime import datetime

# Add project root to path
sys.path.append(str(Path(__file__).resolve().parents[1]))

from dashboard.app import execute_full_run
from dashboard.db import init_engine, init_db, get_session, TestSession

def reproduce():
    print("Initializing DB...")
    db_url = "sqlite:///dashboard.db"
    init_engine(db_url)
    init_db()

    url = "https://www.wikipedia.org/"
    print(f"Starting test run for {url}...")

    db = get_session()
    try:
        sess = TestSession(url=url, depth=1, label="Reproduction Run", status="running")
        db.add(sess)
        db.commit()
        db.refresh(sess)
        print(f"Created session {sess.id}")

        captures_root = Path("captures")
        out_dir = captures_root / f"session_{sess.id}"
        out_dir.mkdir(parents=True, exist_ok=True)

        execute_full_run(url=url, depth=1, out_dir=out_dir, db=db, test_session=sess)

        sess.status = "completed"
        sess.completed_at = datetime.utcnow()
        db.commit()
        print("Test run completed successfully.")

    except Exception as e:
        print(f"Test run failed: {e}")
        import traceback
        traceback.print_exc()
        if 'sess' in locals():
            sess.status = "failed"
            db.commit()
    finally:
        db.close()

if __name__ == "__main__":
    reproduce()
