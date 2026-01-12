from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List

from .matching import AnnotationRecord


@dataclass
class ConfusionStats:
    tp: int
    fp: int
    fn: int

    @property
    def precision(self) -> float:
        denom = self.tp + self.fp
        return float(self.tp) / denom if denom > 0 else 0.0

    @property
    def recall(self) -> float:
        denom = self.tp + self.fn
        return float(self.tp) / denom if denom > 0 else 0.0

    @property
    def f1(self) -> float:
        p = self.precision
        r = self.recall
        denom = p + r
        return 2 * p * r / denom if denom > 0 else 0.0

    @property
    def fp_rate(self) -> float:
        denom = self.tp + self.fp
        return float(self.fp) / denom if denom > 0 else 0.0


def compute_overall_stats(tp: List[AnnotationRecord], fp: List[AnnotationRecord], fn: List[AnnotationRecord]) -> ConfusionStats:
    return ConfusionStats(tp=len(tp), fp=len(fp), fn=len(fn))


def compute_stats_by_viewport(
    tp: List[AnnotationRecord],
    fp: List[AnnotationRecord],
    fn: List[AnnotationRecord],
) -> Dict[str, ConfusionStats]:
    buckets: Dict[str, Dict[str, int]] = {}

    def bump(kind: str, viewport: str) -> None:
        b = buckets.setdefault(viewport, {"tp": 0, "fp": 0, "fn": 0})
        b[kind] += 1

    for rec in tp:
        bump("tp", rec.viewport)
    for rec in fp:
        bump("fp", rec.viewport)
    for rec in fn:
        bump("fn", rec.viewport)

    return {
        vp: ConfusionStats(tp=data["tp"], fp=data["fp"], fn=data["fn"])
        for vp, data in buckets.items()
    }
