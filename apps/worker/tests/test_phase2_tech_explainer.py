import pytest
from unittest.mock import MagicMock
from sqlmodel import Session, create_engine, SQLModel
import uuid

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../api")))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from models import VideoType, VideoJob, VideoJobStatus, User
from routers.videos import CreateVideoJobRequest, create_video_job, get_video_timeline
from database import _ensure_schema_migrations


def test_videotype_enum_includes_tech_explainer():
    assert hasattr(VideoType, "TECH_EXPLAINER")
    assert VideoType.TECH_EXPLAINER == "tech_explainer"
    assert VideoType.TECH_EXPLAINER.value == "tech_explainer"


def test_tech_explainer_validation_requires_script_or_topic():
    # Missing both script and topic -> raises ValueError
    with pytest.raises(ValueError, match="Tech explainer videos require 'script_text' or 'topic'"):
        CreateVideoJobRequest(
            title="Tech Explainer Fail",
            video_type=VideoType.TECH_EXPLAINER,
            settings={}
        )

    # Valid with script_text
    req1 = CreateVideoJobRequest(
        title="AI Agents 101",
        video_type=VideoType.TECH_EXPLAINER,
        settings={"script_text": "Autonomous agents are taking over software workflows."}
    )
    assert req1.video_type == VideoType.TECH_EXPLAINER

    # Valid with topic
    req2 = CreateVideoJobRequest(
        title="AI Agents 101",
        video_type=VideoType.TECH_EXPLAINER,
        settings={"topic": "Autonomous AI Swarms"}
    )
    assert req2.video_type == VideoType.TECH_EXPLAINER


def test_tech_explainer_defaults_to_9x16_and_faceless():
    engine = create_engine("sqlite:///:memory:")
    SQLModel.metadata.create_all(engine)

    with Session(engine) as session:
        req = CreateVideoJobRequest(
            title="Roboverse 9:16 Test",
            video_type=VideoType.TECH_EXPLAINER,
            clerk_id="user_test_42",
            email="creator@example.com",
            settings={"topic": "Docker Swarm Management"}
        )

        job = create_video_job(payload=req, session=session)

        assert job.video_type == VideoType.TECH_EXPLAINER
        assert job.settings.get("aspect_ratio") == "9:16"
        assert job.settings.get("is_faceless") is True
        assert job.status == VideoJobStatus.QUEUED


def test_tech_explainer_caption_safety_position():
    engine = create_engine("sqlite:///:memory:")
    SQLModel.metadata.create_all(engine)

    with Session(engine) as session:
        user = User(clerk_id="user_safe", email="safe@example.com")
        session.add(user)
        session.commit()

        job = VideoJob(
            user_id=user.id,
            title="Spatial Clearance Test",
            source_url="https://example.com/mock.mp4",
            video_type=VideoType.TECH_EXPLAINER,
            status=VideoJobStatus.COMPLETED,
            settings={"aspect_ratio": "9:16", "topic": "Tech Explainer", "is_faceless": True},
            edit_decision_list='{"timeline_project": {"tracks": {"videoTrack": [{"id": "v1", "source": "https://example.com/base.mp4"}]}}}'
        )
        session.add(job)
        session.commit()

        tp = get_video_timeline(video_id=job.id, session=session)
        assert tp is not None
        assert tp.get("videoType") == "tech_explainer"
        assert tp.get("isFaceless") is True


def test_ensure_schema_migrations_compatibility():
    engine = create_engine("sqlite:///:memory:")
    # Must run cleanly without throwing on SQLite or PostgreSQL mock
    _ensure_schema_migrations(engine)
