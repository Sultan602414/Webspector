import json
from pathlib import Path

import pytest

from perception.perception import PerceptionObservation, PerceptionPipeline


@pytest.mark.integration
def test_perception_analyze_screenshot_minimal(tmp_path: Path) -> None:
    try:
        import cv2  # type: ignore  # noqa: F401
    except Exception:
        pytest.skip("cv2 is required for perception tests")

    try:
        from PIL import Image
    except Exception:
        pytest.skip("Pillow is required for perception tests")

    img_path = tmp_path / "test_screenshot.png"
    img = Image.new("RGB", (400, 300), color=(255, 255, 255))
    img.save(img_path)

    pipeline = PerceptionPipeline(
        enable_captioning=False,
        enable_ocr=False,
        enable_clip=False,
    )

    observation = pipeline.analyze_screenshot(img_path)

    assert isinstance(observation, PerceptionObservation)
    vf = observation.visual_features
    assert vf.width > 0 and vf.height > 0
    assert 0.0 <= observation.anomaly_score <= 1.0

    out_path = tmp_path / "perception_obs.json"
    pipeline.save_observation_json(observation, out_path)

    data = json.loads(out_path.read_text(encoding="utf-8"))
    assert data["screenshot_path"].endswith(".png")
    assert isinstance(data["visual_features"], dict)
    assert isinstance(data["detected_elements"], list)
    assert isinstance(data["findings"], list)
    assert isinstance(data["anomaly_score"], float)
