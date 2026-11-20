import os
import sys
import subprocess
from services.compositor import composite_insta_reel
from services.subtitle_generator import generate_ass_subtitles


def main():
    source_video = "/tmp/sample_probe/raw_desktop_input.mp4"
    if not os.path.exists(source_video):
        print(f"Error: source video not found at {source_video}")
        return 1

    out_dir = "sample_video"
    os.makedirs(out_dir, exist_ok=True)
    frames_dir = os.path.join(out_dir, "insta_reel_frames")
    os.makedirs(frames_dir, exist_ok=True)

    output_mp4 = os.path.join(out_dir, "insta_reel_sample_render.mp4")
    subtitle_ass = os.path.join(out_dir, "insta_reel_sample.ass")

    timestamp_map = {
        "chunk_1": {
            "start": 0.0,
            "end": 2.2,
            "text": "HOW DO AUTONOMOUS AI AGENTS WORK",
            "words": [
                {"word": "HOW", "start": 0.0, "end": 0.3},
                {"word": "DO", "start": 0.3, "end": 0.6},
                {"word": "AUTONOMOUS", "start": 0.6, "end": 1.2},
                {"word": "AI", "start": 1.2, "end": 1.5},
                {"word": "AGENTS", "start": 1.5, "end": 1.9},
                {"word": "WORK", "start": 1.9, "end": 2.2},
            ]
        },
        "chunk_2": {
            "start": 2.3,
            "end": 5.0,
            "text": "WITHOUT EVER HALLUCINATING IN PRODUCTION",
            "words": [
                {"word": "WITHOUT", "start": 2.3, "end": 2.8},
                {"word": "EVER", "start": 2.8, "end": 3.3},
                {"word": "HALLUCINATING", "start": 3.3, "end": 4.1},
                {"word": "IN", "start": 4.1, "end": 4.4},
                {"word": "PRODUCTION", "start": 4.4, "end": 5.0},
            ]
        }
    }

    print("[1/3] Generating docked ASS subtitles for Insta Reel...")
    generate_ass_subtitles(
        timestamp_map=timestamp_map,
        output_ass_path=subtitle_ass,
        caption_preset="insta_reel",
        aspect_ratio="9:16",
        is_insta_reel=True,
    )

    print(f"[2/3] Compositing Insta Reel into {output_mp4}...")
    composite_insta_reel(
        source_video_path=source_video,
        output_mp4_path=output_mp4,
        subtitle_ass_path=subtitle_ass,
        settings={"is_insta_reel": True, "video_style": "insta_reel"}
    )

    print("[3/3] Extracting verification frames...")
    subprocess.run([
        "ffmpeg", "-y", "-ss", "00:00:01.000", "-i", output_mp4,
        "-vframes", "1", "-q:v", "2",
        os.path.join(frames_dir, "frame_01s.png")
    ], check=True)

    subprocess.run([
        "ffmpeg", "-y", "-ss", "00:00:03.500", "-i", output_mp4,
        "-vframes", "1", "-q:v", "2",
        os.path.join(frames_dir, "frame_03s.png")
    ], check=True)

    file_size_mb = os.path.getsize(output_mp4) / (1024 * 1024)
    print(f"SUCCESS: Rendered Insta Reel ({file_size_mb:.2f} MB)")
    print(f"Frames saved to: {frames_dir}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
