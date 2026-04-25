from __future__ import annotations

import csv
import json
import os
from datetime import datetime
from functools import wraps
from io import BytesIO, StringIO
from pathlib import Path
from typing import Any, Dict, List

from flask import (
    Flask,
    abort,
    current_app,
    jsonify,
    redirect,
    render_template,
    request,
    send_file,
    url_for,
)

from sqlalchemy.orm import joinedload

from dashboard.db import (

    Issue,
    Perception,
    Screenshot,
    TestSession,
    get_session,
    init_db,
    init_engine,
    to_dict_issue,
    to_dict_screenshot,
    to_dict_session,
)


try:  # optional PDF export
    from weasyprint import HTML  # type: ignore
except Exception:  # pragma: no cover
    HTML = None  # type: ignore


def create_app(test_config: Dict[str, Any] | None = None) -> Flask:
    app = Flask(__name__, template_folder="templates", static_folder="static")

    project_root = Path(__file__).resolve().parents[1]
    default_db = f"sqlite:///{project_root / 'dashboard.db'}"

    app.config.update(
        DATABASE_URL=os.getenv("DASHBOARD_DATABASE_URL", default_db),
        DASHBOARD_TOKEN=os.getenv("DASHBOARD_TOKEN", ""),
        CAPTURES_ROOT=str(project_root / "captures"),
    )
    if test_config:
        app.config.update(test_config)

    init_engine(app.config["DATABASE_URL"])
    init_db()

    def require_token(view_func):
        @wraps(view_func)
        def wrapped(*args, **kwargs):
            expected = current_app.config.get("DASHBOARD_TOKEN") or ""
            if expected:
                token = request.headers.get("X-API-Token") or request.args.get("token")
                if token != expected:
                    abort(401)
            return view_func(*args, **kwargs)

        return wrapped

    @app.route("/")
    @require_token
    def index() -> Any:
        return redirect(url_for("dashboard_home", token=current_app.config.get("DASHBOARD_TOKEN", "")))

    @app.route("/dashboard", methods=["GET"])
    @require_token
    def dashboard_home() -> Any:
        """Dashboard home page - API only."""
        return jsonify({"message": "Use the React frontend on port 5173", "status": "active"})

    @app.route("/run-test", methods=["GET"])
    @require_token
    def run_test_page() -> Any:
        """Run test page - API only."""
        return jsonify({"message": "Use the React frontend on port 5173", "status": "active"})


    @app.route("/sessions", methods=["GET"])
    @require_token
    def list_sessions() -> Any:
        db = get_session()
        try:
            sessions = db.query(TestSession).order_by(TestSession.created_at.desc()).all()
            result: List[Dict[str, Any]] = []
            for sess in sessions:
                issue_count = db.query(Issue).filter(Issue.session_id == sess.id).count()
                screenshot_count = db.query(Screenshot).filter(Screenshot.session_id == sess.id).count()
                result.append(to_dict_session(sess, issue_count, screenshot_count))
        finally:
            db.close()

        return jsonify(result)

    @app.route("/session/<int:session_id>", methods=["GET"])
    @require_token
    def get_session_detail(session_id: int) -> Any:
        db = get_session()
        try:
            sess = db.query(TestSession).get(session_id)
            if not sess:
                abort(404)
            shots = db.query(Screenshot).filter(Screenshot.session_id == session_id).order_by(Screenshot.id).all()

            severity_filter = request.args.get("severity")
            q = db.query(Issue).filter(Issue.session_id == session_id)
            if severity_filter:
                q = q.filter(Issue.severity == severity_filter)
            issues = q.order_by(Issue.id).all()

            session_dict = to_dict_session(sess)
            screenshots_payload = [to_dict_screenshot(s) for s in shots]
            issues_payload = [to_dict_issue(i) for i in issues]
        finally:
            db.close()

        return jsonify(
            {
                "session": session_dict,
                "screenshots": screenshots_payload,
                "issues": issues_payload,
            }
        )

    @app.route("/issue/<int:issue_id>", methods=["GET"])
    @require_token
    def get_issue_detail(issue_id: int) -> Any:
        db = get_session()
        try:
            issue = db.query(Issue).get(issue_id)
            if not issue:
                abort(404)
            payload = to_dict_issue(issue)
            payload["structured_report"] = json.loads(issue.structured_report_json)
            payload["annotation"] = json.loads(issue.annotation_json)
        finally:
            db.close()

        return jsonify(payload)

    @app.route("/session/<int:session_id>/actions", methods=["GET"])
    @require_token
    def get_session_actions(session_id: int) -> Any:
        """Get action timeline for a session with LLM analyses."""
        from dashboard.db import Action, LLMAnalysis
        
        db = get_session()
        try:
            session = db.query(TestSession).get(session_id)
            if not session:
                abort(404)
            
            actions = db.query(Action).filter(
                Action.session_id == session_id
            ).order_by(Action.sequence_number).all()
            
            actions_data = []
            for action in actions:
                action_dict = {
                    'id': action.id,
                    'sequence_number': action.sequence_number,
                    'action_type': action.action_type,
                    'target_element': action.target_element,
                    'before_screenshot_path': action.before_screenshot_path,
                    'after_screenshot_path': action.after_screenshot_path,
                    'timestamp': action.timestamp.isoformat(),
                    'metadata': json.loads(action.metadata_json or '{}')
                }
                
                if action.llm_analysis:
                    action_dict['llm_analysis'] = {
                        'status': action.llm_analysis.status,
                        'response': action.llm_analysis.llm_response,
                        'issues': json.loads(action.llm_analysis.issues_found or '[]'),
                        'model': action.llm_analysis.model_used,
                        'elapsed_seconds': action.llm_analysis.elapsed_seconds
                    }
                
                actions_data.append(action_dict)
                
        finally:
            db.close()
        
        return jsonify({'session_id': session_id, 'actions': actions_data})

    @app.route("/session/<int:session_id>/llm-report", methods=["GET"])
    @require_token
    def get_llm_report(session_id: int) -> Any:
        """Get comprehensive LLM-generated report for a session."""
        from cognitive_reasoning.report_generator import ComprehensiveReportGenerator
        
        db = get_session()
        try:
            session = db.query(TestSession).get(session_id)
            if not session:
                abort(404)
        finally:
            db.close()
        
        # Generate report
        generator = ComprehensiveReportGenerator()
        report = generator.generate_report(session_id)
        
        return jsonify(report)

    @app.route("/screenshot/<int:screenshot_id>", methods=["GET"])
    def get_screenshot(screenshot_id: int) -> Any:
        # Note: auth can be enforced by including token as a query parameter in template-generated URLs.
        db = get_session()
        try:
            shot = db.query(Screenshot).get(screenshot_id)
            if not shot:
                abort(404)
        finally:
            db.close()

        root = Path(current_app.config["CAPTURES_ROOT"])
        file_path = root / shot.screenshot_path
        if not file_path.is_file():
            abort(404)
        return send_file(str(file_path))

    @app.route("/screenshot-file/<path:filepath>", methods=["GET"])
    def get_screenshot_file(filepath: str) -> Any:
        """Serve screenshot files from captures directory (for action screenshots)."""
        root = Path(current_app.config["CAPTURES_ROOT"])
        file_path = root / filepath
        
        # Security check: ensure file is within captures root
        try:
            file_path = file_path.resolve()
            root = root.resolve()
            if not str(file_path).startswith(str(root)):
                abort(403)
        except Exception:
            abort(404)
        
        if not file_path.is_file():
            abort(404)
        return send_file(str(file_path))

    @app.route("/session/<int:session_id>/export/csv", methods=["GET"])
    @require_token
    def export_session_csv(session_id: int) -> Any:
        db = get_session()
        try:
            sess = db.query(TestSession).get(session_id)
            if not sess:
                abort(404)
            # Eager load screenshots to avoid DetachedInstanceError
            issues = db.query(Issue).options(joinedload(Issue.screenshot)).filter(Issue.session_id == session_id).order_by(Issue.id).all()

            output = StringIO()
            writer = csv.writer(output)
            writer.writerow(
                [
                    "issue_id",
                    "session_id",
                    "url",
                    "issue_class",
                    "severity",
                    "schema_severity",
                    "issue_type",
                    "recommended_action",
                    "title",
                    "description",
                ]
            )
            for issue in issues:
                writer.writerow(
                    [
                        issue.id,
                        issue.session_id,
                        issue.screenshot.url if issue.screenshot else "",
                        issue.issue_class,
                        issue.severity,
                        issue.schema_severity,
                        issue.issue_type,
                        issue.recommended_action,
                        issue.title,
                        issue.description,
                    ]
                )

            output.seek(0)
            csv_bytes = output.getvalue().encode("utf-8")
            filename = f"session_{session_id}_report.csv"
            print(f"DEBUG: Exporting CSV for session {session_id}, size: {len(csv_bytes)}")
            return send_file(
                BytesIO(csv_bytes),
                mimetype="text/csv",
                as_attachment=True,
                download_name=filename,
            )

        finally:
            db.close()


    @app.route("/session/<int:session_id>/export/pdf", methods=["GET"])
    @require_token
    def export_session_pdf(session_id: int) -> Any:
        if HTML is None:
            abort(501, description="PDF export requires WeasyPrint to be installed.")

        db = get_session()
        try:
            sess = db.query(TestSession).get(session_id)
            if not sess:
                abort(404)
            issues = db.query(Issue).filter(Issue.session_id == session_id).order_by(Issue.id).all()
            shots = db.query(Screenshot).filter(Screenshot.session_id == session_id).order_by(Screenshot.id).all()
        finally:
            db.close()

        session_dict = to_dict_session(sess)
        screenshots_payload = [to_dict_screenshot(s) for s in shots]
        issues_payload = [to_dict_issue(i) for i in issues]

        html = render_template(
            "session_report.html",
            session=session_dict,
            screenshots=screenshots_payload,
            issues=issues_payload,
        )
        pdf_bytes = HTML(string=html, base_url=str(Path(current_app.root_path))).write_pdf()
        return send_file(
            bytes_to_file_stream(pdf_bytes),
            mimetype="application/pdf",
            as_attachment=True,
            download_name=f"session_{session_id}_report.pdf",
        )

    @app.route("/run", methods=["POST"])
    @require_token
    def trigger_run() -> Any:
        payload = request.get_json(silent=True) or {}
        url = payload.get("url") or request.form.get("url")
        depth = int(payload.get("depth") or request.form.get("depth") or 1)
        label = payload.get("label") or request.form.get("label")
        if not url:
            abort(400, description="Missing 'url' in request body.")

        db = get_session()
        try:
            sess = TestSession(url=url, depth=depth, label=label, status="running")
            db.add(sess)
            db.commit()
            db.refresh(sess)

            captures_root = Path(current_app.config["CAPTURES_ROOT"])
            out_dir = captures_root / f"session_{sess.id}"
            out_dir.mkdir(parents=True, exist_ok=True)

            execute_full_run(url=url, depth=depth, out_dir=out_dir, db=db, test_session=sess)

            sess.status = "completed"
            sess.completed_at = datetime.utcnow()
            db.commit()
        except Exception as exc:  # pragma: no cover - error path
            import traceback
            print(f"\n{'='*60}")
            print(f"ERROR in test execution:")
            print(f"URL: {url}")
            print(f"Error: {type(exc).__name__}: {exc}")
            print(f"{'='*60}")
            traceback.print_exc()
            print(f"{'='*60}\n")
            
            sess.status = "failed"
            db.commit()
            abort(500, description=str(exc))
        finally:
            db.close()

        return jsonify({"session_id": sess.id, "status": sess.status})

    return app


def execute_full_run(url: str, depth: int, out_dir: Path, db, test_session: TestSession) -> None:
    """Run crawler -> perception -> orchestrator and persist results.

    Split into a helper so tests can monkeypatch this function for faster runs.
    """

    from web_interaction.browser_driver import PlaywrightBrowserDriver
    from web_interaction.crawler import crawl_site
    from web_interaction.crawler_llm import crawl_site_with_llm
    from perception.perception import PerceptionPipeline
    from cognitive_reasoning import analyze_and_plan
    import config

    from dashboard.db import Issue, Perception, Screenshot

    pipeline = PerceptionPipeline(enable_captioning=False, enable_ocr=False, enable_clip=False)

    with PlaywrightBrowserDriver(headless=True) as driver:
        # Use LLM-powered crawler if enabled in config
        if config.LLM_ANALYSIS_ENABLED:
            print(f"[Dashboard] Using LLM-powered crawler with {config.get_current_models()['vision']}")
            captures = crawl_site_with_llm(
                url=url, 
                depth=depth, 
                out_dir=out_dir, 
                driver=driver,
                session_id=test_session.id,
                enable_llm=True
            )
        else:
            print("[Dashboard] Using standard crawler (LLM disabled)")
            captures = crawl_site(url=url, depth=depth, out_dir=out_dir, driver=driver)

    for meta in captures:
        screenshot_abs = out_dir / meta.screenshot_path
        observation = pipeline.analyze_screenshot(screenshot_abs)
        obs_json = observation.to_json()
        obs_json["url"] = meta.url
        obs_json["viewport"] = meta.viewport
        obs_json["dom_path"] = meta.dom_path

        structured, _ = analyze_and_plan(obs_json)
        annotation = structured["annotation"]

        captured_at = datetime.fromisoformat(meta.timestamp)

        # Store screenshot path relative to CAPTURES_ROOT, including the session folder,
        # so /screenshot can resolve it directly.
        rel_path = Path(f"session_{test_session.id}") / meta.screenshot_path
        screenshot = Screenshot(
            session_id=test_session.id,
            url=meta.url,
            viewport_name=meta.viewport.get("name", ""),
            width=int(meta.viewport.get("width", 0)),
            height=int(meta.viewport.get("height", 0)),
            screenshot_path=str(rel_path).replace("\\", "/"),
            dom_path=meta.dom_path,
            load_time=meta.load_time,
            captured_at=captured_at,
        )
        db.add(screenshot)
        db.flush()

        perception = Perception(
            session_id=test_session.id,
            screenshot_id=screenshot.id,
            anomaly_score=observation.anomaly_score,
            caption=observation.semantic_caption,
            observation_json=json.dumps(obs_json, ensure_ascii=False),
        )
        db.add(perception)
        db.flush()

        issue = Issue(
            session_id=test_session.id,
            screenshot_id=screenshot.id,
            perception_id=perception.id,
            issue_class=structured["issue_class"],
            severity=structured["severity"],
            schema_severity=annotation["severity"],
            issue_type=annotation["issue_type"],
            recommended_action=structured["recommended_action"],
            title=structured["bug_report"]["title"],
            description=structured["bug_report"]["description"],
            structured_report_json=json.dumps(structured, ensure_ascii=False),
            annotation_json=json.dumps(annotation, ensure_ascii=False),
        )
        db.add(issue)

    db.commit()


def _wants_json() -> bool:
    best = request.accept_mimetypes.best
    return best == "application/json" or request.args.get("format") == "json"


def bytes_to_file_stream(data: bytes):
    from io import BytesIO

    return BytesIO(data)
