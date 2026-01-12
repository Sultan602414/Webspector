from typing import Dict, List, Optional, Tuple

try:
    from playwright.sync_api import Browser, BrowserContext, Page, TimeoutError, sync_playwright
except ImportError as exc:
    raise ImportError(
        "playwright is required to use PlaywrightBrowserDriver. "
        "Install dependencies from requirements.txt and run `python -m playwright install`."
    ) from exc


class PlaywrightBrowserDriver:
    def __init__(
        self, 
        headless: bool = True, 
        browser_name: str = "chromium", 
        default_timeout_ms: int = 45000,
        action_callback=None
    ) -> None:
        self.headless = headless
        self.browser_name = browser_name
        self.default_timeout_ms = default_timeout_ms
        self.action_callback = action_callback
        self.action_sequence = []
        self._playwright = None
        self._browser: Optional[Browser] = None

    def __enter__(self) -> "PlaywrightBrowserDriver":
        self._playwright = sync_playwright().start()
        browser_type = getattr(self._playwright, self.browser_name)
        self._browser = browser_type.launch(headless=self.headless)
        return self

    def __exit__(self, exc_type, exc, tb) -> None:
        if self._browser is not None:
            self._browser.close()
        if self._playwright is not None:
            self._playwright.stop()

    def open_page(self, url: str, viewport: Dict) -> Tuple[Page, BrowserContext, float, List[str]]:
        assert self._browser is not None, "Browser not started. Use PlaywrightBrowserDriver as a context manager."

        context = self._browser.new_context(
            viewport={"width": viewport["width"], "height": viewport["height"]},
            device_scale_factor=viewport.get("device_scale_factor", 1),
            is_mobile=viewport.get("is_mobile", False),
        )
        page = context.new_page()
        page.set_default_timeout(self.default_timeout_ms)

        network_requests: List[str] = []

        def _on_request(request) -> None:
            try:
                network_requests.append(request.url)
            except Exception:
                pass

        page.on("request", _on_request)

        import time

        start = time.perf_counter()
        try:
            page.goto(url, wait_until="networkidle", timeout=self.default_timeout_ms)
        except TimeoutError:
            # Fallback for sites where "networkidle" never occurs; use a simpler condition.
            page.goto(url, wait_until="load", timeout=self.default_timeout_ms)
        load_time = time.perf_counter() - start

        return page, context, load_time, network_requests

    def get_dom_snippet(self, page: Page, max_chars: int = 20000) -> str:
        html = page.content()
        if len(html) > max_chars:
            return html[:max_chars]
        return html

    def scroll_page(self, page: Page, steps: int = 4, step_px: int = 500) -> None:
        from datetime import datetime
        for i in range(steps):
            if self.action_callback:
                before_screenshot = page.screenshot()
            
            page.mouse.wheel(0, step_px)
            page.wait_for_timeout(400)
            
            if self.action_callback:
                after_screenshot = page.screenshot()
                action_data = {
                    'type': 'scroll',
                    'target': f'step {i+1}/{steps}',
                    'before_screenshot': before_screenshot,
                    'after_screenshot': after_screenshot,
                    'timestamp': datetime.now().isoformat()
                }
                self.action_sequence.append(action_data)
                self.action_callback(action_data)

    def click_top_nav_links(self, page: Page, max_links: int = 3) -> None:
        from datetime import datetime
        selectors = ["nav a", "header a", "a[role='button']"]
        elements = []
        seen_hrefs = set()
        for selector in selectors:
            for el in page.query_selector_all(selector):
                href = el.get_attribute("href")
                if href and href not in seen_hrefs:
                    seen_hrefs.add(href)
                    elements.append((el, href))
        for i, (el, href) in enumerate(elements[:max_links]):
            try:
                if self.action_callback:
                    before_screenshot = page.screenshot()
                
                el.click()
                page.wait_for_timeout(800)
                
                if self.action_callback:
                    after_screenshot = page.screenshot()
                    action_data = {
                        'type': 'click_nav',
                        'target': href,
                        'before_screenshot': before_screenshot,
                        'after_screenshot': after_screenshot,
                        'timestamp': datetime.now().isoformat()
                    }
                    self.action_sequence.append(action_data)
                    self.action_callback(action_data)
            except Exception:
                continue

    def fill_simple_forms(self, page: Page, max_forms: int = 1, submit: bool = True) -> None:
        forms = page.query_selector_all("form")
        
        # If no forms found, treat the whole page as a form
        if not forms:
            # Create a dummy object that mimics a form element's query_selector_all
            class PageAsForm:
                def __init__(self, page: Page):
                    self.page = page
                def query_selector_all(self, selector: str):
                    return self.page.query_selector_all(selector)
                def query_selector(self, selector: str):
                    return self.page.query_selector(selector)
                def press(self, key: str):
                    return self.page.keyboard.press(key)
            
            forms = [PageAsForm(page)]
            max_forms = 1

        for form in forms[:max_forms]:
            try:
                # Find all interactive elements
                inputs = form.query_selector_all("input, textarea, select")
                
                for el in inputs:
                    tag_name = el.evaluate("el => el.tagName.toLowerCase()")
                    type_attr = (el.get_attribute("type") or "").lower()
                    id_attr = (el.get_attribute("id") or "").lower()
                    name_attr = (el.get_attribute("name") or "").lower()
                    placeholder = (el.get_attribute("placeholder") or "").lower()
                    
                    # Combine context for better matching
                    context = f"{id_attr} {name_attr} {placeholder}"
                    
                    if tag_name == "input":
                        if type_attr in ["text", "email", "tel", "password", "number", "url", "search"] or not type_attr:
                            value = "test"
                            if "full" in context and "name" in context or "name" in context:
                                value = "John Doe"
                            elif "email" in context:
                                value = "john.doe@example.com"
                            elif "phone" in context or "tel" in context:
                                value = "+15551234567"
                            elif "subject" in context:
                                value = "Inquiry about services"
                            elif "password" in context:
                                value = "P@ssword123!"
                            elif "zip" in context or "postal" in context:
                                value = "12345"
                            
                            el.fill(value)
                        elif type_attr in ["checkbox", "radio"]:
                            if not el.is_checked():
                                el.check()
                    elif tag_name == "textarea":
                        el.fill("This is a test message with more than ten characters to satisfy validation.")
                    elif tag_name == "select":
                        # Try to select the first non-empty option
                        options = el.query_selector_all("option")
                        selected = False
                        for opt in options:
                            val = opt.get_attribute("value")
                            if val and val.strip():
                                el.select_option(value=val)
                                selected = True
                                break
                        if not selected and len(options) > 1:
                            el.select_option(index=1)

                if submit:
                    submit_btn = form.query_selector("button[type='submit'], input[type='submit'], button:not([type])")
                    if submit_btn:
                        submit_btn.click()
                    else:
                        form.press("Enter")
                page.wait_for_timeout(1000)
            except Exception:
                continue

    def perform_basic_actions(self, page: Page, depth: int = 1) -> None:
        max_nav_clicks = max(1, depth)
        self.click_top_nav_links(page, max_links=max_nav_clicks)
        self.scroll_page(page)
        self.fill_simple_forms(page)
