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

FINANCE_SCRIPT_TEXT = (
    "Most people think becoming wealthy is about saving every penny in a bank account. "
    "That is a trap. "
    "Every year, inflation quietly devours your purchasing power, turning your cash into dead weight. "
    "The top one percent play by a completely different playbook: The Velocity of Money. "
    "Instead of hoarding cash, they split their capital into three distinct engines. "
    "First, The Liquidity Buffer: three to six months of expenses in high-yield cash for emergency defense. "
    "Second, Compound Accelerators: index funds and cash-flowing assets that double your money every seven years through the Rule of 72. "
    "And third, Asymmetric Upside: calculated investments with capped downside and 100x potential. "
    "Your cash is not a trophy to hoard; it is an army of employees. "
    "Put every dollar to work, deploy for velocity, and let compounding build true financial freedom."
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

    job_id = uuid.UUID("2efd0ec7-88e6-4e5a-b3d7-e8e983f2d86c")
    existing_job = session.get(VideoJob, job_id)
    if not existing_job:
        job_settings = {
            "topic": "The Velocity of Wealth: Why Saving Cash Makes You Poor",
            "script": FINANCE_SCRIPT_TEXT,
            "niche": "Finance",
            "theme": "dark",
            "aspect_ratio": "9:16",
            "mood": "authoritative",
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
            title="The Velocity of Wealth: Why Saving Cash Makes You Poor",
            source_url="",
            video_type=VideoType.FACELESS_SHORT,
            status=VideoJobStatus.QUEUED,
            settings=job_settings,
        )

        session.add(job)
        session.commit()
    session.close()

    print(f"\n========================================================")
    print(f"🚀 SUBMITTING FINANCE SCRIPT TO WORKER PIPELINE")
    print(f"Job ID: {job_id}")
    print(f"Script ({len(FINANCE_SCRIPT_TEXT.split())} words): {FINANCE_SCRIPT_TEXT[:80]}...")
    print(f"========================================================\n")

    start_t = time.time()
    # Execute Celery worker pipeline synchronously
    result = process_video_pipeline.apply(args=[str(job_id)])
    res_val = result.get()
    elapsed = time.time() - start_t

    print(f"\n🎉 WORKER FINISHED in {elapsed:.1f}s ({elapsed/60:.1f} mins)!")
    print(f"Pipeline Result: {res_val}")

    # Check the final file
    worker_temp_dir = os.path.join(ROOT_DIR, "media_temp", str(job_id))
    rendered_file = os.path.join(worker_temp_dir, "final_rendered.mp4")
    master_copy = os.path.join(ROOT_DIR, "finance_wealth_velocity_1min.mp4")
    web_copy = os.path.join(ROOT_DIR, "apps", "web", "public", "finance_wealth_velocity_1min.mp4")

    if os.path.exists(rendered_file):
        shutil.copy2(rendered_file, master_copy)
        shutil.copy2(rendered_file, web_copy)
        size_mb = os.path.getsize(master_copy) / (1024 * 1024)
        print(f"\n📁 Final Worker Master Video: {master_copy} ({size_mb:.2f} MB)")
        print(f"📁 Web Stream Video:         {web_copy}")

        # Extract 6 snapshot preview frames across the timeline
        previews_dir = os.path.join(ROOT_DIR, "media_temp", "finance_worker_previews")
        os.makedirs(previews_dir, exist_ok=True)
        dur_proc = subprocess.run([
            "ffprobe", "-v", "error", "-show_entries", "format=duration",
            "-of", "default=noprint_wrappers=1:nokey=1", master_copy
        ], capture_output=True, text=True)
        dur = float(dur_proc.stdout.strip()) if dur_proc.stdout.strip() else 54.0

        sample_points = [
            (3.0, "frame_03s_hook.jpg"),
            (12.0, "frame_12s_inflation.jpg"),
            (24.0, "frame_24s_velocity.jpg"),
            (34.0, "frame_34s_liquidity.jpg"),
            (44.0, "frame_44s_compound.jpg"),
            (min(52.0, dur - 2.0), "frame_52s_freedom.jpg"),
        ]
        for t_sec, fname in sample_points:
            out_frame = os.path.join(previews_dir, fname)
            subprocess.run([
                "ffmpeg", "-y", "-ss", str(t_sec), "-i", master_copy,
                "-vframes", "1", "-q:v", "2", out_frame
            ], capture_output=True)
            if os.path.exists(out_frame):
                print(f"  [✓] Extracted snapshot @ {t_sec}s -> {fname}")
    else:
        print(f"[!] Warning: Rendered output not found at {rendered_file}")

if __name__ == "__main__":
    main()

