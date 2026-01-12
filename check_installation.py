"""Installation verification script for LLM-powered QA agent (Windows-compatible).

Run this to verify that everything is installed and configured correctly.
"""

import sys
from pathlib import Path

print("=" * 60)
print("WebSpector LLM Installation Checker")
print("=" * 60)

errors = []
warnings = []
success = []

# Check 1: Python version
print("\n[1/7] Checking Python version...")
if sys.version_info >= (3, 10):
    success.append(f"[OK] Python {sys.version_info.major}.{sys.version_info.minor}")
else:
    errors.append(f"[X] Python {sys.version_info.major}.{sys.version_info.minor} (need 3.10+)")

# Check 2: Required packages
print("[2/7] Checking Python packages...")
required_packages = {
    'flask': 'Flask',
    'playwright': 'Playwright',
    'sqlalchemy': 'SQLAlchemy',
    'ollama': 'Ollama (for LLM)'
}

for module, name in required_packages.items():
    try:
        __import__(module)
        success.append(f"[OK] {name}")
    except ImportError:
        errors.append(f"[X] {name} - Run: pip install {module}")

# Check 3: Ollama
print("[3/7] Checking Ollama...")
try:
    import ollama
    models = ollama.list()
    success.append(f"[OK] Ollama is installed")
    
    # Check for LLaVA models
    model_names = [m['name'] for m in models.get('models', [])]
    llava_models = [m for m in model_names if 'llava' in m.lower()]
    
    if llava_models:
        success.append(f"[OK] LLaVA models found: {', '.join(llava_models[:3])}")
    else:
        warnings.append("[!] No LLaVA models found - Run: ollama pull llava:13b")
        
except Exception as e:
    errors.append(f"[X] Ollama not running - {str(e)}")
    warnings.append("  Install from: https://ollama.com/download/windows")

# Check 4: Database
print("[4/7] Checking database...")
db_path = Path("dashboard.db")
if db_path.exists():
    success.append(f"[OK] Database exists ({db_path})")
    
    # Check for new tables
    try:
        from dashboard.db import init_engine, get_session, Action, LLMAnalysis
        init_engine(f"sqlite:///{db_path}")
        db = get_session()
        
        action_count = db.query(Action).count()
        db.close()
        success.append(f"[OK] Action table exists ({action_count} actions)")
    except Exception as e:
        warnings.append(f"[!] Database might need migration: {e}")
        warnings.append("  Run: python migrate_db.py")
else:
    warnings.append(f"[!] Database not found - Will be created on first run")

# Check 5: Configuration
print("[5/7] Checking configuration...")
env_path = Path(".env")
if env_path.exists():
    success.append("[OK] .env file exists")
    
    # Check config settings
    try:
        import config
        models_info = config.get_current_models()
        success.append(f"[OK] LLM preset: {config.LLM_PRESET}")
        success.append(f"[OK] Vision model: {models_info['vision']}")
    except Exception as e:
        warnings.append(f"[!] Config error: {e}")
else:
    warnings.append("[!] .env file not found (using defaults)")

# Check 6: Project structure
print("[6/7] Checking project structure...")
required_files = [
    "config.py",
    "perception/llm_vision.py",
    "perception/action_processor.py",
    "web_interaction/crawler_llm.py",
    "cognitive_reasoning/report_generator.py",
    "dashboard/app.py",
    "demo_llm_qa.py"
]

for file in required_files:
    if Path(file).exists():
        success.append(f"[OK] {file}")
    else:
        errors.append(f"[X] Missing: {file}")

# Check 7: Playwright browsers
print("[7/7] Checking Playwright browsers...")
try:
    from playwright.sync_api import sync_playwright
    with sync_playwright() as p:
        browsers = []
        try:
            p.chromium.launch(headless=True).close()
            browsers.append("chromium")
        except:
            pass
        
        if browsers:
            success.append(f"[OK] Playwright browsers: {', '.join(browsers)}")
        else:
            warnings.append("[!] Playwright browsers not installed")
            warnings.append("  Run: python -m playwright install")
except Exception as e:
    errors.append(f"[X] Playwright error: {e}")

# Summary
print("\n" + "=" * 60)
print("SUMMARY")
print("=" * 60)

if success:
    print(f"\n[OK] SUCCESS ({len(success)} items):")
    for item in success[:10]:  # Show first 10
        print(f"  {item}")
    if len(success) > 10:
        print(f"  ... and {len(success) - 10} more")

if warnings:
    print(f"\n[!] WARNINGS ({len(warnings)} items):")
    for item in warnings:
        print(f"  {item}")

if errors:
    print(f"\n[X] ERRORS ({len(errors)} items):")
    for item in errors:
        print(f"  {item}")

print("\n" + "=" * 60)

if not errors and not warnings:
    print("[OK] PERFECT! Everything is installed correctly!")
    print("\nYou're ready to run:")
    print("  python demo_llm_qa.py")
    print("  OR")
    print("  flask --app dashboard run")
elif not errors:
    print("[OK] GOOD! Core features work, but there are some warnings.")
    print("\nYou can run tests, but consider addressing warnings.")
else:
    print("[X] ISSUES FOUND! Fix the errors above before running tests.")
    print("\nQuick fix commands:")
    print("  pip install ollama")
    print("  ollama pull llava:13b")
    print("  python migrate_db.py")

print("=" * 60)
print("\nFor detailed setup instructions, see: README_LLM.md")
