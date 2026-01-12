from __future__ import annotations

from dataclasses import dataclass
from typing import List


@dataclass
class AnnotationRecord:
    """Normalized view of a bug annotation for matching.

    key:        unique key used for matching (e.g., url|viewport|issue_type).
    url:        page URL.
    viewport:   canonical viewport name (e.g., desktop_1366x768).
    issue_type: normalized issue type (e.g., layout, functional).
    """

    key: str
    url: str
    viewport: str
    issue_type: str


@dataclass
class MatchResult:
    true_positives: List[AnnotationRecord]
    false_positives: List[AnnotationRecord]
    false_negatives: List[AnnotationRecord]


def match_annotations(
    ground_truth: List[AnnotationRecord],
    predictions: List[AnnotationRecord],
) -> MatchResult:
    """Greedy matching between ground-truth and predicted annotations.

    A prediction is considered a true positive if there exists at least one
    ground-truth annotation with the same key (url+viewport+issue_type) that
    has not already been matched. Remaining predictions are false positives.
    Ground-truth annotations that are never matched are false negatives.
    """

    gt_by_key: dict[str, List[AnnotationRecord]] = {}
    for rec in ground_truth:
        gt_by_key.setdefault(rec.key, []).append(rec)

    tp: List[AnnotationRecord] = []
    fp: List[AnnotationRecord] = []

    for pred in predictions:
        bucket = gt_by_key.get(pred.key)
        if bucket:
            # consume one GT item from this bucket
            _ = bucket.pop(0)
            tp.append(pred)
        else:
            fp.append(pred)

    fn: List[AnnotationRecord] = []
    for remaining in gt_by_key.values():
        fn.extend(remaining)

    return MatchResult(true_positives=tp, false_positives=fp, false_negatives=fn)
