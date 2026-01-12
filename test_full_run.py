from dashboard.app import create_app, execute_full_run
from dashboard.db import get_session, TestSession, Screenshot, Issue
from pathlib import Path
import traceback

def run_test():
    app = create_app()
    app.app_context().push()
    db = get_session()
    
    print("Creating test session...")
    sess = TestSession(url='https://www.wikipedia.org/', depth=1, status='running')
    db.add(sess)
    db.commit()
    db.refresh(sess)
    print(f"Session {sess.id} created.")
    
    out_dir = Path(app.config['CAPTURES_ROOT']) / f"session_{sess.id}"
    out_dir.mkdir(parents=True, exist_ok=True)
    
    print(f"Starting full run for session {sess.id}...")
    try:
        execute_full_run('https://www.wikipedia.org/', 1, out_dir, db, sess)
        sess.status = 'completed'
        db.commit()
        print('Full run completed successfully!')
        
        # Verify results immediately
        screenshots = db.query(Screenshot).filter(Screenshot.session_id == sess.id).all()
        print(f"Screenshots captured: {len(screenshots)}")
        for s in screenshots:
            print(f"  - {s.screenshot_path}")
            
        issues = db.query(Issue).filter(Issue.session_id == sess.id).all()
        print(f"Issues found: {len(issues)}")
        
    except Exception as e:
        print(f'Run failed: {e}')
        traceback.print_exc()
        sess.status = 'failed'
        db.commit()

if __name__ == "__main__":
    run_test()
