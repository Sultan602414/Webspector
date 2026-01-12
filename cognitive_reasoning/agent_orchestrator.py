from __future__ import annotations

import json
import os
from typing import Any, Dict, List, Tuple

try:  # optional LangChain + OpenAI
    from langchain.chat_models import ChatOpenAI  # type: ignore
except Exception:  # pragma: no cover
    ChatOpenAI = None  # type: ignore

try:  # optional local LLM
    from transformers import pipeline as hf_pipeline  # type: ignore
except Exception:  # pragma: no cover
    hf_pipeline = None  # type: ignore


ISSUE_CLASSES = {"UI", "navigation", "responsiveness", "functional"}
SEVERITY_LEVELS = ["low", "medium", "high", "critical"]
RECOMMENDED_ACTIONS = {"retest", "flag", "skip", "escalate"}


class AgentOrchestrator:
    def __init__(self) -> None:
        self._local_pipe = None

    def analyze_and_plan(self, perception_json: Dict[str, Any]) -> Tuple[Dict[str, Any], str]:
        obs = dict(perception_json or {})
        findings: List[Dict[str, Any]] = obs.get("findings", []) or []
        anomaly_score = float(obs.get("anomaly_score", 0.0) or 0.0)

        issue_class = self._classify_issue(obs)
        severity = self._determine_severity(obs, issue_class)
        recommended_action = self._recommend_action(issue_class, severity, anomaly_score, findings)

        url = obs.get("url") or (obs.get("metadata") or {}).get("url") or ""
        viewport = obs.get("viewport") or (obs.get("metadata") or {}).get("viewport") or {}
        screenshot_path = obs.get("screenshot_path") or obs.get("screenshot") or ""

        action_plan = self._build_action_plan(issue_class, severity, url, viewport, screenshot_path, findings)
        description = self._build_description(issue_class, severity, findings, obs.get("semantic_caption") or "")
        steps_to_reproduce = self._build_repro_steps(url, viewport, issue_class, findings)
        evidence_links = self._build_evidence_links(screenshot_path, obs)

        schema_issue_type = self._map_issue_type(issue_class)
        schema_severity = self._map_schema_severity(severity)

        annotation: Dict[str, Any] = {
            "url": url or "unknown",
            "viewport": self._build_viewport_payload(viewport),
            "screenshot_path": screenshot_path,
            "issue_type": schema_issue_type,
            "severity": schema_severity,
            "description": description,
            "steps_to_reproduce": "\n".join(steps_to_reproduce),
        }

        bug_report = {
            "title": self._build_title(issue_class, severity, url),
            "description": description,
            "steps_to_reproduce": steps_to_reproduce,
            "evidence_links": evidence_links,
        }

        structured: Dict[str, Any] = {
            "issue_class": issue_class,
            "severity": severity,
            "recommended_action": recommended_action,
            "anomaly_score": anomaly_score,
            "action_plan": action_plan,
            "bug_report": bug_report,
            "annotation": annotation,
        }

        human_readable = self._render_human_report(structured)
        return structured, human_readable

    # ---------- classification & severity ----------
    def _classify_issue(self, obs: Dict[str, Any]) -> str:
        findings: List[Dict[str, Any]] = obs.get("findings", []) or []
        caption = (obs.get("semantic_caption") or "").lower()
        types = {str(f.get("type", "")) for f in findings}

        if any(
            t in types
            for t in [
                "low_contrast",
                "large_blank_regions",
                "possible_missing_hero_image",
                "high_layout_density",
                "possible_button_or_text_overlap",
                "possible_truncated_text",
            ]
        ):
            return "UI"
        if "error_state_caption" in types:
            return "functional"
        if any("navigation" in t or "redirect" in t or "link" in t for t in types):
            return "navigation"
        if "mobile" in caption or "responsive" in caption or "small screen" in caption:
            return "responsiveness"
        if float(obs.get("anomaly_score", 0.0) or 0.0) > 0.8:
            return "UI"
        return "functional"

    def _determine_severity(self, obs: Dict[str, Any], issue_class: str) -> str:
        findings: List[Dict[str, Any]] = obs.get("findings", []) or []
        caption = (obs.get("semantic_caption") or "").lower()
        score = float(obs.get("anomaly_score", 0.0) or 0.0)

        critical_keywords = ["checkout", "payment", "pay", "purchase", "order", "login", "sign in"]
        if any(k in caption for k in critical_keywords) and ("error" in caption or "failed" in caption):
            return "critical"

        level_map = {"low": 0, "medium": 1, "high": 2, "critical": 3}
        level = 0
        for f in findings:
            sev = str(f.get("severity", "")).lower()
            level = max(level, level_map.get(sev, 0))

        if score > 0.9:
            level = max(level, 3)
        elif score > 0.75:
            level = max(level, 2)
        elif score > 0.5:
            level = max(level, 1)

        return SEVERITY_LEVELS[level]

    def _recommend_action(
        self,
        issue_class: str,
        severity: str,
        anomaly_score: float,
        findings: List[Dict[str, Any]],
    ) -> str:
        if severity == "critical":
            return "escalate"
        if severity == "high":
            return "flag"
        if severity == "medium":
            return "retest"
        if anomaly_score < 0.4 and len(findings) <= 1:
            return "skip"
        return "retest"

    # ---------- action planning ----------
    def _build_action_plan(
        self,
        issue_class: str,
        severity: str,
        url: str,
        viewport: Dict[str, Any],
        screenshot_path: str,
        findings: List[Dict[str, Any]],
    ) -> Dict[str, Any]:
        vp_name = viewport.get("name") or viewport.get("device") or "desktop"
        steps: List[Dict[str, Any]] = []
        step = 1

        if url:
            steps.append({"step": step, "operation": "open_url", "url": url, "viewport": vp_name})
            step += 1

        if issue_class == "responsiveness":
            steps.append({"step": step, "operation": "change_viewport", "viewport": "mobile"})
            step += 1
            steps.append({"step": step, "operation": "recapture", "artifacts": ["screenshot", "dom"]})
        elif issue_class == "navigation":
            steps.append({"step": step, "operation": "click_top_nav_links", "max_links": 3})
            step += 1
            steps.append({"step": step, "operation": "recapture", "artifacts": ["screenshot", "dom"]})
        elif issue_class == "functional":
            steps.append({"step": step, "operation": "fill_and_submit_forms", "max_forms": 1})
            step += 1
            steps.append({"step": step, "operation": "recapture", "artifacts": ["screenshot", "dom"]})
        else:  # UI
            steps.append({"step": step, "operation": "recapture", "artifacts": ["screenshot", "dom"]})

        return {
            "goal": f"Probe {issue_class} anomaly with severity {severity}",
            "steps": steps,
            "screenshot_path": screenshot_path,
        }

    # ---------- text helpers ----------
    def _build_description(
        self,
        issue_class: str,
        severity: str,
        findings: List[Dict[str, Any]],
        caption: str,
    ) -> str:
        main_msg = ""
        high_first = [f for f in findings if str(f.get("severity", "")).lower() in {"high", "critical"}]
        source = high_first or findings
        if source:
            main_msg = str(source[0].get("message", ""))
        if not main_msg and caption:
            main_msg = caption
        if not main_msg:
            main_msg = "Perception layer detected an anomaly on the page."
        return f"{severity.capitalize()} {issue_class} issue: {main_msg}".strip()

    def _build_repro_steps(
        self,
        url: str,
        viewport: Dict[str, Any],
        issue_class: str,
        findings: List[Dict[str, Any]],
    ) -> List[str]:
        vp_name = viewport.get("name") or viewport.get("device") or "desktop"
        page_label = url or "the target page"
        steps = [f"1. Open {page_label} in a {vp_name} viewport."]
        steps.append("2. Allow the page to fully load.")
        if issue_class == "responsiveness":
            steps.append("3. Resize or switch the viewport to a mobile-width screen.")
            steps.append("4. Observe layout changes and any overlapping or truncated content.")
        elif issue_class == "navigation":
            steps.append("3. Click primary navigation links in the header or nav bar.")
            steps.append("4. Observe unexpected errors, 404 pages, or broken redirects.")
        elif issue_class == "functional":
            steps.append("3. Fill in visible forms with valid data and submit.")
            steps.append("4. Observe whether the expected success path occurs or an error is shown.")
        else:
            steps.append("3. Scroll through the page and focus on key content blocks and hero sections.")
            steps.append("4. Observe visual anomalies such as missing images, low contrast text, or cluttered layout.")
        if findings:
            steps.append("5. Compare what you see with the issue described in the findings.")
        return steps

    def _build_evidence_links(self, screenshot_path: str, obs: Dict[str, Any]) -> List[str]:
        links: List[str] = []
        if screenshot_path:
            links.append(str(screenshot_path))
        dom_path = obs.get("dom_path") or (obs.get("metadata") or {}).get("dom_path")
        if dom_path:
            links.append(str(dom_path))
        return links

    def _map_issue_type(self, issue_class: str) -> str:
        if issue_class in {"UI", "responsiveness"}:
            return "layout"
        if issue_class == "functional":
            return "functional"
        if issue_class == "navigation":
            return "other"
        return "other"

    def _map_schema_severity(self, severity: str) -> str:
        if severity == "critical":
            return "blocker"
        if severity == "high":
            return "critical"
        if severity == "medium":
            return "major"
        if severity == "low":
            return "minor"
        return "minor"

    def _build_viewport_payload(self, viewport: Dict[str, Any]) -> Dict[str, Any]:
        if not viewport:
            return {"width": 0, "height": 0, "device": "unknown"}
        width = int(viewport.get("width", 0) or 0)
        height = int(viewport.get("height", 0) or 0)
        device = viewport.get("name") or viewport.get("device") or "unknown"
        is_mobile = bool(viewport.get("is_mobile", width <= 480))
        return {"width": width, "height": height, "device": device, "is_mobile": is_mobile}

    def _build_title(self, issue_class: str, severity: str, url: str) -> str:
        base = f"{severity.capitalize()} {issue_class} issue"
        if url:
            return f"{base} on {url}"
        return base

    def _render_human_report(self, structured: Dict[str, Any]) -> str:
        if self._can_use_gpt4():
            try:
                return self._render_with_gpt4(structured)
            except Exception:
                pass
        if self._can_use_local_llm():
            try:
                return self._render_with_local_llm(structured)
            except Exception:
                pass
        br = structured["bug_report"]
        lines = [
            br["title"],
            "",
            br["description"],
            "",
            "Steps to reproduce:",
        ]
        for s in br["steps_to_reproduce"]:
            lines.append(f"- {s}")
        if br["evidence_links"]:
            lines.append("")
            lines.append("Evidence:")
            for e in br["evidence_links"]:
                lines.append(f"- {e}")
        return "\n".join(lines)

    def _can_use_gpt4(self) -> bool:
        return ChatOpenAI is not None and bool(os.getenv("OPENAI_API_KEY"))

    def _render_with_gpt4(self, structured: Dict[str, Any]) -> str:
        llm = ChatOpenAI(model_name="gpt-4o-mini", temperature=0.2)
        prompt = (
            "You are a senior QA engineer. Given the following structured JSON describing a web UI bug, "
            "write a concise but clear bug report with a title, description, steps to reproduce, and evidence list.\n"  # noqa: E501
            f"JSON: {json.dumps(structured, ensure_ascii=False)}"
        )
        text = llm.predict(prompt)
        return str(text).strip()

    def _can_use_local_llm(self) -> bool:
        return hf_pipeline is not None and bool(os.getenv("LOCAL_LLM_MODEL"))

    def _render_with_local_llm(self, structured: Dict[str, Any]) -> str:
        model_id = os.getenv("LOCAL_LLM_MODEL")
        if self._local_pipe is None:
            self._local_pipe = hf_pipeline("text-generation", model=model_id)
        prompt = (
            "Generate a short QA-style bug report (title, description, steps, evidence) from this JSON:\n"
            f"{json.dumps(structured, ensure_ascii=False)}"
        )
        out = self._local_pipe(prompt, max_new_tokens=256, do_sample=False)
        text = out[0].get("generated_text", "") if isinstance(out, list) and out else str(out)
        return text.strip()


def analyze_and_plan(perception_json: Dict[str, Any]) -> Tuple[Dict[str, Any], str]:
    orchestrator = AgentOrchestrator()
    return orchestrator.analyze_and_plan(perception_json)
