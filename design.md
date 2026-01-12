# Design: Autonomous Web UI Testing Agent

This document maps the implementation plan to the architecture described in `FYP_Proposal.pdf` and defines key data formats.

## Success Criteria (from FYP_Proposal.pdf)

The system is expected to:

- Operate with **high autonomy** over predefined web test scenarios.
- Reach **≥80% detection rate** on ground-truth annotated bugs.
- Achieve at least **50% reduction in manual testing time** compared to a baseline QA process.

These metrics will drive the design of evaluation datasets and experiments in the `evaluation/` layer.

## Architecture Overview

The system is organized into six primary layers, each with its own package.

### 1. Web Interaction Layer (`web_interaction/`)

**Responsibilities**

- Launch browsers and manage sessions (Playwright/Selenium).
- Navigate to URLs specified in `data/test_sites.csv`.
- Execute user flows: clicks, form submissions, scrolling, navigation.
- Capture DOM snapshots, network logs (optional), and screenshots for analysis.

**Planned modules** (to be implemented later)

- `web_interaction/browser_client.py`: Browser/session abstraction.
- `web_interaction/flows.py`: Test flow definitions per site/page.
- `web_interaction/trace_serializer.py`: Serialize interaction traces.

**Key data structures**

- `InteractionTrace` (JSON): sequence of steps with timestamps, selectors, and outcomes.
- `DOMSnapshot` (JSON/text): HTML and relevant attributes for a given state.

### 2. Perception Layer (`perception/`)

**Responsibilities**

- Capture and manage screenshots from `web_interaction`.
- Extract visual features (layout, color contrast, overlapping elements, etc.).
- Optionally integrate DOM structure with visual features.
- Detect candidate anomalies (e.g., missing images, broken layouts) prior to reasoning.

**Planned modules**

- `perception/screenshot_store.py`: File and metadata handling for screenshots.
- `perception/vision_models.py`: OpenCV/torch-based feature extraction and anomaly scoring.
- `perception/dom_visual_fusion.py`: Combine DOM and visual features.

**Key data structures**

- `Screenshot` (image file + metadata JSON).
- `PerceptionObservation` (JSON): features and preliminary anomaly scores.

### 3. Cognitive Reasoning Layer (`cognitive_reasoning/`)

**Responsibilities**

- Consume observations from `web_interaction` and `perception`.
- Use LLM- or rule-based reasoning (LangChain + transformers + torch) to:
  - Classify issue types.
  - Assess severity and user impact.
  - Filter out likely false positives.
- Propose aggregated bug descriptions and remediation hints.

**Planned modules**

- `cognitive_reasoning/reasoner.py`: Main reasoning pipeline, prompt construction.
- `cognitive_reasoning/models.py`: Model loading and configuration (HF/transformers).
- `cognitive_reasoning/policies.py`: Heuristics and thresholds for bug decisions.

**Key data structures**

- `BugCandidate` (JSON): raw candidate issues prior to final decision.
- `BugReport` (JSON): conforms to `data/annotation_schema.json` fields.

### 4. Reporting Layer (`reporting/`)

**Responsibilities**

- Convert `BugReport` objects into persistent artifacts:
  - JSON files (machine-readable).
  - HTML/Markdown reports (human-readable).
- Aggregate statistics per run, per site, per category.
- Interface with the Dashboard and Evaluation layers.

**Planned modules**

- `reporting/models.py`: Typed representations of bug reports and runs.
- `reporting/json_exporter.py`: Write/read JSON report files.
- `reporting/html_reporter.py`: Generate run summaries.

**Key data structures**

- `RunSummary` (JSON): run-level metrics and metadata.
- `BugReportCollection` (JSON): list of bug reports for a run.

### 5. Dashboard Layer (`dashboard/`)

**Responsibilities**

- Flask-based web UI for:
  - Browsing runs and associated bug reports.
  - Viewing screenshots and DOM snippets.
  - Filtering bugs by severity, issue type, site, and timestamp.
- May later integrate with a database (SQLAlchemy) to store results.

**Planned modules**

- `dashboard/app.py`: Flask application entrypoint.
- `dashboard/routes.py`: Route handlers and templates.
- `dashboard/db.py`: SQLAlchemy models (optional in early stages).

**Key data structures**

- `RunRecord` (DB row or JSON): references to reports and artifacts.

### 6. Evaluation Layer (`evaluation/`)

**Responsibilities**

- Load ground-truth annotations conforming to `data/annotation_schema.json`.
- Compare system-generated `BugReport` objects to ground truth.
- Compute metrics aligned with proposal success criteria:
  - Detection rate / recall (aiming for ≥80%).
  - Precision / false positive rate.
  - Time-to-detect and approximated manual time saved (target ≥50% reduction).

**Planned modules**

- `evaluation/metrics.py`: Core metric computations.
- `evaluation/matching.py`: Logic for matching predicted vs. ground-truth bugs.
- `evaluation/experiments.py`: Scripts to run evaluation over `data/test_sites.csv`.

**Key data structures**

- `EvaluationExample` (JSON): reference to a page, its ground truth, and predictions.
- `EvaluationReport` (JSON): metrics summaries per run and overall.

## Data Formats

### Test Sites Spreadsheet (`data/test_sites.csv`)

A CSV file used by the Web Interaction and Evaluation layers. Columns:

- `site_name`: Human-readable name of the site.
- `url`: Base URL of the site.
- `pages_to_test`: Semicolon-separated list of paths or full URLs to test.
- `expected_functionality`: Short natural language description of what should work.
- `category`: One of `e_commerce`, `blog`, `spa`, `forms`, `content`, etc.

This file seeds scenario design, coverage tracking, and evaluation sampling.

### Ground-Truth Annotation Schema (`data/annotation_schema.json`)

JSON Schema defining the format for ground-truth bug annotations and for system-generated bug reports.

Each annotation is a JSON object with the following **required** fields (from project spec):

- `url`: Page URL where the issue occurs.
- `viewport`: Object describing the browser viewport (width, height, device).
- `screenshot_path`: Relative path to a screenshot image file.
- `issue_type`: Normalized category of the issue.
- `severity`: Impact level.
- `description`: Natural language description of the bug.

Additional optional fields (e.g., `steps_to_reproduce`, `expected_behavior`) are allowed to support richer evaluation.

See `data/annotation_schema.json` for the formal JSON Schema.

## Alignment with Proposal Layers

- **Web Interaction**: Implements the agent's ability to autonomously explore pages and trigger flows, a prerequisite for achieving the autonomy and time-reduction goals.
- **Perception**: Turns raw screenshots and DOM into structured observations to support accurate issue detection.
- **Cognitive Reasoning**: Uses ML/LLM components to push detection performance towards the **≥80% detection** target while controlling false positives.
- **Reporting**: Produces artifacts consumable by QA engineers and downstream tools.
- **Dashboard**: Provides a monitoring and triage interface for humans.
- **Evaluation**: Quantitatively measures detection performance and **manual time reduction (≥50%)** against ground-truth annotations.

This design will be refined as implementation progresses, but the directory structure and data formats defined here establish a stable foundation for the project.
