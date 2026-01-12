"""Enhanced crawler with action-level screenshot capture and LLM analysis.

This is an enhanced version that captures screenshots after every action
and analyzes them with the LLM vision model.
"""

import json
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Optional

from web_interaction.browser_driver import PlaywrightBrowserDriver
from perception.action_processor import ActionProcessor


VIEWPORTS: List[Dict] = [
    {"name": "mobile", "width": 360, "height": 640, "is_mobile": True},
    {"name": "tablet", "width": 768, "height": 1024, "is_mobile": False},
    {"name": "desktop", "width": 1366, "height": 768, "is_mobile": False},
]


@dataclass
class CaptureMetadata:
    url: str
    timestamp: str
    viewport: Dict
    load_time: float
    network_requests: List[str]
    dom_snippet: str
    screenshot_path: str
    dom_path: str


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def crawl_site_with_llm(
    url: str,
    depth: int,
    out_dir: Path,
    driver: PlaywrightBrowserDriver,
    session_id: int,
    enable_llm: bool = True
) -> List[CaptureMetadata]:
    """Crawl site with action-level screenshots and LLM analysis.
    
    Args:
        url: URL to crawl
        depth: Depth of navigation
        out_dir: Output directory
        driver: Browser driver instance
        session_id: Database test session ID
        enable_llm: Whether to enable LLM analysis
    
    Returns:
        List of capture metadata
    """
    out_dir = Path(out_dir)
    captures: List[CaptureMetadata] = []
    
    # Create output directories
    for base in ("screenshots", "dom", "metadata", "actions"):
        (out_dir / base).mkdir(parents=True, exist_ok=True)
    
    # Create action processor
    action_processor = ActionProcessor(
        session_id=session_id,
        output_dir=out_dir,
        enable_llm=enable_llm
    )
    
    # Set the action callback on the driver
    driver.action_callback = action_processor.process_action
    
    index = 1
    
    for viewport in VIEWPORTS:
        page, context, load_time, network_requests = driver.open_page(url, viewport)
        try:
            # Perform actions (will trigger callbacks with screenshots)
            driver.perform_basic_actions(page, depth=depth)
            
            # Capture final state
            dom_html = driver.get_dom_snippet(page, max_chars=20000)
            timestamp = _now_iso()
            vp_name = viewport["name"]
            
            screenshot_rel = Path("screenshots") / vp_name / f"{index:04d}.png"
            dom_rel = Path("dom") / vp_name / f"{index:04d}.html"
            meta_rel = Path("metadata") / vp_name / f"{index:04d}.json"
            
            (out_dir / screenshot_rel).parent.mkdir(parents=True, exist_ok=True)
            (out_dir / dom_rel).parent.mkdir(parents=True, exist_ok=True)
            (out_dir / meta_rel).parent.mkdir(parents=True, exist_ok=True)
            
            page.screenshot(path=str(out_dir / screenshot_rel), full_page=True)
            (out_dir / dom_rel).write_text(dom_html, encoding="utf-8")
            
            meta = CaptureMetadata(
                url=page.url,
                timestamp=timestamp,
                viewport={"name": vp_name, "width": viewport["width"], "height": viewport["height"]},
                load_time=load_time,
                network_requests=network_requests,
                dom_snippet=dom_html,
                screenshot_path=str(screenshot_rel).replace("\\", "/"),
                dom_path=str(dom_rel).replace("\\", "/"),
            )
            captures.append(meta)
            (out_dir / meta_rel).write_text(json.dumps(asdict(meta), indent=2), encoding="utf-8")
            
            index += 1
        finally:
            context.close()
    
    # Save action summary
    summary = action_processor.get_summary()
    summary_path = out_dir / "actions" / "summary.json"
    summary_path.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    
    print(f"\n[Crawler] Completed with {summary['total_actions']} actions processed")
    if summary['llm_enabled']:
        print(f"[LLM] Analysis enabled with model: {action_processor.llm.vision_model if action_processor.llm else 'N/A'}")
    
    index_path = out_dir / "metadata_index.json"
    index_path.write_text(json.dumps([asdict(c) for c in captures], indent=2), encoding="utf-8")
    
    return captures


# Keep original crawler for backward compatibility
def crawl_site(url: str, depth: int, out_dir: Path, driver: PlaywrightBrowserDriver) -> List[CaptureMetadata]:
    """Original crawler without LLM analysis (for backward compatibility)."""
    from web_interaction.crawler import crawl_site as original_crawl
    return original_crawl(url, depth, out_dir, driver)
