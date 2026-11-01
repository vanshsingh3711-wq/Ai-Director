import os
import sys
import uuid
import time
import shutil
import subprocess

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
sys.path.insert(0, os.path.join(ROOT_DIR, "apps", "api"))
sys.path.insert(0, os.path.join(ROOT_DIR, "apps", "worker"))

os.chdir(os.path.join(ROOT_DIR, "apps", "worker"))

from database import get_session
from models import VideoJob, VideoJobStatus, VideoType, User
from tasks.video_pipeline import process_video_pipeline

SCRIPT_TEXT = (
    "Chatbots just talk. AI agents actually do the work. "
    "Instead of answering a prompt and stopping, an AI agent runs on an autonomous four-step loop. "
    "First, Perception: the agent ingests your goal, analyzes the environment, and reads your files. "
    "Second, Recursive Reasoning: it breaks the big mission down into step-by-step sub-tasks. "
    "Third, Tool Execution: the agent calls APIs, writes code, and runs commands in a live terminal. "
    "And fourth, Self-Correction: when code breaks, it inspects the error, rewrites the syntax, and tests until it passes. "
    "Combine specialized agents into a synchronized swarm—a planner, coder, and reviewer—and you have an autonomous engineering team running twenty-four seven. "
    "Stop doing manual toil. Direct the agents, and let autonomous compute build the future."
)

def main():
    print("[*] Connecting to database...")
    session = next(get_session())

    # Ensure default user
    user = session.query(User).filter(User.clerk_id == "user_default").first()
    if not user:
        user = User(
            clerk_id="user_default",
            email="developer@example.com",
            first_name="Developer",
            last_name="Admin"
        )
        session.add(user)
        session.commit()
        session.refresh(user)

    job_id = uuid.uuid4()
    job_settings = {
        "topic": "How Autonomous AI Agents Work",
        "script": SCRIPT_TEXT,
        "niche": "Technology",
        "theme": "dark",
        "aspect_ratio": "9:16",
        "mood": "Energetic",
        "video_style": "viral",
        "ai_model": "DeepSeek-Chat",
        "directing_mode": "auto",
        "tts_voice": "en-US-ChristopherNeural",
        "caption_preset": "tiktok_yellow",
        "USE_GRANULAR_OVERLAYS": True,
        "use_3d_avatar": False,
    }

    job = VideoJob(
        id=job_id,
        user_id=user.id,
        title="How Autonomous AI Agents Work",
        source_url="",
        video_type=VideoType.FACELESS_SHORT,
        status=VideoJobStatus.QUEUED,
        settings=job_settings,
    )

    session.add(job)
    session.commit()
    session.close()

    print(f"\n========================================================")
    print(f"🚀 SUBMITTING SCRIPT TO WORKER PIPELINE (Job ID: {job_id})")
    print(f"========================================================\n")

    start_t = time.time()
    # Trigger Celery worker pipeline
    result = process_video_pipeline.apply(args=[str(job_id)])
    res_val = result.get()
    elapsed = time.time() - start_t

    print(f"\n🎉 WORKER FINISHED in {elapsed:.1f}s!")
    print(f"Pipeline Result: {res_val}")

    # Check the final file
    worker_output = os.path.join(ROOT_DIR, "media_temp", f"{job_id}.mp4")
    master_copy = os.path.join(ROOT_DIR, "worker_ai_agents_video.mp4")
    web_copy = os.path.join(ROOT_DIR, "apps", "web", "public", "worker_ai_agents_video.mp4")

    if os.path.exists(worker_output):
        shutil.copy2(worker_output, master_copy)
        shutil.copy2(worker_output, web_copy)
        print(f"\n📁 Final Worker Master Video: {master_copy} ({os.path.getsize(master_copy) / 1024 / 1024:.2f} MB)")
        print(f"📁 Web Stream Video:         {web_copy}")

        # Extract 5 preview frames
        previews_dir = os.path.join(ROOT_DIR, "media_temp", "worker_job_previews")
        os.makedirs(previews_dir, exist_ok=True)
        for t_sec in [3, 12, 25, 35, 48]:
            frame_path = os.path.join(previews_dir, f"frame_{t_sec}s.jpg")
            subprocess.run([
                "ffmpeg", "-y", "-ss", str(t_sec), "-i", master_copy,
                "-vframes", "1", "-q:v", "2", frame_path
            ], capture_output=True)
            if os.path.exists(frame_path):
                print(f"  [✓] Extracted snapshot @ {t_sec}s -> {frame_path}")
    else:
        print(f"[!] Warning: Expected output not found at {worker_output}")

if __name__ == "__main__":
    main()

