from pathlib import Path
import sys
import json
from datetime import datetime

from PIL import Image, ImageDraw

# Ensure project root is on sys.path so `dashboard` package can be imported when
# running this script directly from scripts/.
project_root = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(project_root))

from dashboard.db import (
    init_engine,
    init_db,
    get_session,
    TestSession,
    Screenshot,
    Perception,
    Issue,
    Action,
    LLMAnalysis,
)


def make_placeholder_image(path: Path, text: str = "Screenshot") -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    img = Image.new("RGB", (1024, 768), color=(73, 109, 137))
    d = ImageDraw.Draw(img)
    d.text((20, 20), text, fill=(255, 255, 0))
    img.save(path)


def main() -> None:
    global project_root
    db_path = project_root / "dashboard.db"
    database_url = f"sqlite:///{db_path}"

    print(f"Initializing DB at: {db_path}")
    init_engine(database_url)
    init_db()

    db = get_session()

    try:
        # Create a demo session
        sess = TestSession(
            url="https://example.com",
            depth=1,
            label="Demo session",
            status="completed",
            created_at=datetime.utcnow(),
            completed_at=datetime.utcnow(),
        )
        db.add(sess)
        db.flush()

        captures_root = project_root / "captures"
        out_dir = captures_root / f"session_{sess.id}"
        out_dir.mkdir(parents=True, exist_ok=True)

        # Create 3 placeholder screenshots
        shots = []
        for i in range(1, 4):
            filename = f"screenshot_{i}.png"
            abs_path = out_dir / filename
            make_placeholder_image(abs_path, text=f"Session {sess.id} - Shot {i}")

            rel_path = Path(f"session_{sess.id}") / filename
            shot = Screenshot(
                session_id=sess.id,
                url=f"https://example.com/page{i}",
                viewport_name="desktop",
                width=1024,
                height=768,
                screenshot_path=str(rel_path).replace("\\", "/"),
                dom_path=f"/html/body/div[{i}]",
                load_time=0.12 * i,
                captured_at=datetime.utcnow(),
            )
            db.add(shot)
            db.flush()

            # Perception
            perception = Perception(
                session_id=sess.id,
                screenshot_id=shot.id,
                anomaly_score=0.1 * i,
                caption=f"A synthetic caption for screenshot {i}",
                observation_json=json.dumps({"note": f"obs {i}"}),
            )
            db.add(perception)
            db.flush()

            # Issue
            issue = Issue(
                session_id=sess.id,
                screenshot_id=shot.id,
                perception_id=perception.id,
                issue_class="ui",
                severity="low" if i == 1 else "medium" if i == 2 else "high",
                schema_severity="minor",
                issue_type="visual",
                recommended_action="fix_css",
                title=f"Demo issue {i}",
                description=f"This is a demo issue generated for screenshot {i}.",
                structured_report_json=json.dumps({"issue": f"demo {i}"}, ensure_ascii=False),
                annotation_json=json.dumps({"severity": "low"}),
            )
            db.add(issue)
            db.flush()

            shots.append((shot, perception, issue))

        # Add an action with LLM analysis
        action = Action(
            session_id=sess.id,
            sequence_number=1,
            action_type="click",
            target_element="#submit",
            before_screenshot_path=shots[0][0].screenshot_path,
            after_screenshot_path=shots[1][0].screenshot_path,
            timestamp=datetime.utcnow(),
            metadata_json=json.dumps({"info": "demo action"}),
        )
        db.add(action)
        db.flush()

        llm = LLMAnalysis(
            action_id=action.id,
            analysis_type="comparison",
            prompt_used="Compare before/after",
            llm_response="{\"result\": \"minor regressions found\"}",
            status="WARNING",
            issues_found=json.dumps([{"id": shots[1][2].id, "note": "demo"}]),
            model_used="demo-model",
            elapsed_seconds=1.23,
        )
        db.add(llm)

        db.commit()

        print(f"Created demo session with id={sess.id}")

    finally:
        db.close()


if __name__ == "__main__":
    main()
