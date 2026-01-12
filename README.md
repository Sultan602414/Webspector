# Autonomous Web UI Testing Agent

This repository implements the architecture described in `FYP_Proposal.pdf` for an **autonomous web application testing agent**. The agent interacts with real websites, perceives visual and functional issues, reasons about their impact, and reports them via a dashboard and structured artifacts.

Core success criteria (from `FYP_Proposal.pdf`):

- Autonomously explore and test target web flows.
- Achieve **≥80% bug detection coverage** on annotated test cases.
- Deliver **≥50% reduction in manual testing time** compared to a baseline QA process.

## Architecture Layers

- **Web Interaction** (`web_interaction/`)
- **Perception** (`perception/`)
- **Cognitive Reasoning** (`cognitive_reasoning/`)
- **Reporting** (`reporting/`)
- **Dashboard** (`dashboard/`)
- **Evaluation** (`evaluation/`)

See `design.md` for a more detailed mapping of modules, data flows, and formats.

## Getting Started

### Prerequisites

- Python **3.10+** installed
- Git (optional but recommended)

### Create and Activate Virtual Environment

On Windows (PowerShell):

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install --upgrade pip
pip install -r requirements.txt
python -m playwright install
```

On Unix-like shells (or Git Bash):

```bash
./setup_env.sh
```

### Project Layout

- `web_interaction/`: Browser automation, navigation policies, user flows.
- `perception/`: Screenshot capture, layout & visual analysis, DOM+image fusion.
- `cognitive_reasoning/`: LLM and rule-based reasoning over observations.
- `reporting/`: Bug objects, JSON/HTML reports, export utilities.
- `dashboard/`: Flask-based UI for inspecting runs and bug reports.
- `evaluation/`: Offline evaluation against ground-truth annotations.
- `data/test_sites.csv`: List of public sites, pages, and expected functionality.
- `data/annotation_schema.json`: JSON Schema for ground-truth bug annotations.

## Next Steps

- Implement concrete modules in each layer according to `design.md`.
- Add automated tests using `pytest`.
- Connect the dashboard to the reporting and evaluation outputs.
