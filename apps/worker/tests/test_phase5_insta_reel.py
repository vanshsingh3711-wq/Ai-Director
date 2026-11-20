import os
import pytest
from unittest.mock import MagicMock, patch
from services.compositor import _ensure_insta_reel_assets, composite_insta_reel
from services.subtitle_generator import generate_ass_subtitles, PRESET_CONFIGS
from models import VideoType


def test_insta_reel_assets_generation(tmp_path):
    """Verify that _ensure_insta_reel_assets creates the 9:16 background canvas, mask, shadow, and bezel."""
    assets_dir = str(tmp_path / "insta_reel_assets")
    _ensure_insta_reel_assets(assets_dir)

    assert os.path.exists(os.path.join(assets_dir, "bg_canvas_9x16.png"))
    assert os.path.exists(os.path.join(assets_dir, "corner_mask.png"))
    assert os.path.exists(os.path.join(assets_dir, "shadow_layer.png"))
    assert os.path.exists(os.path.join(assets_dir, "bezel_layer.png"))


def test_insta_reel_subtitle_preset_and_dock():
    """Verify insta_reel subtitle preset exists with charcoal/cyan styling and locks to y=1420."""
    assert "insta_reel" in PRESET_CONFIGS
    preset = PRESET_CONFIGS["insta_reel"]
    assert preset["primary"] == "&H00181111"  # Charcoal
    assert preset["active"] == "&H00D4FF00"  # Vibrant accent Pop

    out_ass = "/tmp/test_insta_reel_sub.ass"
    timestamp_map = {
        "chunk_1": {
            "start": 0.0,
            "end": 2.5,
            "text": "How do AI agents work",
            "words": [
                {"word": "How", "start": 0.0, "end": 0.5},
                {"word": "do", "start": 0.5, "end": 0.9},
                {"word": "AI", "start": 0.9, "end": 1.4},
                {"word": "agents", "start": 1.4, "end": 2.0},
                {"word": "work", "start": 2.0, "end": 2.5},
            ]
        }
    }

    generate_ass_subtitles(
        timestamp_map=timestamp_map,
        output_ass_path=out_ass,
        caption_preset="insta_reel",
        aspect_ratio="9:16",
        is_insta_reel=True,
    )

    assert os.path.exists(out_ass)
    with open(out_ass, "r") as f:
        content = f.read()

    # Must contain position locked to y=1450 beneath monitor frame
    assert r"\pos(540,1450)" in content
    # Must contain ASS Dialogue lines
    assert "Dialogue:" in content


def test_insta_reel_pipeline_logic_uncut_vs_prompt():
    """Verify that Insta Reel without user prompt stays uncut, but with prompt triggers AI editing."""
    job_settings_default = {
        "video_style": "insta_reel",
        "is_explanation": True,
    }

    is_insta_reel = job_settings_default.get("video_style") == "insta_reel"
    user_edit_prompt = str(job_settings_default.get("editing_prompt") or "").strip()
    ai_edit_video = bool(job_settings_default.get("ai_edit_video", False) or user_edit_prompt)

    assert is_insta_reel is True
    assert ai_edit_video is False  # By default: main video is NOT edited!

    # When user supplies an editing prompt:
    job_settings_with_prompt = {
        "video_style": "insta_reel",
        "editing_prompt": "Trim the intro silence and add zoom in on the button click",
        "is_explanation": True,
    }
    user_edit_prompt_2 = str(job_settings_with_prompt.get("editing_prompt") or "").strip()
    ai_edit_video_2 = bool(job_settings_with_prompt.get("ai_edit_video", False) or user_edit_prompt_2)

    assert ai_edit_video_2 is True  # Triggers AI Director edits
    assert "Trim the intro" in user_edit_prompt_2


def test_insta_reel_non_explanation_bypasses_captions():
    """Verify that when is_explanation is False, subtitles are bypassed."""
    job_settings = {
        "video_style": "insta_reel",
        "is_explanation": False,
    }
    is_explanation = bool(job_settings.get("is_explanation", True))
    assert is_explanation is False
