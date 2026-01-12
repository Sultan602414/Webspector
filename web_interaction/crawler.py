import json
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List

from web_interaction.browser_driver import PlaywrightBrowserDriver


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


def crawl_site(url: str, depth: int, out_dir: Path, driver: PlaywrightBrowserDriver) -> List[CaptureMetadata]:
    out_dir = Path(out_dir)
    captures: List[CaptureMetadata] = []

    for base in ("screenshots", "dom", "metadata"):
        (out_dir / base).mkdir(parents=True, exist_ok=True)

    index = 1

    for viewport in VIEWPORTS:
        page, context, load_time, network_requests = driver.open_page(url, viewport)
        try:
            driver.perform_basic_actions(page, depth=depth)
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

    index_path = out_dir / "metadata_index.json"
    index_path.write_text(json.dumps([asdict(c) for c in captures], indent=2), encoding="utf-8")

    return captures
