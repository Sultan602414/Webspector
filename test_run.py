from dashboard.app import create_app
from dashboard.db import get_session, TestSession
from pathlib import Path

def test_run_manually():
    """Try to run a test manually to see what error occurs"""
    app = create_app()
    
    with app.app_context():
        from web_interaction.browser_driver import PlaywrightBrowserDriver
        from web_interaction.crawler import crawl_site
        
        try:
            print("Creating browser driver...")
            with PlaywrightBrowserDriver(headless=True) as driver:
                print("Crawling site...")
                out_dir = Path("./captures/test_manual")
                out_dir.mkdir(parents=True, exist_ok=True)
                
                captures = crawl_site(
                    url="https://example.com",
                    depth=1,
                    out_dir=out_dir,
                    driver=driver
                )
                
                print(f"Success! Created {len(captures)} captures")
                
        except Exception as e:
            print(f"ERROR: {type(e).__name__}: {e}")
            import traceback
            traceback.print_exc()

if __name__ == "__main__":
    test_run_manually()
