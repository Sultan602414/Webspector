import json
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

try:
    import cv2
except Exception:  # pragma: no cover
    cv2 = None  # type: ignore

try:
    import pytesseract
except Exception:  # pragma: no cover
    pytesseract = None  # type: ignore

try:
    from PIL import Image
except Exception:  # pragma: no cover
    Image = None  # type: ignore

try:
    import torch
    import torch.nn.functional as F
except Exception:  # pragma: no cover
    torch = None  # type: ignore
    F = None  # type: ignore

try:
    from transformers import CLIPModel, CLIPProcessor, pipeline
except Exception:  # pragma: no cover
    CLIPModel = None  # type: ignore
    CLIPProcessor = None  # type: ignore
    pipeline = None  # type: ignore


@dataclass
class OCRElement:
    text: str
    bbox: Tuple[int, int, int, int]
    confidence: float


@dataclass
class VisualFeatures:
    width: int
    height: int
    avg_luminance: float
    contrast: float
    text_area_ratio: float
    layout_density: float
    num_text_blocks: int
    placeholder_fraction: float


@dataclass
class Finding:
    type: str
    severity: str
    message: str
    metadata: Dict[str, Any]


@dataclass
class PerceptionObservation:
    screenshot_path: str
    semantic_caption: Optional[str]
    detected_elements: List[OCRElement]
    visual_features: VisualFeatures
    anomaly_score: float
    findings: List[Finding]

    def to_json(self) -> Dict[str, Any]:
        return asdict(self)


class GPT4VAdapter:
    def __init__(self, client: Any, model: str, system_prompt: Optional[str] = None) -> None:
        self.client = client
        self.model = model
        self.system_prompt = system_prompt or "You are a testing assistant that describes web UI screenshots and potential visual issues."

    def generate_caption(self, image_bytes: bytes, user_prompt: Optional[str] = None) -> str:
        if self.client is None:
            raise RuntimeError("GPT-4V client is not configured")
        prompt = user_prompt or "Describe this web page UI and mention any visual anomalies or layout issues you can see."
        import base64

        image_b64 = base64.b64encode(image_bytes).decode("ascii")
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": self.system_prompt},
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt},
                        {
                            "type": "image_url",
                            "image_url": {"url": f"data:image/png;base64,{image_b64}"},
                        },
                    ],
                },
            ],
        )
        content = response.choices[0].message.content
        return str(content)


class PerceptionPipeline:
    def __init__(
        self,
        device: Optional[str] = None,
        enable_captioning: bool = True,
        enable_ocr: bool = True,
        enable_clip: bool = True,
        blip_model_name: str = "Salesforce/blip-image-captioning-base",
        clip_model_name: str = "openai/clip-vit-base-patch32",
        gpt4v_adapter: Optional[GPT4VAdapter] = None,
    ) -> None:
        self.device = device or ("cuda" if torch is not None and torch.cuda.is_available() else "cpu")
        self.enable_captioning = enable_captioning and pipeline is not None
        self.enable_ocr = enable_ocr and cv2 is not None and pytesseract is not None
        self.enable_clip = enable_clip and CLIPModel is not None and CLIPProcessor is not None and torch is not None
        self.blip_model_name = blip_model_name
        self.clip_model_name = clip_model_name
        self.gpt4v_adapter = gpt4v_adapter
        self._caption_pipeline = None
        self._clip_model = None
        self._clip_processor = None

    def analyze_screenshot(
        self,
        image_path: Path,
        expected_page_type: Optional[str] = None,
        baseline_clip_embedding: Optional["torch.Tensor"] = None,
    ) -> PerceptionObservation:
        if cv2 is None:
            # Fallback for when cv2 is missing (e.g. Python 3.14 compatibility issues)
            return PerceptionObservation(
                screenshot_path=str(image_path).replace("\\", "/"),
                semantic_caption=None,
                detected_elements=[],
                visual_features=VisualFeatures(
                    width=0, height=0, avg_luminance=0, contrast=0, 
                    text_area_ratio=0, layout_density=0, num_text_blocks=0, placeholder_fraction=0
                ),
                anomaly_score=0.0,
                findings=[
                    Finding(
                        type="dependency_missing",
                        severity="warning",
                        message="AI perception disabled: 'opencv-python' not installed (likely due to Python version incompatibility).",
                        metadata={"python_version": "3.14+"}
                    )
                ]
            )
            
        image_path = Path(image_path)
        if not image_path.is_file():
            raise FileNotFoundError(str(image_path))
        bgr, gray, ocr_ready, rgb = self._preprocess_image(image_path)
        elements: List[OCRElement] = []
        if self.enable_ocr:
            elements = self._run_ocr(ocr_ready)
        features = self._compute_visual_features(bgr, gray, elements)
        caption = None
        if self.enable_captioning:
            caption = self._generate_caption(rgb)
        if self.gpt4v_adapter is not None and Image is not None:
            with image_path.open("rb") as f:
                caption = self.gpt4v_adapter.generate_caption(f.read())
        anomaly_score = self._compute_anomaly_score(
            rgb,
            features,
            expected_page_type=expected_page_type,
            baseline_clip_embedding=baseline_clip_embedding,
        )
        findings = self._compute_findings(features, elements, caption, anomaly_score)
        return PerceptionObservation(
            screenshot_path=str(image_path).replace("\\", "/"),
            semantic_caption=caption,
            detected_elements=elements,
            visual_features=features,
            anomaly_score=anomaly_score,
            findings=findings,
        )

    def save_observation_json(self, observation: PerceptionObservation, out_path: Path) -> None:
        data = observation.to_json()
        out_path = Path(out_path)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(json.dumps(data, indent=2), encoding="utf-8")

    def _preprocess_image(self, image_path: Path) -> Tuple[Any, Any, Any, Any]:
        assert cv2 is not None
        bgr = cv2.imread(str(image_path), cv2.IMREAD_COLOR)
        if bgr is None:
            raise RuntimeError("Failed to read image")
        h, w = bgr.shape[:2]
        max_w, max_h = 1024, 1024
        scale = min(max_w / float(w), max_h / float(h), 1.0)
        if scale < 1.0:
            new_w = int(w * scale)
            new_h = int(h * scale)
            bgr = cv2.resize(bgr, (new_w, new_h), interpolation=cv2.INTER_AREA)
        gray = cv2.cvtColor(bgr, cv2.COLOR_BGR2GRAY)
        ocr_ready = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 31, 15)
        rgb = cv2.cvtColor(bgr, cv2.COLOR_BGR2RGB)
        return bgr, gray, ocr_ready, rgb

    def _run_ocr(self, ocr_image: Any) -> List[OCRElement]:
        assert pytesseract is not None
        data = pytesseract.image_to_data(ocr_image, output_type=pytesseract.Output.DICT)
        texts = data.get("text", [])
        confs = data.get("conf", [])
        left = data.get("left", [])
        top = data.get("top", [])
        width = data.get("width", [])
        height = data.get("height", [])
        elements: List[OCRElement] = []
        for i, raw in enumerate(texts):
            text = str(raw).strip()
            if not text:
                continue
            try:
                conf = float(confs[i])
            except Exception:
                conf = 0.0
            if conf < 0:
                continue
            x = int(left[i])
            y = int(top[i])
            w = int(width[i])
            h = int(height[i])
            elements.append(OCRElement(text=text, bbox=(x, y, w, h), confidence=conf))
        return elements

    def _compute_visual_features(self, bgr: Any, gray: Any, elements: List[OCRElement]) -> VisualFeatures:
        assert cv2 is not None
        h, w = gray.shape[:2]
        mean_val, std_val = cv2.meanStdDev(gray)
        avg_luminance = float(mean_val[0][0]) / 255.0
        contrast = float(std_val[0][0]) / 255.0
        total_area = float(w * h)
        text_area = 0.0
        for e in elements:
            _, _, bw, bh = e.bbox
            text_area += float(max(bw, 0) * max(bh, 0))
        text_area_ratio = text_area / total_area if total_area > 0 else 0.0
        edges = cv2.Canny(gray, 100, 200)
        edge_pixels = float(cv2.countNonZero(edges))
        layout_density = edge_pixels / total_area if total_area > 0 else 0.0
        _, white = cv2.threshold(gray, 245, 255, cv2.THRESH_BINARY)
        white_pixels = float(cv2.countNonZero(white))
        placeholder_fraction = white_pixels / total_area if total_area > 0 else 0.0
        return VisualFeatures(
            width=w,
            height=h,
            avg_luminance=avg_luminance,
            contrast=contrast,
            text_area_ratio=min(text_area_ratio, 1.0),
            layout_density=min(layout_density, 1.0),
            num_text_blocks=len(elements),
            placeholder_fraction=min(placeholder_fraction, 1.0),
        )

    def _ensure_caption_pipeline(self) -> None:
        if self._caption_pipeline is not None or not self.enable_captioning:
            return
        assert pipeline is not None
        kwargs: Dict[str, Any] = {"model": self.blip_model_name}
        if torch is not None and self.device == "cuda":
            kwargs["device"] = 0
        self._caption_pipeline = pipeline("image-to-text", **kwargs)

    def _generate_caption(self, rgb: Any) -> Optional[str]:
        self._ensure_caption_pipeline()
        if self._caption_pipeline is None:
            return None
        if Image is None:
            return None
        img = Image.fromarray(rgb)
        out = self._caption_pipeline(img, max_new_tokens=64)
        if isinstance(out, list) and out:
            text = out[0].get("generated_text") or out[0].get("caption")
            if isinstance(text, str):
                return text
        return None

    def _ensure_clip(self) -> None:
        if self._clip_model is not None or not self.enable_clip:
            return
        assert CLIPModel is not None and CLIPProcessor is not None and torch is not None
        self._clip_model = CLIPModel.from_pretrained(self.clip_model_name)
        self._clip_processor = CLIPProcessor.from_pretrained(self.clip_model_name)
        self._clip_model.to(self.device)
        self._clip_model.eval()

    def _clip_embedding_from_image(self, rgb: Any) -> Optional["torch.Tensor"]:
        self._ensure_clip()
        if self._clip_model is None or self._clip_processor is None or torch is None:
            return None
        img = Image.fromarray(rgb) if Image is not None else rgb
        inputs = self._clip_processor(images=img, return_tensors="pt")
        inputs = {k: v.to(self.device) for k, v in inputs.items()}
        with torch.no_grad():
            emb = self._clip_model.get_image_features(**inputs)
        emb = F.normalize(emb, p=2, dim=-1)
        return emb.squeeze(0)

    def _clip_embedding_from_text(self, text: str) -> Optional["torch.Tensor"]:
        self._ensure_clip()
        if self._clip_model is None or self._clip_processor is None or torch is None:
            return None
        inputs = self._clip_processor(text=[text], return_tensors="pt", padding=True)
        inputs = {k: v.to(self.device) for k, v in inputs.items()}
        with torch.no_grad():
            emb = self._clip_model.get_text_features(**inputs)
        emb = F.normalize(emb, p=2, dim=-1)
        return emb.squeeze(0)

    def _compute_anomaly_score(
        self,
        rgb: Any,
        features: VisualFeatures,
        expected_page_type: Optional[str] = None,
        baseline_clip_embedding: Optional["torch.Tensor"] = None,
    ) -> float:
        sim: Optional[float] = None
        if self.enable_clip:
            img_emb = self._clip_embedding_from_image(rgb)
            if img_emb is not None:
                ref_emb = baseline_clip_embedding
                if ref_emb is None and expected_page_type:
                    ref_emb = self._clip_embedding_from_text(expected_page_type)
                if ref_emb is not None and torch is not None:
                    sim = float(torch.matmul(img_emb, ref_emb) / (img_emb.norm() * ref_emb.norm() + 1e-8))
        anomaly = 0.5
        if sim is not None:
            similarity_score = max(min(sim, 1.0), -1.0)
            anomaly = 1.0 - (similarity_score + 1.0) / 2.0
        penalty = 0.0
        if features.contrast < 0.1:
            penalty += 0.2
        if features.placeholder_fraction > 0.5:
            penalty += 0.2
        if features.layout_density < 0.02:
            penalty += 0.1
        anomaly = max(0.0, min(anomaly + penalty, 1.0))
        return anomaly

    def _compute_findings(
        self,
        features: VisualFeatures,
        elements: List[OCRElement],
        caption: Optional[str],
        anomaly_score: float,
    ) -> List[Finding]:
        findings: List[Finding] = []
        if features.contrast < 0.08:
            findings.append(
                Finding(
                    type="low_contrast",
                    severity="medium",
                    message="Overall grayscale contrast appears low; text may be hard to read.",
                    metadata={"contrast": features.contrast},
                )
            )
        if features.placeholder_fraction > 0.5:
            findings.append(
                Finding(
                    type="large_blank_regions",
                    severity="medium",
                    message="Large white/blank regions detected; possible missing images or content.",
                    metadata={"placeholder_fraction": features.placeholder_fraction},
                )
            )
            findings.append(
                Finding(
                    type="possible_missing_hero_image",
                    severity="medium",
                    message=(
                        "Large bright/blank region detected with relatively little text; "
                        "a hero image or banner may be missing or not loaded."
                    ),
                    metadata={
                        "placeholder_fraction": features.placeholder_fraction,
                        "text_area_ratio": features.text_area_ratio,
                    },
                )
            )
        if features.text_area_ratio < 0.01 and features.num_text_blocks <= 1:
            findings.append(
                Finding(
                    type="very_little_text",
                    severity="low",
                    message="Almost no text detected on the page; possible rendering failure.",
                    metadata={"text_area_ratio": features.text_area_ratio, "num_text_blocks": features.num_text_blocks},
                )
            )
        if features.layout_density > 0.5:
            findings.append(
                Finding(
                    type="high_layout_density",
                    severity="low",
                    message="Many edges and visual elements; layout may be crowded or cluttered.",
                    metadata={"layout_density": features.layout_density},
                )
            )
        if elements and len(elements) > 5:
            overlaps = 0
            for i in range(len(elements)):
                x1, y1, w1, h1 = elements[i].bbox
                a1 = max(w1, 0) * max(h1, 0)
                if a1 <= 0:
                    continue
                for j in range(i + 1, len(elements)):
                    x2, y2, w2, h2 = elements[j].bbox
                    a2 = max(w2, 0) * max(h2, 0)
                    if a2 <= 0:
                        continue
                    ix1 = max(x1, x2)
                    iy1 = max(y1, y2)
                    ix2 = min(x1 + w1, x2 + w2)
                    iy2 = min(y1 + h1, y2 + h2)
                    iw = max(0, ix2 - ix1)
                    ih = max(0, iy2 - iy1)
                    inter = iw * ih
                    if inter <= 0:
                        continue
                    smaller = float(min(a1, a2))
                    if smaller > 0 and inter / smaller > 0.5:
                        overlaps += 1
                        if overlaps > 5:
                            break
                if overlaps > 5:
                    break
            if overlaps > 5:
                findings.append(
                    Finding(
                        type="possible_button_or_text_overlap",
                        severity="medium",
                        message=(
                            "Multiple overlapping text regions detected; this may indicate "
                            "buttons or labels visually overlapping or cramped."
                        ),
                        metadata={"overlap_pairs": overlaps},
                    )
                )
        if elements:
            try:
                page_width = max(e.bbox[0] + e.bbox[2] for e in elements)
            except ValueError:
                page_width = 0
            truncated_candidates: List[OCRElement] = []
            for e in elements:
                text = e.text.strip()
                if not text:
                    continue
                if text.endswith("...") or text.endswith("…"):
                    truncated_candidates.append(e)
                elif page_width and e.bbox[0] + e.bbox[2] >= 0.95 * page_width and len(text) > 20:
                    truncated_candidates.append(e)
            if truncated_candidates:
                findings.append(
                    Finding(
                        type="possible_truncated_text",
                        severity="low",
                        message="Some text blocks look truncated or cut off at the edge of the viewport.",
                        metadata={
                            "examples": [t.text for t in truncated_candidates[:3]],
                            "count": len(truncated_candidates),
                        },
                    )
                )
        if caption:
            lowered = caption.lower()
            if "error" in lowered or "not found" in lowered:
                findings.append(
                    Finding(
                        type="error_state_caption",
                        severity="high",
                        message="Caption suggests an error or not-found state.",
                        metadata={"caption": caption},
                    )
                )
        if anomaly_score > 0.7:
            findings.append(
                Finding(
                    type="high_anomaly_score",
                    severity="high",
                    message="Overall anomaly score is high.",
                    metadata={"anomaly_score": anomaly_score},
                )
            )
        return findings
