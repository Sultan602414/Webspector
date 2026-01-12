from __future__ import annotations

from datetime import datetime
from typing import Any, Dict, Optional

from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, String, Text, create_engine
from sqlalchemy.orm import declarative_base, relationship, scoped_session, sessionmaker, Session


Base = declarative_base()
_engine = None
_SessionLocal: Optional[scoped_session] = None


class TestSession(Base):
    __tablename__ = "test_sessions"

    id = Column(Integer, primary_key=True)
    url = Column(String(500), nullable=False)
    depth = Column(Integer, default=1, nullable=False)
    label = Column(String(200))
    status = Column(String(50), default="running", nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    completed_at = Column(DateTime)
    metadata_json = Column(Text)

    screenshots = relationship("Screenshot", back_populates="session", cascade="all, delete-orphan")
    perceptions = relationship("Perception", back_populates="session", cascade="all, delete-orphan")
    issues = relationship("Issue", back_populates="session", cascade="all, delete-orphan")
    actions = relationship("Action", back_populates="session", cascade="all, delete-orphan")


class Action(Base):
    """Individual action performed during testing (click, scroll, etc)."""
    __tablename__ = "actions"
    
    id = Column(Integer, primary_key=True)
    session_id = Column(Integer, ForeignKey("test_sessions.id"), nullable=False)
    sequence_number = Column(Integer, nullable=False)  # Order in test sequence
    action_type = Column(String(50), nullable=False)  # scroll, click_nav, form_fill, etc
    target_element = Column(String(500))  # What was clicked/interacted with
    before_screenshot_path = Column(String(500))
    after_screenshot_path = Column(String(500))
    timestamp = Column(DateTime, default=datetime.utcnow, nullable=False)
    metadata_json = Column(Text)  # Additional action-specific data
    
    session = relationship("TestSession", back_populates="actions")
    llm_analysis = relationship("LLMAnalysis", back_populates="action", uselist=False, cascade="all, delete-orphan")


class LLMAnalysis(Base):
    """LLM analysis of screenshots and actions."""
    __tablename__ = "llm_analyses"
    
    id = Column(Integer, primary_key=True)
    action_id = Column(Integer, ForeignKey("actions.id"), nullable=False)
    analysis_type = Column(String(50), nullable=False)  # 'screenshot', 'comparison', 'report'
    prompt_used = Column(Text)  # The prompt sent to LLM
    llm_response = Column(Text, nullable=False)  # Raw LLM response
    status = Column(String(20))  # PASS, FAIL, WARNING, ERROR
    issues_found = Column(Text)  # JSON list of issues
    model_used = Column(String(100))  # e.g., 'llava:13b'
    elapsed_seconds = Column(Float)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    action = relationship("Action", back_populates="llm_analysis")


class Screenshot(Base):
    __tablename__ = "screenshots"

    id = Column(Integer, primary_key=True)
    session_id = Column(Integer, ForeignKey("test_sessions.id"), nullable=False)
    url = Column(String(500), nullable=False)
    viewport_name = Column(String(50), nullable=False)
    width = Column(Integer, nullable=False)
    height = Column(Integer, nullable=False)
    screenshot_path = Column(String(500), nullable=False)
    dom_path = Column(String(500))
    load_time = Column(Float)
    captured_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    session = relationship("TestSession", back_populates="screenshots")
    perception = relationship("Perception", back_populates="screenshot", uselist=False)
    issues = relationship("Issue", back_populates="screenshot")


class Perception(Base):
    __tablename__ = "perceptions"

    id = Column(Integer, primary_key=True)
    session_id = Column(Integer, ForeignKey("test_sessions.id"), nullable=False)
    screenshot_id = Column(Integer, ForeignKey("screenshots.id"), nullable=False)
    anomaly_score = Column(Float, nullable=False)
    caption = Column(Text)
    observation_json = Column(Text, nullable=False)

    session = relationship("TestSession", back_populates="perceptions")
    screenshot = relationship("Screenshot", back_populates="perception")
    issues = relationship("Issue", back_populates="perception")


class Issue(Base):
    __tablename__ = "issues"

    id = Column(Integer, primary_key=True)
    session_id = Column(Integer, ForeignKey("test_sessions.id"), nullable=False)
    screenshot_id = Column(Integer, ForeignKey("screenshots.id"), nullable=False)
    perception_id = Column(Integer, ForeignKey("perceptions.id"), nullable=False)

    issue_class = Column(String(50), nullable=False)
    severity = Column(String(20), nullable=False)
    schema_severity = Column(String(20), nullable=False)
    issue_type = Column(String(50), nullable=False)
    recommended_action = Column(String(50), nullable=False)

    title = Column(String(500), nullable=False)
    description = Column(Text, nullable=False)

    structured_report_json = Column(Text, nullable=False)
    annotation_json = Column(Text, nullable=False)

    session = relationship("TestSession", back_populates="issues")
    screenshot = relationship("Screenshot", back_populates="issues")
    perception = relationship("Perception", back_populates="issues")


def init_engine(database_url: str) -> None:
    global _engine, _SessionLocal
    _engine = create_engine(database_url, future=True)
    _SessionLocal = scoped_session(
        sessionmaker(bind=_engine, autoflush=False, autocommit=False, expire_on_commit=False)
    )


def get_engine():  # type: ignore[override]
    if _engine is None:
        raise RuntimeError("Database engine is not initialized. Call init_engine() first.")
    return _engine


def get_session() -> Session:
    if _SessionLocal is None:
        raise RuntimeError("Database session factory is not initialized. Call init_engine() first.")
    return _SessionLocal()


def init_db() -> None:
    if _engine is None:
        raise RuntimeError("Database engine is not initialized. Call init_engine() first.")
    Base.metadata.create_all(bind=_engine)


def to_dict_issue(issue: Issue) -> Dict[str, Any]:
    return {
        "id": issue.id,
        "session_id": issue.session_id,
        "screenshot_id": issue.screenshot_id,
        "perception_id": issue.perception_id,
        "issue_class": issue.issue_class,
        "severity": issue.severity,
        "schema_severity": issue.schema_severity,
        "issue_type": issue.issue_type,
        "recommended_action": issue.recommended_action,
        "title": issue.title,
        "description": issue.description,
    }


def to_dict_screenshot(shot: Screenshot) -> Dict[str, Any]:
    return {
        "id": shot.id,
        "session_id": shot.session_id,
        "url": shot.url,
        "viewport_name": shot.viewport_name,
        "width": shot.width,
        "height": shot.height,
        "screenshot_path": shot.screenshot_path,
        "dom_path": shot.dom_path,
        "load_time": shot.load_time,
        "captured_at": shot.captured_at.isoformat() if shot.captured_at else None,
    }


def to_dict_session(sess: TestSession, issue_count: Optional[int] = None, screenshot_count: Optional[int] = None) -> Dict[str, Any]:
    return {
        "id": sess.id,
        "url": sess.url,
        "depth": sess.depth,
        "label": sess.label,
        "status": sess.status,
        "created_at": sess.created_at.isoformat() if sess.created_at else None,
        "completed_at": sess.completed_at.isoformat() if sess.completed_at else None,
        "issue_count": issue_count,
        "screenshot_count": screenshot_count,
    }
