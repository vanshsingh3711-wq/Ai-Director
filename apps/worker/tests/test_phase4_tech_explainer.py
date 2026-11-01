import os
import pytest
from services.treatment_assigner import infer_suggested_template, assign_visual_treatments
from services.remotion_renderer import ALLOWED_COMPOSITIONS, build_props_from_edit
from services.subtitle_generator import generate_ass_subtitles
from services.motion_graphic_planner import ALLOWED_TEMPLATES, REMOTION_ONLY_TEMPLATES


def test_infer_suggested_template_mobile_and_backend():
    """Verify script-aware heuristic maps to Option C and Option B accurately."""
    # Option C: Mobile Phone
    beat_mobile_1 = {
        "text": "First, your smartphone triggers the request through a lightweight mobile assistant.",
        "focus_phrase": "smartphone mobile assistant",
        "role": "point"
    }
    assert infer_suggested_template(beat_mobile_1) == "device_mockup_phone"

    beat_mobile_2 = {
        "text": "Open the iOS messaging app and send a quick prompt to the bot.",
        "focus_phrase": "ios messaging app bot",
        "role": "point"
    }
    assert infer_suggested_template(beat_mobile_2) == "device_mockup_phone"

    # Option B: Isometric Window / Card Deck
    beat_backend_1 = {
        "text": "Behind the scenes, the orchestrator spins up isolated Docker containers.",
        "focus_phrase": "orchestrator isolated Docker containers",
        "role": "point"
    }
    assert infer_suggested_template(beat_backend_1) == "isometric_card_deck"

    beat_backend_2 = {
        "text": "Every terminal command executes safely inside a sandboxed Kubernetes cluster.",
        "focus_phrase": "terminal command Kubernetes cluster",
        "role": "point"
    }
    assert infer_suggested_template(beat_backend_2) == "isometric_card_deck"

    # Orbital Agent Nucleus
    beat_nucleus = {
        "text": "At the center lies the autonomous core reasoning nucleus.",
        "focus_phrase": "core reasoning nucleus",
        "role": "point"
    }
    assert infer_suggested_template(beat_nucleus) == "orbital_agent_badge"


def test_assign_visual_treatments_tech_explainer():
    """Verify tech explainer receives 100% studio motion graphics with zero b-roll demotions."""
    beat_sheet = {
        "beats": [
            {
                "id": 1,
                "start": 0.0,
                "end": 3.0,
                "text": "How do autonomous AI agents actually execute real-world tasks?",
                "role": "hook",
                "importance": 3,
                "concreteness": "abstract",
            },
            {
                "id": 2,
                "start": 3.0,
                "end": 7.0,
                "text": "First, your smartphone triggers the request through a lightweight mobile assistant.",
                "role": "point",
                "importance": 2,
                "concreteness": "concrete",  # Would be b-roll in normal videos
            },
            {
                "id": 3,
                "start": 7.0,
                "end": 12.0,
                "text": "Behind the scenes, the orchestrator spins up isolated Docker containers.",
                "role": "point",
                "importance": 2,
                "concreteness": "concrete",  # Would be b-roll in normal videos
            },
            {
                "id": 4,
                "start": 12.0,
                "end": 16.0,
                "text": "A recursive reasoning loop checks every terminal command against a deterministic test suite.",
                "role": "point",
                "importance": 1,
                "concreteness": "abstract",
            },
        ]
    }

    settings = {
        "is_faceless": False,
        "is_tech_explainer": True,
        "MAX_OVERLAYS_PER_MIN": 8,
        "MIN_OVERLAY_DURATION": 2.0,
        "MAX_OVERLAY_DURATION": 6.0,
    }

    updated_sheet, _ = assign_visual_treatments(beat_sheet, 16.0, settings)
    beats = updated_sheet["beats"]

    # All beats must be motion graphics or kinetic text (NO b_roll or none)
    for b in beats:
        assert b["treatment"] in ("motion_graphic", "kinetic_text"), f"Beat {b['id']} had treatment {b['treatment']}"

    # Verify template suggestions
    assert beats[1]["suggested_template"] == "device_mockup_phone"
    assert beats[2]["suggested_template"] == "isometric_card_deck"
    assert beats[3]["suggested_template"] in ("isometric_card_deck", "tactile_checklist_stamp")


def test_remotion_composition_and_props():
    """Verify composition registrations and prop translation in remotion_renderer."""
    # Ensure allowed compositions include the 3D pack
    for comp in ["device_mockup_phone", "isometric_card_deck", "orbital_agent_badge"]:
        assert comp in ALLOWED_COMPOSITIONS
        assert comp in ALLOWED_TEMPLATES
        assert comp in REMOTION_ONLY_TEMPLATES

    # Test prop translation for device_mockup_phone
    phone_edit = {
        "motion_graphics_type": "device_mockup_phone",
        "motion_graphics_targets": {
            "appTitle": "Autonomous Agent",
            "botName": "Claude Agent",
            "accentColor": "#00e5ff",
        }
    }
    phone_props = build_props_from_edit(phone_edit)
    assert phone_props.get("appTitle") == "Autonomous Agent"
    assert phone_props.get("botName") == "Claude Agent"
    assert phone_props.get("accentColor") == "#00e5ff"

    # Test prop translation for isometric_card_deck
    deck_edit = {
        "motion_graphics_type": "isometric_card_deck",
        "motion_graphics_targets": {
            "headline": "SWARM CLUSTERS",
            "subheadline": "ISOLATED DOCKER WORKERS",
            "accentColor": "#a855f7",
        }
    }
    deck_props = build_props_from_edit(deck_edit)
    assert deck_props.get("headline") == "SWARM CLUSTERS"
    assert deck_props.get("subheadline") == "ISOLATED DOCKER WORKERS"
    assert deck_props.get("accentColor") == "#a855f7"


def test_tech_explainer_subtitles_lower_third(tmp_path):
    """Verify Tech Explainer subtitles are generated with Alignment=2 in lower-third."""
    timestamp_map = {
        "ID_01": {
            "start": 0.5,
            "end": 2.5,
            "text": "How do autonomous agents work?",
            "words": [
                {"word": "How", "start": 0.5, "end": 0.8},
                {"word": "do", "start": 0.8, "end": 1.1},
                {"word": "autonomous", "start": 1.1, "end": 1.8},
                {"word": "agents", "start": 1.8, "end": 2.1},
                {"word": "work?", "start": 2.1, "end": 2.5},
            ]
        }
    }

    out_ass = str(tmp_path / "test_explainer.ass")
    generate_ass_subtitles(
        timestamp_map=timestamp_map,
        output_ass_path=out_ass,
        caption_preset="modern_clean",
        aspect_ratio="9:16",
        is_faceless=True,
        alignment=2,  # Tech Explainer lower-third override
    )

    assert os.path.exists(out_ass)
    with open(out_ass, "r", encoding="utf-8") as f:
        content = f.read()

    # Must specify PlayRes 1080x1920
    assert "PlayResX: 1080" in content
    assert "PlayResY: 1920" in content
    # Style line must specify Alignment 2 (lower-third)
    assert ",2,40,40,160,1" in content or "Alignment=2" in content or r"\an2\pos" in content
    # Dialogue lines must place subtitles at lower third (y >= 1600)
    assert r"\an2\pos(540,1760)" in content

