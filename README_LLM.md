# WebSpector - LLM-Powered QA Agent 🤖

**AI-Powered Quality Assurance Testing with Action-Level Analysis**

WebSpector is an automated QA testing tool that uses **LLaVA vision models** to analyze websites like a human QA engineer. It captures screenshots after every action, analyzes them with AI, and generates comprehensive, professional QA reports.

---

## ✨ Features

- ✅ **Action-Level Screenshot Capture** - Screenshots before/after every scroll, click, form fill
- ✅ **AI Vision Analysis** - Uses LLaVA 7B/13B models to analyze each action
- ✅ **Comprehensive Reports** - Executive summary, findings, recommendations in Markdown
- ✅ **Pass/Fail/Warning Status** - Each action gets analyzed and scored
- ✅ **Beautiful Dashboard** - Web UI to view sessions, actions, and reports
- ✅ **GPU Accelerated** - Runs locally on your RTX GPU (no API costs!)
- ✅ **Professional Output** - Reports that match human QA engineer quality

---

## 🎯 What It Does

**Before (Standard Testing)**:
```
❌ Take 3 screenshots (mobile, tablet, desktop)
❌ Basic issue detection
❌ Manual review required
```

**After (LLM-Powered)**:
```
✅ Capture 30-50 screenshots (every action)
✅ AI analyzes each action in real-time
✅ Generate comprehensive QA report
✅ PASS/FAIL/WARNING for each interaction
✅ Professional recommendations
```

---

## 📋 Requirements

### Hardware
- **GPU**: NVIDIA RTX 3060 or better (8GB+ VRAM)
  - RTX 5070 Ti (16GB) ← Your GPU: **Perfect!**
  - RTX 4070/4080/4090 also work great
- **RAM**: 16GB+ system RAM recommended
- **Storage**: 10GB for models + test data

### Software
- **Python**: 3.10+ (you have 3.14 ✅)
- **Ollama**: For running LLaVA models locally
- **Windows/Linux/Mac**: All supported

---

## 🚀 Installation

### Step 1: Install Dependencies

```bash
cd c:\Users\Namal\Desktop\wind_project

# Install Python packages
pip install -r requirements.txt

# Install Playwright browsers
python -m playwright install
```

### Step 2: Install Ollama

**Windows**:
1. Download from: https://ollama.com/download/windows
2. Run installer
3. Restart terminal

**Verify Installation**:
```bash
ollama --version
```

### Step 3: Pull LLaVA Models

```bash
# For RTX 5070 Ti (16GB VRAM) - Recommended
ollama pull llava:13b

# Or for faster analysis (8GB VRAM)
ollama pull llava:7b

# Verify models
ollama list
```

### Step 4: Configure Environment

```bash
# Create .env file
copy .env.example .env

# Edit .env and set (optional):
LLM_PRESET=balanced  # Uses llava:13b (default)
# or
LLM_PRESET=fast      # Uses llava:7b
```

### Step 5: Initialize Database

```bash
python migrate_db.py
```

---

## 💻 Usage

### Method 1: Dashboard (Web UI)

```bash
# Start the dashboard
flask --app dashboard run

# Open browser
http://localhost:5000

# Run a test:
1. Click "Run Test"
2. Enter URL to test
3. Wait for completion
4. View action timeline and LLM report
```

**New Dashboard Features**:
- **Session Detail**: Original viewport screenshots + issues
- **Action Timeline**: Before/after for every action with LLM analysis
- **LLM Report**: Comprehensive QA report with executive summary

### Method 2: Demo Script

```bash
# Quick test
python demo_llm_qa.py

# Test specific URL
python demo_llm_qa.py https://www.wikipedia.org

# View report
notepad captures\session_X\comprehensive_report.md
```

### Method 3: Python API

```python
from pathlib import Path
from web_interaction.browser_driver import PlaywrightBrowserDriver
from web_interaction.crawler_llm import crawl_site_with_llm
from cognitive_reasoning.report_generator import ComprehensiveReportGenerator
from dashboard.db import init_engine, init_db, TestSession, get_session

# Setup
init_engine("sqlite:///dashboard.db")
init_db()

# Create session
db = get_session()
session = TestSession(url="https://example.com", status="running")
db.add(session)
db.commit()
session_id = session.id
db.close()

# Run test
with PlaywrightBrowserDriver(headless=True) as driver:
    captures = crawl_site_with_llm(
        url="https://example.com",
        depth=1,
        out_dir=Path(f"captures/session_{session_id}"),
        driver=driver,
        session_id=session_id,
        enable_llm=True
    )

# Generate report
generator = ComprehensiveReportGenerator()
report = generator.generate_report(session_id)
markdown = generator.export_as_markdown(report)

print(markdown)
```

---

## 📊 Dashboard Routes

| Route | Description |
|-------|-------------|
| `/` | Home page |
| `/run-test` | Start new test |
| `/sessions` | List all test sessions |
| `/session/<id>` | Session detail (original) |
| `/session/<id>/actions` | **NEW**: Action timeline with before/after |
| `/session/<id>/llm-report` | **NEW**: Comprehensive LLM report |
| `/session/<id>/export/csv` | Export issues as CSV |

---

## ⚙️ Configuration

### Model Presets

Edit `.env` or `config.py`:

```python
# Fast (7B model - 3-5 sec per action)
LLM_PRESET=fast

# Balanced (13B model - 6-8 sec per action) ← Default for RTX 5070 Ti
LLM_PRESET=balanced

# Best (34B model - requires 32GB+ VRAM)
LLM_PRESET=best
```

### Environment Variables

```bash
# LLM Settings
LLM_PRESET=balanced              # fast/balanced/best
LLM_ANALYSIS_ENABLED=true        # Enable/disable LLM
LLM_TEMPERATURE=0.2              # 0-1, lower = more consistent

# Report Settings
REPORT_DETAIL_LEVEL=comprehensive  # quick/standard/comprehensive
SCREENSHOT_QUALITY=high            # low/medium/high

# Dashboard
DASHBOARD_TOKEN=                  # Optional: Set for authentication
CAPTURES_ROOT=./captures          # Where screenshots are saved
```

---

## 📈 Performance

### Your Setup (RTX 5070 Ti, 16GB VRAM)

| Model | VRAM | Speed/Action | Quality | Recommended |
|-------|------|--------------|---------|-------------|
| llava:7b | 8GB | 3-5 sec | ⭐⭐⭐⭐ | Fast testing |
| **llava:13b** | **12GB** | **6-8 sec** | **⭐⭐⭐⭐⭐** | **Production** ✅ |
| llava:34b | 24GB | ❌ N/A | ⭐⭐⭐⭐⭐ | Too large |

### Typical Test

**Test**: 30 actions (scroll, click, navigate)
**Duration**: 
- Without LLM: ~30 seconds
- With LLM (13B): ~3-4 minutes  
**Cost**: $0 (runs locally!)

---

## 📝 Example Report Output

```markdown
# QA Test Report

## Executive Summary

**Website:** https://www.example.com  
**Overall Quality Score:** 95/100  
**Risk Level:** LOW

### Key Findings
- Total Actions: 12
- Passed: 11 (92%)
- Failed: 0
- Warnings: 1

---

## Test Execution Timeline

| Step | Action | Target | Status |
|------|--------|--------|--------|
| 1 | page_load | / | ✓ PASS |
| 2 | scroll | step 1/4 | ✓ PASS |
| 3 | click_nav | /about | ⚠ WARNING |
| 4 | scroll | step 2/4 | ✓ PASS |
...

---

## Issues Found

### MEDIUM (1 issue)
- **Action 3**: click_nav on /about
  Navigation worked but page load took longer than expected.
  Consider optimizing page load performance.

---

## Recommendations

1. **Priority 2**: Review and address 1 warning to improve UX
2. Overall website performance is good
```

---

## 🐛 Troubleshooting

### "ollama-python not installed"
```bash
pip install ollama
```

### "Model not found"
```bash
ollama pull llava:13b
ollama list  # Verify
```

### "Connection refused" (Ollama not running)
```bash
# Windows: Ollama should auto-start
# If not, run:
ollama serve
```

### "Out of memory" (GPU)
```bash
# Switch to 7B model
echo LLM_PRESET=fast > .env

# Or disable LLM temporarily
echo LLM_ANALYSIS_ENABLED=false > .env
```

### "No actions recorded"
- Your test session was run before LLM integration
- Re-run the test with LLM enabled
- Check `.env` has `LLM_ANALYSIS_ENABLED=true`

---

## 🏗️ Architecture

```
┌─────────────────┐
│ Browser Driver  │ → Performs actions (scroll, click)
└────────┬────────┘
         │ Captures screenshots before/after
         ↓
┌─────────────────┐
│ Action Processor│ → Saves screenshots to disk
└────────┬────────┘
         │ Sends to LLM
         ↓
┌─────────────────┐
│ LLM Vision      │ → Analyzes with LLaVA model
└────────┬────────┘
         │ Returns PASS/FAIL/WARNING
         ↓
┌─────────────────┐
│ Database        │ → Stores actions + analyses
└────────┬────────┘
         │ Aggregates findings
         ↓
┌─────────────────┐
│ Report Generator│ → Creates comprehensive report
└─────────────────┘
```

---

## 📁 Project Structure

```
wind_project/
├── config.py                    # Configuration and presets
├── dashboard/
│   ├── app.py                   # Flask application (✨ Updated)
│   ├── db.py                    # Database models (✨ Updated)
│   └── templates/
│       ├── action_timeline.html # ✨ NEW: Action timeline view
│       └── llm_report.html      # ✨ NEW: LLM report view
├── perception/
│   ├── llm_vision.py           # ✨ NEW: LLM vision analyzer
│   ├── action_processor.py     # ✨ NEW: Action processing
│   └── perception.py           # Original perception pipeline
├── web_interaction/
│   ├── browser_driver.py       # ✨ Updated: Action callbacks
│   ├── crawler.py              # Original crawler
│   └── crawler_llm.py          # ✨ NEW: LLM-powered crawler
├── cognitive_reasoning/
│   ├── agent_orchestrator.py   # Original reasoning
│   └── report_generator.py     # ✨ NEW: Report generator
├── demo_llm_qa.py              # ✨ NEW: Demo script
├── migrate_db.py               # ✨ NEW: Database migration
└── requirements.txt            # ✨ Updated: Added ollama
```

---

## 🎓 How It Works

### 1. Test Execution
```python
driver = PlaywrightBrowserDriver(
    action_callback=processor.process_action  # NEW!
)
driver.scroll_page()  # Captures before/after automatically
```

### 2. Action Processing
```python
# For each action:
1. Save before screenshot
2. Perform action (scroll/click/etc)
3. Save after screenshot
4. Send to LLM for analysis
5. Store results in database
```

### 3. LLM Analysis
```python
llm.compare_before_after(
    before_screenshot="before.png",
    after_screenshot="after.png",
    action="scroll step 1/4"
)
# Returns: {status: "PASS", analysis: "Page scrolled correctly..."}
```

### 4. Report Generation
```python
# Aggregates all actions + analyses
generator.generate_report(session_id)
# Creates: Executive summary, timeline, issues, recommendations
```

---

## 🚦 Status Codes

- **PASS** ✓ - Action worked correctly, no issues found
- **WARNING** ⚠️ - Action worked but has minor issues or concerns
- **FAIL** ✗ - Action failed or caused errors
- **ERROR** - LLM analysis failed (technical issue)
- **NO_LLM** - Action was recorded but not analyzed (LLM disabled)

---

## 💡 Tips

1. **First Time Setup**: Run demo script first to verify installation
2. **Faster Testing**: Use `fast` preset (llava:7b) during development
3. **Production**: Switch to `balanced` preset (llava:13b) for final reports
4. **Large Sites**: Reduce depth parameter to limit actions captured
5. **Screenshots**: Located in `captures/session_X/actions/`

---

## 🤝 Contributing

This is your custom QA agent! Customize the prompts in `perception/llm_vision.py` to match your testing needs.

---

## 📄 License

Private project - All rights reserved

---

## 🎯 Next Steps

1. ✅ **Install Ollama** - Download and install
2. ✅ **Pull Models** - `ollama pull llava:13b`
3. ✅ **Run Demo** - `python demo_llm_qa.py`
4. ✅ **Test Dashboard** - `flask --app dashboard run`
5. 🚀 **Start Testing!** - Replace manual QA with AI

---

**Ready to replace your QA team with AI? Let's go! 🚀**

Need help? Check the troubleshooting section or review the walkthrough.md file.
