from playwright.sync_api import sync_playwright
try:
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        print("Playwright Chromium is INSTALLED and working.")
        browser.close()
except Exception as e:
    print(f"Playwright ERROR: {e}")
