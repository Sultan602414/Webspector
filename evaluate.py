from __future__ import annotations

import argparse
import csv
import json
from collections import Counter
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Sequence, Tuple

from dashboard.db import Issue, Screenshot, TestSession, get_session, init_engine
from evaluation.matching import AnnotationRecord, match_annotations
from evaluation.metrics import ConfusionStats, compute_overall_stats, compute_stats_by_viewport


ROOT = Path(__file__).resolve().parent


def canonical_viewport_name(viewport: Dict[str, Any]) -> str:
    width = int(viewport.get("width", 0) or 0)
    height = int(viewport.get("height", 0) or 0)
    device = viewport.get("device") or viewport.get("name") or "unknown"
    return f"{device}_{width}x{height}"


def build_key(url: str, viewport_name: str, issue_type: str) -> str:
    return f"{url}|{viewport_name}|{issue_type}"


def load_ground_truth(path: Path) -> List[AnnotationRecord]:
    if not path.is_file():
        raise FileNotFoundError(f"Ground-truth file not found: {path}")

    text = path.read_text(encoding="utf-8").strip()
    records: List[Dict[str, Any]]
    if text.startswith("["):
        records = json.loads(text)
    else:
        records = []
        for line in text.splitlines():
            line = line.strip()
            if not line:
                continue
            records.append(json.loads(line))

    out: List[AnnotationRecord] = []
    for ann in records:
        url = ann.get("url")
        viewport = ann.get("viewport") or {}
        issue_type = ann.get("issue_type") or "other"
        if not url:
            continue
        vp_name = canonical_viewport_name(viewport)
        key = build_key(url, vp_name, issue_type)
        out.append(AnnotationRecord(key=key, url=url, viewport=vp_name, issue_type=issue_type))
    return out


def _filter_sessions(session_ids: Optional[Sequence[int]]) -> List[int]:
    db = get_session()
    try:
        q = db.query(TestSession.id)
        if session_ids:
            q = q.filter(TestSession.id.in_(list(session_ids)))
        rows = q.all()
    finally:
        db.close()
    return [r[0] for r in rows]


def load_predictions(session_ids: Optional[Sequence[int]] = None) -> List[AnnotationRecord]:
    valid_ids = _filter_sessions(session_ids)
    if not valid_ids:
        return []

    db = get_session()
    try:
        q = (
            db.query(Issue, Screenshot)
            .join(Screenshot, Screenshot.id == Issue.screenshot_id)
            .filter(Issue.session_id.in_(valid_ids))
        )
        out: List[AnnotationRecord] = []
        for issue, shot in q.all():
            try:
                ann = json.loads(issue.annotation_json)
            except Exception:
                continue
            url = ann.get("url") or shot.url
            viewport = ann.get("viewport") or {}
            issue_type = ann.get("issue_type") or "other"
            vp_name = canonical_viewport_name(viewport)
            key = build_key(url, vp_name, issue_type)
            out.append(AnnotationRecord(key=key, url=url, viewport=vp_name, issue_type=issue_type))
    finally:
        db.close()

    return out


def estimate_manual_time(ground_truth: Iterable[AnnotationRecord], seconds_per_page: float) -> float:
    pages = {(rec.url, rec.viewport) for rec in ground_truth}
    return float(len(pages)) * float(seconds_per_page)


def estimate_automated_time(session_ids: Optional[Sequence[int]] = None) -> float:
    valid_ids = _filter_sessions(session_ids)
    if not valid_ids:
        return 0.0
    db = get_session()
    try:
        q = db.query(Screenshot).filter(Screenshot.session_id.in_(valid_ids))
        total = 0.0
        for shot in q.all():
            total += float(shot.load_time or 0.0) + 2.0  # approximate extra processing time
    finally:
        db.close()
    return total


def write_summary_csv(path: Path, stats: ConfusionStats, manual_time: float, auto_time: float) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(
            [
                "tp",
                "fp",
                "fn",
                "precision",
                "recall",
                "f1",
                "fp_rate",
                "manual_time_sec",
                "auto_time_sec",
                "time_reduction_pct",
            ]
        )
        time_reduction_pct = 0.0
        if manual_time > 0.0:
            time_reduction_pct = max(0.0, (manual_time - auto_time) / manual_time * 100.0)
        writer.writerow(
            [
                stats.tp,
                stats.fp,
                stats.fn,
                f"{stats.precision:.3f}",
                f"{stats.recall:.3f}",
                f"{stats.f1:.3f}",
                f"{stats.fp_rate:.3f}",
                f"{manual_time:.1f}",
                f"{auto_time:.1f}",
                f"{time_reduction_pct:.1f}",
            ]
        )


def write_viewport_csv(path: Path, by_viewport: Dict[str, ConfusionStats]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["viewport", "tp", "fp", "fn", "precision", "recall", "f1", "fp_rate"])
        for vp, s in sorted(by_viewport.items()):
            writer.writerow(
                [
                    vp,
                    s.tp,
                    s.fp,
                    s.fn,
                    f"{s.precision:.3f}",
                    f"{s.recall:.3f}",
                    f"{s.f1:.3f}",
                    f"{s.fp_rate:.3f}",
                ]
            )


def write_error_analysis_csv(path: Path, tp: List[AnnotationRecord], fp: List[AnnotationRecord], fn: List[AnnotationRecord]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["kind", "url", "viewport", "issue_type", "key"])
        for rec in fn:
            writer.writerow(["FN", rec.url, rec.viewport, rec.issue_type, rec.key])
        for rec in fp:
            writer.writerow(["FP", rec.url, rec.viewport, rec.issue_type, rec.key])
        for rec in tp:
            writer.writerow(["TP", rec.url, rec.viewport, rec.issue_type, rec.key])


def generate_plots(
    out_dir: Path,
    overall: ConfusionStats,
    by_viewport: Dict[str, ConfusionStats],
    manual_time: float,
    auto_time: float,
) -> None:
    try:
        import matplotlib.pyplot as plt  # type: ignore
    except Exception:  # pragma: no cover - plotting is optional
        return

    out_dir.mkdir(parents=True, exist_ok=True)

    # Overall metrics
    fig, ax = plt.subplots(figsize=(4, 3))
    metrics = ["precision", "recall", "f1"]
    values = [overall.precision, overall.recall, overall.f1]
    ax.bar(metrics, values, color=["#2563eb", "#16a34a", "#9333ea"])
    ax.set_ylim(0.0, 1.0)
    ax.set_ylabel("Score")
    ax.set_title("Overall detection metrics")
    for i, v in enumerate(values):
        ax.text(i, v + 0.02, f"{v:.2f}", ha="center", va="bottom", fontsize=8)
    fig.tight_layout()
    fig.savefig(out_dir / "overall_metrics.png", dpi=150)
    plt.close(fig)

    # F1 by viewport
    if by_viewport:
        fig, ax = plt.subplots(figsize=(max(4, len(by_viewport)), 3))
        vps = list(sorted(by_viewport.keys()))
        f1s = [by_viewport[vp].f1 for vp in vps]
        ax.bar(vps, f1s, color="#0ea5e9")
        ax.set_ylim(0.0, 1.0)
        ax.set_ylabel("F1")
        ax.set_title("F1 by viewport")
        ax.tick_params(axis="x", rotation=30)
        for i, v in enumerate(f1s):
            ax.text(i, v + 0.02, f"{v:.2f}", ha="center", va="bottom", fontsize=8)
        fig.tight_layout()
        fig.savefig(out_dir / "f1_by_viewport.png", dpi=150)
        plt.close(fig)

    # Time comparison
    fig, ax = plt.subplots(figsize=(4, 3))
    labels = ["Manual", "WebSpector"]
    values = [manual_time, auto_time]
    colors = ["#6b7280", "#10b981"]
    ax.bar(labels, values, color=colors)
    ax.set_ylabel("Total seconds")
    ax.set_title("Time per test (total)")
    for i, v in enumerate(values):
        ax.text(i, v + max(1.0, v * 0.02), f"{v:.0f}s", ha="center", va="bottom", fontsize=8)
    fig.tight_layout()
    fig.savefig(out_dir / "time_comparison.png", dpi=150)
    plt.close(fig)


def summarize_errors(tp: List[AnnotationRecord], fp: List[AnnotationRecord], fn: List[AnnotationRecord]) -> Dict[str, Any]:
    issue_type_fn = Counter(rec.issue_type for rec in fn)
    issue_type_fp = Counter(rec.issue_type for rec in fp)
    viewport_fn = Counter(rec.viewport for rec in fn)
    viewport_fp = Counter(rec.viewport for rec in fp)
    return {
        "fn_by_issue_type": issue_type_fn,
        "fp_by_issue_type": issue_type_fp,
        "fn_by_viewport": viewport_fn,
        "fp_by_viewport": viewport_fp,
    }


def recommend_fixes(overall: ConfusionStats, error_summary: Dict[str, Any]) -> List[str]:
    recs: List[str] = []
    if overall.recall < 0.8:
        recs.append(
            "Recall below 0.80. Focus on missed ground-truth issues (FNs) by issue_type and viewport."
        )
    if overall.fp_rate > 0.2:
        recs.append(
            "High false positive rate; tighten perception thresholds (e.g., anomaly_score) and orchestrator filters."
        )

    fn_by_issue_type: Counter = error_summary.get("fn_by_issue_type", Counter())
    if fn_by_issue_type:
        worst_type, count = fn_by_issue_type.most_common(1)[0]
        if worst_type in {"layout", "visual"}:
            recs.append(
                "Many missed layout/visual issues. Consider tuning PerceptionPipeline thresholds (contrast, placeholder_fraction) "
                "and adding heuristics for truncated/overlapping elements."
            )
        elif worst_type in {"functional"}:
            recs.append(
                "Many missed functional issues. Enrich orchestrator prompts with more functional expectations and "
                "add DOM/network-based checks (e.g., HTTP errors, form submission results)."
            )

    fn_by_viewport: Counter = error_summary.get("fn_by_viewport", Counter())
    if fn_by_viewport:
        worst_vp, _ = fn_by_viewport.most_common(1)[0]
        if "mobile" in worst_vp.lower():
            recs.append(
                "Missed issues are concentrated on mobile viewports. Add more responsiveness-specific checks and "
                "ensure mobile captures are enabled for all flows."
            )

    if not recs:
        recs.append("No major issues detected; metrics look healthy. Continue monitoring on new sites.")
    return recs


def parse_args(argv: Optional[Sequence[str]] = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Evaluate WebSpector detection accuracy against ground-truth annotations and "
            "estimate time savings vs a manual baseline."
        )
    )
    parser.add_argument(
        "--ground-truth",
        required=True,
        help="Path to ground-truth annotations (JSON or JSONL) following data/annotation_schema.json.",
    )
    parser.add_argument(
        "--database",
        default=str(ROOT / "dashboard.db"),
        help="SQLAlchemy database URL or path to SQLite file (default: ./dashboard.db)",
    )
    parser.add_argument(
        "--session-id",
        action="append",
        type=int,
        help="Optional session id to include. Repeat flag to pass multiple sessions. By default all sessions are used.",
    )
    parser.add_argument(
        "--manual-seconds-per-page",
        type=float,
        default=60.0,
        help="Assumed manual tester time per page (seconds) for baseline (default: 60).",
    )
    parser.add_argument(
        "--out-dir",
        default=str(ROOT / "evaluation" / "results"),
        help="Directory to write CSV summaries and charts (default: evaluation/results).",
    )
    return parser.parse_args(argv)


def main(argv: Optional[Sequence[str]] = None) -> None:
    args = parse_args(argv)

    gt_path = Path(args.ground_truth)
    ground_truth = load_ground_truth(gt_path)
    if not ground_truth:
        raise SystemExit("No valid ground-truth annotations loaded; check the file format.")

    db_url = args.database
    if db_url.endswith(".db") and not db_url.startswith("sqlite:"):
        db_url = f"sqlite:///{db_url}"

    init_engine(db_url)

    session_ids = args.session_id if args.session_id else None
    predictions = load_predictions(session_ids=session_ids)

    match = match_annotations(ground_truth, predictions)
    overall = compute_overall_stats(match.true_positives, match.false_positives, match.false_negatives)
    by_viewport = compute_stats_by_viewport(match.true_positives, match.false_positives, match.false_negatives)

    manual_time = estimate_manual_time(ground_truth, seconds_per_page=args.manual_seconds_per_page)
    auto_time = estimate_automated_time(session_ids=session_ids)

    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    write_summary_csv(out_dir / "summary.csv", overall, manual_time, auto_time)
    write_viewport_csv(out_dir / "by_viewport.csv", by_viewport)
    write_error_analysis_csv(out_dir / "error_analysis.csv", match.true_positives, match.false_positives, match.false_negatives)
    generate_plots(out_dir, overall, by_viewport, manual_time, auto_time)

    error_summary = summarize_errors(match.true_positives, match.false_positives, match.false_negatives)
    recs = recommend_fixes(overall, error_summary)

    print("=== Evaluation Summary ===")
    print(f"Ground truth issues: {len(ground_truth)}")
    print(f"Predicted issues:    {len(predictions)}")
    print(f"TP: {overall.tp}  FP: {overall.fp}  FN: {overall.fn}")
    print(f"Precision: {overall.precision:.3f}  Recall: {overall.recall:.3f}  F1: {overall.f1:.3f}  FP rate: {overall.fp_rate:.3f}")
    print("")
    print(f"Manual baseline time: {manual_time:.1f}s  |  WebSpector time: {auto_time:.1f}s")
    if manual_time > 0.0:
        tr = max(0.0, (manual_time - auto_time) / manual_time * 100.0)
        print(f"Approx. time reduction: {tr:.1f}%")
    print("")

    if overall.recall < 0.8:
        print("Overall recall is below 0.80; consider tuning system components.")

    print("\n=== Recommended Fixes / Next Steps ===")
    for r in recs:
        print(f"- {r}")

    print("\nArtifacts written to:", out_dir)


if __name__ == "__main__":  # pragma: no cover
    main()
