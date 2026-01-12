"""Configuration module for WebSpector."""
import os
from pathlib import Path
from typing import Literal

# Project paths
PROJECT_ROOT = Path(__file__).parent
CAPTURES_ROOT = Path(os.getenv("CAPTURES_ROOT", PROJECT_ROOT / "captures"))

# Database
DATABASE_URL = os.getenv("DASHBOARD_DATABASE_URL", f"sqlite:///{PROJECT_ROOT / 'dashboard.db'}")

# Dashboard
DASHBOARD_TOKEN = os.getenv("DASHBOARD_TOKEN", "")

# LLM Configuration
LLM_VISION_MODEL = os.getenv("LLM_VISION_MODEL", "llava:13b")  # Default to 13B for RTX 5070 Ti
LLM_TEXT_MODEL = os.getenv("LLM_TEXT_MODEL", "llama3.1")  # For text-only report generation
LLM_ANALYSIS_ENABLED = os.getenv("LLM_ANALYSIS_ENABLED", "true").lower() == "true"

# Model presets for easy switching
MODEL_PRESETS = {
    "fast": {
        "vision": "llava:7b",
        "text": "llama3.1",
        "description": "Fast inference, good quality (8GB VRAM)"
    },
    "balanced": {
        "vision": "llava:13b",
        "text": "llama3.1",
        "description": "Best balance of speed and quality (16GB VRAM)"
    },
    "best": {
        "vision": "llava:34b",
        "text": "llama3.1:70b",
        "description": "Highest quality, slower (32GB+ VRAM)"
    }
}

# Get current preset
LLM_PRESET = os.getenv("LLM_PRESET", "balanced")  # fast, balanced, or best

# Report Settings
REPORT_DETAIL_LEVEL: Literal["quick", "standard", "comprehensive"] = os.getenv(
    "REPORT_DETAIL_LEVEL", "comprehensive"
)
SCREENSHOT_QUALITY: Literal["low", "medium", "high"] = os.getenv("SCREENSHOT_QUALITY", "high")
ACTION_SCREENSHOT_ENABLED = os.getenv("ACTION_SCREENSHOT_ENABLED", "true").lower() == "true"

# Performance Settings
LLM_TIMEOUT_SECONDS = int(os.getenv("LLM_TIMEOUT_SECONDS", "30"))
LLM_MAX_RETRIES = int(os.getenv("LLM_MAX_RETRIES", "3"))
LLM_TEMPERATURE = float(os.getenv("LLM_TEMPERATURE", "0.2"))

# OpenAI (Optional fallback)
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4-vision-preview")

# Feature Flags
USE_OPENAI_FALLBACK = bool(OPENAI_API_KEY)  # Use OpenAI if local LLM fails


def get_current_models():
    """Get the current vision and text models based on preset."""
    if LLM_PRESET in MODEL_PRESETS:
        preset = MODEL_PRESETS[LLM_PRESET]
        return {
            "vision": preset["vision"],
            "text": preset["text"],
            "description": preset["description"]
        }
    # Fallback to environment variables
    return {
        "vision": LLM_VISION_MODEL,
        "text": LLM_TEXT_MODEL,
        "description": "Custom configuration"
    }


def print_config():
    """Print current configuration for debugging."""
    models = get_current_models()
    print("=" * 60)
    print("WebSpector Configuration")
    print("=" * 60)
    print(f"LLM Preset: {LLM_PRESET}")
    print(f"Vision Model: {models['vision']}")
    print(f"Text Model: {models['text']}")
    print(f"Description: {models['description']}")
    print(f"LLM Analysis: {'Enabled' if LLM_ANALYSIS_ENABLED else 'Disabled'}")
    print(f"Report Detail: {REPORT_DETAIL_LEVEL}")
    print(f"Screenshot Quality: {SCREENSHOT_QUALITY}")
    print(f"Action Screenshots: {'Enabled' if ACTION_SCREENSHOT_ENABLED else 'Disabled'}")
    print("=" * 60)


if __name__ == "__main__":
    print_config()
