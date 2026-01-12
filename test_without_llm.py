"""Quick test script to verify WebSpector works without LLM.

This tests the core functionality:
- Browser automation
- Screenshot capture
- Database storage
- Basic perception

Run this while waiting for LLaVA to download.
"""

from pathlib import Path
from datetime import datetime

print("=" * 60)
print("WebSpector Test (WITHOUT LLM)")
print("=" * 60)
print("\nThis will test the system WITHOUT AI analysis.")
print("Perfect for verifying everything works while model downloads!\n")

# Step 1: Database setup
print("[1/5] Setting up database...")
from dashboard.db import init_engine, init_db, TestSession, get_session

init_engine("sqlite:///dashboard.db")
init_db()

db = get_session()
try:
    session = TestSession(
        url="https://example.com",
        depth=1,
        label="Test Without LLM",
        status="running"
    )
    db.add(session)
    db.commit()
    db.refresh(session)
    session_id = session.id
    print(f"   [OK] Created test session #{session_id}")
finally:
    db.close()

# Step 2: Run crawler (without LLM)
print("\n[2/5] Running browser automation...")
print("   This will take ~30 seconds...")

from web_interaction.browser_driver import PlaywrightBrowserDriver
from web_interaction.crawler import crawl_site

out_dir = Path(f"captures/session_{session_id}")
out_dir.mkdir(parents=True, exist_ok=True)

try:
    with PlaywrightBrowserDriver(headless=True) as driver:
        captures = crawl_site(
            url="https://example.com",
            depth=1,
            out_dir=out_dir,
            driver=driver
        )
    print(f"   [OK] Captured {len(captures)} screenshots")
    print(f"   [OK] Screenshots saved to: {out_dir}")
except Exception as e:
    print(f"   [X] Error: {e}")
    import traceback
    traceback.print_exc()
    exit(1)

# Step 3: Run perception (basic analysis)
print("\n[3/5] Running basic perception analysis...")
from perception.perception import PerceptionPipeline
from dashboard.db import Screenshot, Perception

pipeline = PerceptionPipeline(
    enable_captioning=False,
    enable_ocr=False,
    enable_clip=False
)

db = get_session()
try:
    for meta in captures:
        screenshot_abs = out_dir / meta.screenshot_path
        observation = pipeline.analyze_screenshot(screenshot_abs)
        
        # Store screenshot
        rel_path = Path(f"session_{session_id}") / meta.screenshot_path
        screenshot = Screenshot(
            session_id=session_id,
            url=meta.url,
            viewport_name=meta.viewport.get("name", ""),
            width=int(meta.viewport.get("width", 0)),
            height=int(meta.viewport.get("height", 0)),
            screenshot_path=str(rel_path).replace("\\", "/"),
            dom_path=meta.dom_path,
            load_time=meta.load_time,
            captured_at=datetime.fromisoformat(meta.timestamp)
        )
        db.add(screenshot)
        db.flush()
        
        # Store perception
        obs_json = observation.to_json()
        perception = Perception(
            session_id=session_id,
            screenshot_id=screenshot.id,
            anomaly_score=observation.anomaly_score,
            caption=observation.caption,
            observation_json=str(obs_json)
        )
        db.add(perception)
    
    db.commit()
    print(f"   [OK] Analyzed {len(captures)} screenshots")
finally:
    db.close()

# Step 4: Update session
print("\n[4/5] Finalizing session...")
db = get_session()
try:
    session = db.query(TestSession).get(session_id)
    session.status = "completed"
    session.completed_at = datetime.utcnow()
    db.commit()
    print(f"   [OK] Session completed")
finally:
    db.close()

# Step 5: Summary
print("\n[5/5] Test Summary")
print("=" * 60)
print(f"Session ID: {session_id}")
print(f"Screenshots: {len(captures)}")
print(f"Location: {out_dir}")
print(f"Status: COMPLETED")
print("\n[OK] SUCCESS! Core system works perfectly!")

print("\n" + "=" * 60)
print("NEXT STEPS:")
print("=" * 60)
print("\n1. View in dashboard:")
print(f"   flask --app dashboard run")
print(f"   Then visit: http://localhost:5000/session/{session_id}")
print("\n2. Continue downloading LLaVA model:")
print("   ollama pull llava:7b")
print("   (Keep retrying - it resumes from where it stopped)")
print("\n3. Once model is downloaded:")
print("   - Change .env: LLM_ANALYSIS_ENABLED=true")
print("   - Run: python demo_llm_qa.py")
print("   - Get AI-powered analysis!")

print("\n" + "=" * 60)
print("The system works great without LLM!")
print("LLM just adds AI analysis on top of existing features.")
print("=" * 60)
