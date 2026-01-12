"""Demo script showing the complete LLM-powered QA workflow.

This demonstrates:
1. Action-level screenshot capture
2. LLM analysis of each action
3. Comprehensive report generation
"""

from pathlib import Path
from datetime import datetime

# Database setup
from dashboard.db import init_engine, init_db, TestSession, get_session

# Browser and crawler
from web_interaction.browser_driver import PlaywrightBrowserDriver
from web_interaction.crawler_llm import crawl_site_with_llm

# Report generation
from cognitive_reasoning.report_generator import ComprehensiveReportGenerator


def demo_llm_qa_workflow(test_url: str = "https://www.example.com"):
    """Run complete LLM-powered QA workflow demo.
    
    Args:
        test_url: URL to test
    """
    print("=" * 60)
    print("LLM-Powered QA Agent Demo")
    print("=" * 60)
    
    # Step 1: Setup database
    print("\n[Step 1] Initializing database...")
    init_engine("sqlite:///dashboard.db")
    init_db()
    
    # Step 2: Create test session
    print(f"\n[Step 2] Creating test session for: {test_url}")
    db = get_session()
    try:
        session = TestSession(
            url=test_url,
            depth=1,
            label="LLM Demo Test",
            status="running"
        )
        db.add(session)
        db.commit()
        db.refresh(session)
        session_id = session.id
        print(f"[Session] Created session #{session_id}")
    finally:
        db.close()
    
    # Step 3: Run crawler with LLM analysis
    print(f"\n[Step 3] Running crawler with LLM analysis...")
    print("[Info] This will:")
    print("  - Capture screenshots before/after each action")
    print("  - Analyze each action with LLaVA vision model")
    print("  - Store findings in database")
    
    out_dir = Path(f"captures/session_{session_id}")
    out_dir.mkdir(parents=True, exist_ok=True)
    
    try:
        with PlaywrightBrowserDriver(headless=True) as driver:
            captures = crawl_site_with_llm(
                url=test_url,
                depth=1,
                out_dir=out_dir,
                driver=driver,
                session_id=session_id,
                enable_llm=True  # Enable LLM analysis
            )
        
        print(f"\n[Crawler] Completed! Captured {len(captures)} viewports")
        
        # Update session status
        db = get_session()
        try:
            session = db.query(TestSession).get(session_id)
            session.status = "completed"
            session.completed_at = datetime.utcnow()
            db.commit()
        finally:
            db.close()
            
    except Exception as e:
        print(f"\n[Error] Crawler failed: {e}")
        import traceback
        traceback.print_exc()
        
        # Mark session as failed
        db = get_session()
        try:
            session = db.query(TestSession).get(session_id)
            session.status = "failed"
            db.commit()
        finally:
            db.close()
        return
    
    # Step 4: Generate comprehensive report
    print(f"\n[Step 4] Generating comprehensive QA report...")
    
    generator = ComprehensiveReportGenerator()
    report = generator.generate_report(session_id)
    
    # Display report summary
    print("\n" + "=" * 60)
    print("REPORT SUMMARY")
    print("=" * 60)
    print(report['executive_summary']['text'])
    
    print(f"\nTotal Actions Analyzed: {report['statistics']['total_actions']}")
    print(f"LLM Analyses: {report['statistics']['llm_analyses']}")
    
    # Show some findings
    print("\n" + "-" * 60)
    print("RECENT ACTIONS:")
    print("-" * 60)
    for entry in report['test_execution']['timeline'][:5]:
        print(f"\n{entry['step']}. {entry['action']} - {entry['status']}")
        print(f"   Target: {entry['target']}")
        if 'analysis' in entry:
            print(f"   Analysis: {entry['analysis'][:100]}...")
    
    # Export report
    print(f"\n[Step 5] Exporting report...")
    markdown_report = generator.export_as_markdown(report)
    
    report_path = out_dir / "comprehensive_report.md"
    report_path.write_text(markdown_report, encoding='utf-8')
    print(f"[Report] Saved to: {report_path}")
    
    # Save JSON report too
    import json
    json_report_path = out_dir / "report.json"
    json_report_path.write_text(json.dumps(report, indent=2), encoding='utf-8')
    print(f"[Report] JSON saved to: {json_report_path}")
    
    print("\n" + "=" * 60)
    print("DEMO COMPLETE!")
    print("=" * 60)
    print(f"\nView your report at: {report_path}")
    print(f"View in dashboard: http://localhost:5000/session/{session_id}")
    print("\nNext steps:")
    print("  1. Install Ollama: https://ollama.com/download/windows")
    print("  2. Pull models: ollama pull llava:13b")
    print("  3. Run this demo again with LLM enabled!")


if __name__ == "__main__":
    import sys
    
    # Get URL from command line or use default
    test_url = sys.argv[1] if len(sys.argv) > 1 else "https://www.example.com"
    
    print("\nWARNING: LLM analysis requires:")
    print("  1. Ollama installed")
    print("  2. LLaVA model pulled (ollama pull llava:13b)")
    print("  3. Ollama running in background")
    print("\nWithout these, the demo will run but skip LLM analysis.")
    input("\nPress Enter to continue...")
    
    demo_llm_qa_workflow(test_url)
