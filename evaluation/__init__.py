"""Evaluation utilities: matching and metric computation."""

from .matching import AnnotationRecord, match_annotations  # noqa: F401
from .metrics import ConfusionStats, compute_overall_stats, compute_stats_by_viewport  # noqa: F401

