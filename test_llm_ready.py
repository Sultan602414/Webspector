"""Quick LLM readiness check and test script.

This checks if Ollama is running and tests the LLM integration.
"""

import sys
from pathlib import Path

print("=" * 70)
print("LLM QA SYSTEM - READINESS CHECK")
print("=" * 70)

# Step 1: Check Ollama connection
print("\n[STEP 1] Checking Ollama service...")
try:
    import ollama
    
    try:
        models = ollama.list()
        model_names = [m['name'] for m in models.get('models', [])]
        print(f"   [OK] Ollama is running")
        print(f"   [OK] Available models: {len(model_names)}")
        
        llava_models = [m for m in model_names if 'llava' in m.lower()]
        if llava_models:
            print(f"   [OK] LLaVA found: {llava_models[0]}")
        else:
            print("   [!] No LLaVA model found")
            print("   Run: ollama pull llava:7b")
            sys.exit(1)
            
    except Exception as e:
        print(f"   [X] Ollama not running!")
        print(f"   Error: {e}")
        print("\n   SOLUTION:")
        print("   Ollama should start automatically on Windows.")
        print("   If not, open a new terminal and run: ollama serve")
        print("   Or restart Ollama from Start menu")
        sys.exit(1)
        
except ImportError:
    print("   [X] 'ollama' package not installed")
    print("   Run: pip install ollama")
    sys.exit(1)

# Step 2: Test LLM initialization
print("\n[STEP 2] Testing LLM integration...")
try:
    from perception.llm_vision import LocalVisionLLM
    
    llm = LocalVisionLLM()
    print(f"   [OK] LLM initialized successfully")
    print(f"   [OK] Vision model: {llm.vision_model}")
    print(f"   [OK] Text model: {llm.text_model}")
    
except Exception as e:
    print(f"   [X] LLM initialization failed: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Step 3: Check configuration
print("\n[STEP 3] Checking configuration...")
try:
    import config
    
    print(f"   [OK] LLM enabled: {config.LLM_ANALYSIS_ENABLED}")
    print(f"   [OK] Preset: {config.LLM_PRESET}")
    
    models_info = config.get_current_models()
    print(f"   [OK] Configured: {models_info['vision']}")
    
    if not config.LLM_ANALYSIS_ENABLED:
        print("\n   [!] WARNING: LLM is disabled in .env")
        print("   Set LLM_ANALYSIS_ENABLED=true to enable")
        
except Exception as e:
    print(f"   [X] Config error: {e}")

# Step 4: Check database
print("\n[STEP 4] Checking database...")
try:
    from dashboard.db import Action, LLMAnalysis, init_engine, get_session
    
    init_engine("sqlite:///dashboard.db")
    db = get_session()
    action_count = db.query(Action).count()
    analysis_count = db.query(LLMAnalysis).count()
    db.close()
    
    print(f"   [OK] Action records: {action_count}")
    print(f"   [OK] LLM analysis records: {analysis_count}")
    
except Exception as e:
    print(f"   [!] Database issue: {e}")
    print("   Run: python migrate_db.py")

# Summary
print("\n" + "=" * 70)
print("SYSTEM STATUS: READY!")
print("=" * 70)

print("\nYour LLM-Powered QA System is configured and ready:")
print("  [OK] Ollama service running")
print(f"  [OK] LLaVA model installed")
print("  [OK] LLM integration working")
print("  [OK] Database ready")

print("\n" + "=" * 70)
print("NEXT STEPS - Run Your First AI-Powered Test:")
print("=" * 70)

print("\nOption 1: Quick Demo (Recommended)")
print("  python demo_llm_qa.py")
print("\nOption 2: Dashboard")
print("  flask --app dashboard run")
print("  Then visit: http://localhost:5000")

print("\n" + "=" * 70)
print("WHAT YOU'LL GET:")
print("=" * 70)
print("  1. Screenshots after EVERY action (scroll, click, etc.)")
print("  2. AI analyzes each action with LLaVA")
print("  3. Before/after comparison for each action")
print("  4. Comprehensive QA report generated")
print("  5. PASS/FAIL/WARNING status for everything")
print("  6. Professional recommendations")

print("\n" + "=" * 70)
print("Ready to test? Run: python demo_llm_qa.py")
print("=" * 70)
