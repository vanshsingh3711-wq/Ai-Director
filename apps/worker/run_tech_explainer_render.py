import os
import sys
import uuid
import time
import subprocess
import shutil
from pathlib import Path

# Load environment
from dotenv import load_dotenv
load_dotenv(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".env")))

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "api")))
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from database import get_session
from models import VideoJob, VideoJobStatus, VideoType, User
from tasks.video_pipeline import process_video_pipeline


def get_session_with_retry(max_attempts: int = 3, delay: float = 2.0):
    for attempt in range(max_attempts):
        try:
            return next(get_session())
        except Exception as e:
            if attempt == max_attempts - 1:
                raise
            print(f"[*] DB connection attempt {attempt + 1} retrying in {delay}s: {e}")
            time.sleep(delay)


def run_benchmark_tech_explainer():
    session = get_session_with_retry()

    # Ensure a default user exists
    user = session.query(User).filter(User.clerk_id == "user_default").first()
    if not user:
        user = User(
            clerk_id="user_default",
            email="test@example.com",
            first_name="Test",
            last_name="User",
        )
        session.add(user)
        session.commit()
        session.refresh(user)

    # Script carefully designed to test:
    # 1. Introduction / hook question
    # 2. Agent Nucleus: Autonomous reasoning nucleus (orbital_agent_badge)
    # 3. Option C: Mobile assistant on smartphone (device_mockup_phone)
    # 4. Option B: Docker containers & orchestrator (isometric_card_deck)
    # 5. Terminal execution against deterministic test suite (isometric_card_deck)
    # 6. Security sentinel 42ms isolation metric (metric_reveal)
    # 7. Self-healing developer swarms conclusion
    test_script = (
        "How do autonomous AI agents actually execute real-world tasks without hallucinating? "
        "At the foundational level, every decision originates from an autonomous reasoning nucleus. "
        "First, your smartphone triggers the mission through a lightweight mobile assistant. "
        "Behind the scenes, the orchestrator spins up isolated Docker containers across the cluster. "
        "A recursive reasoning loop checks every terminal command against a deterministic test suite before execution. "
        "And if an anomaly occurs, the security sentinel isolates the container in forty-two milliseconds. "
        "This is how modern software builds autonomous, self-healing developer swarms."
    )

    settings = {
        "topic": "Autonomous AI Agent Architecture",
        "script": test_script,
        "character": "sarah",
        "niche": "Technology",
        "theme": "dark",
        "aspect_ratio": "9:16",
        "mood": "Technical",
        "video_style": "viral",
        "ai_model": "DeepSeek-Chat",
        "caption_preset": "modern_clean",
        "USE_GRANULAR_OVERLAYS": True,
        "is_faceless": True,
        "continuous_composition": True,
        "SINGLE_PASS_COMPOSITION": True,
        "is_tech_explainer": True,
    }

    job_id = uuid.uuid4()
    job = VideoJob(
        id=job_id,
        user_id=user.id,
        title="Autonomous AI Agents Architecture (Roboverse Style)",
        source_url="",
        video_type=VideoType.TECH_EXPLAINER,
        status=VideoJobStatus.QUEUED,
        settings=settings,
    )

    session.add(job)
    session.commit()
    print(f"\n=======================================================")
    print(f"[*] Created TECH_EXPLAINER Video Job: {job_id}")
    print(f"[*] Video Type: {job.video_type}")
    print(f"[*] Aspect Ratio: {settings['aspect_ratio']}")
    print(f"[*] AI Model: {settings['ai_model']}")
    print(f"[*] Script length: {len(test_script.split())} words")
    print(f"=======================================================\n")
    session.close()

    print("[*] Launching process_video_pipeline synchronously...")
    start_time = time.time()
    result = process_video_pipeline.apply(args=[str(job_id)])
    output = result.get()
    elapsed = time.time() - start_time

    print(f"\n🎉 PIPELINE FINISHED in {elapsed:.1f}s!")
    print(f"Result: {output}")

    s = get_session_with_retry()
    final_job = s.query(VideoJob).filter(VideoJob.id == job_id).first()
    if not final_job:
        print("[!] Job not found in DB after completion!")
        return

    print(f"[*] Final Status: {final_job.status}")
    print(f"[*] Rendered URL: {final_job.rendered_url}")
    
    # Destination in sample_video directory
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
    sample_dir = os.path.join(project_root, "sample_video")
    os.makedirs(sample_dir, exist_ok=True)
    target_mp4 = os.path.join(sample_dir, "tech_explainer_9x16.mp4")

    # Local file path for validation
    from config import settings as worker_settings
    local_candidates = [
        os.path.join(worker_settings.TEMP_DIR, str(job_id), "final_rendered.mp4"),
        final_job.rendered_url or "",
    ]
    local_mp4 = None
    for cand in local_candidates:
        if cand and os.path.exists(cand):
            local_mp4 = cand
            break

    if local_mp4 and os.path.exists(local_mp4):
        shutil.copyfile(local_mp4, target_mp4)
        print(f"[*] Copied final video to: {target_mp4} ({os.path.getsize(target_mp4) / (1024*1024):.2f} MB)")

        # Verify dimensions with ffprobe
        probe_cmd = [
            "ffprobe", "-v", "error", "-select_streams", "v:0",
            "-show_entries", "stream=width,height,duration,r_frame_rate",
            "-of", "default=noprint_wrappers=1", local_mp4
        ]
        probe_res = subprocess.run(probe_cmd, capture_output=True, text=True)
        print("\n[*] Video Stream Properties:")
        print(probe_res.stdout.strip())

        # Extract validation frames across the timeline
        frames_dir = os.path.join(project_root, "sample_video", "tech_explainer_frames")
        os.makedirs(frames_dir, exist_ok=True)
        artifact_frames_dir = "/home/vansh/.gemini/antigravity/brain/1725d150-289e-43ff-a5fb-c82b28f7c0ef/tech_explainer_renders"
        os.makedirs(artifact_frames_dir, exist_ok=True)

        scenes_map = [
            (2, "scene1_02s_orbital_nucleus"),
            (7, "scene2_07s_exploded_layers"),
            (13, "scene3_13s_phone_mockup"),
            (18, "scene4_18s_docker_cluster"),
            (25, "scene5_25s_deterministic_tests"),
            (31, "scene6_31s_security_sentinel"),
            (37, "scene7_37s_developer_swarms"),
        ]

        for sec, name in scenes_map:
            frame_out = os.path.join(frames_dir, f"{name}.png")
            extract_cmd = [
                "ffmpeg", "-y", "-ss", str(sec), "-i", local_mp4,
                "-vframes", "1", "-q:v", "2", frame_out
            ]
            subprocess.run(extract_cmd, capture_output=True)
            if os.path.exists(frame_out):
                artifact_frame = os.path.join(artifact_frames_dir, f"{name}.png")
                shutil.copyfile(frame_out, artifact_frame)
                print(f"[*] Extracted frame at {sec}s ({name}) -> {frame_out} ({os.path.getsize(frame_out) // 1024} KB)")

    s.close()


if __name__ == "__main__":
    run_benchmark_tech_explainer()
