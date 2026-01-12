from __future__ import annotations

from datetime import datetime
from pathlib import Path
from typing import Any

import pytest

from dashboard.app import create_app
from dashboard import db as db_module


@pytest.mark.integration
def test_run_endpoint_persists_session_and_issues(tmp_path: Path, monkeypatch: Any) -> None:
    db_path = tmp_path / "dashboard.db"
    captures_root = tmp_path

    app = create_app(
        {
            "TESTING": True,
            "DATABASE_URL": f"sqlite:///{db_path}",
            "CAPTURES_ROOT": str(captures_root),
            "DASHBOARD_TOKEN": "test-token",
        }
    )

    def fake_execute_full_run(url: str, depth: int, out_dir: Path, db, test_session) -> None:  # type: ignore[override]
        # Stub pipeline: create a single screenshot, perception, and issue without launching a browser.
        from dashboard.db import Issue, Perception, Screenshot

        root = Path(out_dir).parent
        screenshot_rel = "dummy.png"
        (root / screenshot_rel).write_bytes(b"")

        screenshot = Screenshot(
            session_id=test_session.id,
            url=url,
            viewport_name="desktop",
            width=1366,
            height=768,
            screenshot_path=screenshot_rel,
            dom_path=None,
            load_time=1.0,
            captured_at=datetime.utcnow(),
        )
        db.add(screenshot)
        db.flush()

        perception = Perception(
            session_id=test_session.id,
            screenshot_id=screenshot.id,
            anomaly_score=0.5,
            caption="dummy",
            observation_json="{}",
        )
        db.add(perception)
        db.flush()

        issue = Issue(
            session_id=test_session.id,
            screenshot_id=screenshot.id,
            perception_id=perception.id,
            issue_class="UI",
            severity="medium",
            schema_severity="major",
            issue_type="layout",
            recommended_action="retest",
            title="Dummy issue",
            description="Dummy description",
            structured_report_json="{}",
            annotation_json="{}",
        )
        db.add(issue)
        db.commit()

    monkeypatch.setattr("dashboard.app.execute_full_run", fake_execute_full_run)

    client = app.test_client()

    resp = client.post("/run", json={"url": "https://example.com", "depth": 1}, headers={"X-API-Token": "test-token"})
    assert resp.status_code == 200
    data = resp.get_json()
    assert data is not None
    session_id = data["session_id"]

    resp = client.get("/sessions", headers={"X-API-Token": "test-token", "Accept": "application/json"})
    assert resp.status_code == 200
    sessions = resp.get_json()
    assert isinstance(sessions, list)
    assert any(s["id"] == session_id for s in sessions)

    resp = client.get(
        f"/session/{session_id}",
        headers={"X-API-Token": "test-token", "Accept": "application/json"},
    )
    assert resp.status_code == 200
    detail = resp.get_json()
    assert "session" in detail and "issues" in detail and "screenshots" in detail
    assert detail["issues"]
    assert detail["screenshots"]

    issue_id = detail["issues"][0]["id"]
    resp = client.get(
        f"/issue/{issue_id}",
        headers={"X-API-Token": "test-token", "Accept": "application/json"},
    )
    assert resp.status_code == 200
    issue_detail = resp.get_json()
    assert issue_detail["id"] == issue_id
    assert issue_detail["annotation"] is not None

    resp = client.get(
        f"/session/{session_id}/export/csv",
        headers={"X-API-Token": "test-token"},
    )
    assert resp.status_code == 200
    assert resp.mimetype == "text/csv"
