import json
from pathlib import Path

import pytest

from web_interaction.browser_driver import PlaywrightBrowserDriver
from web_interaction.crawler import VIEWPORTS, crawl_site


@pytest.mark.integration
def test_crawl_creates_screenshots_dom_and_metadata(tmp_path: Path) -> None:
    url = "https://example.com"
    out_dir = tmp_path / "session"

    with PlaywrightBrowserDriver(headless=True) as driver:
        captures = crawl_site(url=url, depth=1, out_dir=out_dir, driver=driver)

    assert captures
    assert len(captures) == len(VIEWPORTS)

    for meta in captures:
        screenshot_file = out_dir / meta.screenshot_path
        assert screenshot_file.is_file()
        assert meta.dom_snippet
        assert "width" in meta.viewport and "height" in meta.viewport
        assert meta.url.startswith("https://example.com")

    index_path = out_dir / "metadata_index.json"
    assert index_path.is_file()
    data = json.loads(index_path.read_text(encoding="utf-8"))
    assert len(data) == len(captures)
