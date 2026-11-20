#!/usr/bin/env python3
import os
import sys
import time

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "apps", "worker"))

from services.compositor import composite_insta_reel

def batch_render_insta_reel(input_dir: str = "/home/vansh/Videos", output_dir: str = "/home/vansh/Videos/Insta_Reel_Edits"):
    os.makedirs(output_dir, exist_ok=True)
    
    # Valid video extensions
    valid_exts = {".mp4", ".webm", ".mov", ".mkv"}
    
    # List files directly in input_dir (ignore subdirectories like output_dir)
    entries = sorted(os.listdir(input_dir))
    video_files = [
        f for f in entries
        if os.path.isfile(os.path.join(input_dir, f)) and os.path.splitext(f)[1].lower() in valid_exts
    ]
    
    total = len(video_files)
    print(f"\n==================================================")
    print(f"🎬 Insta Reel Batch Video Processor")
    print(f"📁 Source: {input_dir}")
    print(f"📁 Target: {output_dir}")
    print(f"📼 Total Videos Found: {total}")
    print(f"==================================================\n")
    
    results = []
    total_start = time.time()
    
    for idx, fname in enumerate(video_files, 1):
        src_path = os.path.join(input_dir, fname)
        base_name, _ = os.path.splitext(fname)
        out_fname = f"{base_name}_insta_reel.mp4"
        out_path = os.path.join(output_dir, out_fname)
        
        print(f"[{idx}/{total}] ⏳ Processing: '{fname}'...")
        t0 = time.time()
        
        try:
            composite_insta_reel(
                source_video_path=src_path,
                output_mp4_path=out_path,
                subtitle_ass_path=None,  # No captions requested by user
            )
            elapsed = time.time() - t0
            size_mb = os.path.getsize(out_path) / (1024 * 1024)
            print(f"[{idx}/{total}] ✅ Finished in {elapsed:.1f}s -> {out_fname} ({size_mb:.2f} MB)\n")
            results.append({
                "source": fname,
                "output": out_fname,
                "status": "SUCCESS",
                "time_sec": elapsed,
                "size_mb": size_mb,
            })
        except Exception as e:
            elapsed = time.time() - t0
            print(f"[{idx}/{total}] ❌ Failed after {elapsed:.1f}s: {e}\n")
            results.append({
                "source": fname,
                "output": out_fname,
                "status": f"FAILED: {e}",
                "time_sec": elapsed,
                "size_mb": 0,
            })

    total_elapsed = time.time() - total_start
    print(f"==================================================")
    print(f"🎉 Batch Processing Complete in {total_elapsed:.1f}s!")
    print(f"==================================================")
    for r in results:
        print(f"- {r['source']} -> {r['output']} [{r['status']}] ({r['size_mb']:.1f} MB, {r['time_sec']:.1f}s)")
    print(f"==================================================\n")

if __name__ == "__main__":
    batch_render_insta_reel()
