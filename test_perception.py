from dashboard.app import create_app
from pathlib import Path

def test_perception():
    """Test the perception pipeline on existing captures"""
    from perception.perception import PerceptionPipeline
    from cognitive_reasoning import analyze_and_plan
    
    app = create_app()
    
    with app.app_context():
        try:
            print("Creating perception pipeline...")
            pipeline = PerceptionPipeline(enable_captioning=False, enable_ocr=False, enable_clip=False)
            
            print("Finding screenshot...")
            screenshot_path = Path("./captures/test_manual/screenshots/desktop/0003.png")
            
            if not screenshot_path.exists():
                print(f"Screenshot not found at {screenshot_path}")
                return
            
            print(f"Analyzing screenshot: {screenshot_path}")
            observation = pipeline.analyze_screenshot(screenshot_path)
            
            print("Converting to JSON...")
            obs_json = observation.to_json()
            obs_json["url"] = "https://example.com"
            obs_json["viewport"] = {"name": "desktop", "width": 1920, "height": 1080}
            
            print("Running cognitive reasoning...")
            structured, _ = analyze_and_plan(obs_json)
            
            print("\nSUCCESS!")
            print(f"Issue class: {structured['issue_class']}")
            print(f"Severity: {structured['severity']}")
            print(f"Bug report title: {structured['bug_report']['title']}")
            
        except Exception as e:
            print(f"\nERROR: {type(e).__name__}: {e}")
            import traceback
            traceback.print_exc()

if __name__ == "__main__":
    test_perception()
