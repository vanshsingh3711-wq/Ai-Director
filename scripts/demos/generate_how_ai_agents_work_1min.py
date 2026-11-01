"""
generate_how_ai_agents_work_1min.py

High-retention, cinematic 1-minute viral Tech Reel (9:16 vertical 1080x1920):
"How AI Agents Actually Work: From Chatbots to Autonomous Cognitive Loops"

Pipeline:
1. Neural Edge TTS voiceover (en-US-ChristopherNeural at +8% rate ~53.6s duration)
2. Faster-Whisper word-level transcription with ASS yellow-highlight karaoke subtitles
3. High-definition B-rolls & dark cyberpunk grid canvas
4. 4 Remotion Motion Graphics Overlays:
   - ArchitecturePipeline (Perception -> Recursive Reasoning -> Tool Invocation -> Self-Correction)
   - CodeReveal (Python agent calling live tools and terminal pytest execution)
   - TactileChecklistStamp (Self-healing error detection -> Stack trace patch -> 100% test pass)
   - MindMapNodeWeb (Autonomous Swarm: Planner, Coder, and QA Reviewer)
5. Multi-track synchronized sound design (whooshes, keyboard typing, glitch zaps, stamp hits, reward chimes)
6. Looping ambient BGM with speech ducking
7. FFmpeg master compositing with continuous playback (zero black frames)
"""

import os
import sys
import json
import time
import asyncio
import subprocess
import shutil
from typing import Dict, List, Any
from dotenv import load_dotenv

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
load_dotenv(os.path.join(ROOT_DIR, ".env"))

# Prevent disk overflow by directing temp files to media_temp
os.environ["TMPDIR"] = os.path.join(ROOT_DIR, "media_temp", "tmp")
os.environ["TEMP"] = os.environ["TMPDIR"]
os.environ["TMP"] = os.environ["TMPDIR"]
os.makedirs(os.environ["TMPDIR"], exist_ok=True)

sys.path.insert(0, os.path.join(ROOT_DIR, "apps", "worker"))
os.chdir(os.path.join(ROOT_DIR, "apps", "worker"))

from services.transcriber import transcribe_and_compress
from services.subtitle_generator import generate_ass_subtitles
from services.remotion_renderer import render_motion_graphic

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

OUTPUT_VIDEO = os.path.join(ROOT_DIR, "how_ai_agents_work_1min.mp4")
PUBLIC_WEB_VIDEO = os.path.join(ROOT_DIR, "apps/web/public/how_ai_agents_work_1min.mp4")
TEMP_DIR = os.path.join(ROOT_DIR, "media_temp", "how_ai_agents_work_1min")
os.makedirs(TEMP_DIR, exist_ok=True)
os.makedirs(f"{TEMP_DIR}/assets", exist_ok=True)
os.makedirs(f"{TEMP_DIR}/mg_overlays", exist_ok=True)
os.makedirs(f"{TEMP_DIR}/previews", exist_ok=True)

async def generate_speech(audio_mp3: str, audio_wav: str) -> float:
    print("[1/7] 🎙️ Generating neural AI voiceover with edge-tts (ChristopherNeural)...")
    import edge_tts
    communicate = edge_tts.Communicate(SCRIPT_TEXT, "en-US-ChristopherNeural", rate="+8%", pitch="+0Hz")
    await communicate.save(audio_mp3)

    subprocess.run([
        "ffmpeg", "-y", "-i", audio_mp3,
        "-ac", "1", "-ar", "16000",
        audio_wav
    ], capture_output=True, check=True)

    dur_proc = subprocess.run([
        "ffprobe", "-v", "error", "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1", audio_wav
    ], capture_output=True, text=True)
    duration = float(dur_proc.stdout.strip())
    print(f"      Voiceover duration: {duration:.2f} seconds.")
    return duration

def create_base_canvas(duration: float, audio_wav: str, out_raw: str, bg_video: str = None):
    print(f"[2/7] 🎨 Building 1080x1920 base canvas ({duration:.2f}s)...")
    if bg_video and os.path.exists(bg_video) and os.path.getsize(bg_video) > 10000:
        filter_str = (
            "scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,"
            "eq=brightness=-0.32:contrast=1.35:saturation=0.8,"
            "drawgrid=width=120:height=120:thickness=1:color=white@0.025,"
            "drawbox=x=0:y=0:w=1080:h=1920:color=black@0.45:t=fill"
        )
        cmd = [
            "ffmpeg", "-y",
            "-stream_loop", "-1", "-i", bg_video,
            "-i", audio_wav,
            "-vf", filter_str,
            "-t", f"{duration:.3f}",
            "-c:v", "libx264", "-preset", "fast", "-pix_fmt", "yuv420p",
            "-c:a", "aac", "-b:a", "192k",
            out_raw
        ]
    else:
        filter_str = (
            "color=c=#030712:s=1080x1920:r=30,"
            "drawgrid=width=120:height=120:thickness=1:color=white@0.03,"
            "drawgrid=width=360:height=360:thickness=2:color=#00e5ff@0.04"
        )
        cmd = [
            "ffmpeg", "-y",
            "-f", "lavfi", "-i", filter_str,
            "-i", audio_wav,
            "-t", f"{duration:.3f}",
            "-c:v", "libx264", "-preset", "fast", "-pix_fmt", "yuv420p",
            "-c:a", "aac", "-b:a", "192k",
            out_raw
        ]
    subprocess.run(cmd, capture_output=True, check=True)
    print(f"      Base canvas generated: {out_raw}")

def prepare_brolls(target_dir: str) -> Dict[str, str]:
    print("[3/7] 📦 Resolving high-definition 9:16 tech B-rolls...")
    # Map high quality existing cached b-rolls
    source_pool = {
        "broll_hook_cyber": os.path.join(ROOT_DIR, "media_temp/broll_cache/pexels_14209120_1920x1080.mp4"),
        "broll_future_city": os.path.join(ROOT_DIR, "media_temp/broll_cache/pexels_13801277_1080x1920.mp4"),
        "bg_tech_network": os.path.join(ROOT_DIR, "media_temp/broll_cache/pexels_3141210_1920x1080.mp4")
    }

    resolved = {}
    for k, src in source_pool.items():
        dst = os.path.join(target_dir, f"{k}.mp4")
        if os.path.exists(src) and os.path.getsize(src) > 1000:
            if not os.path.exists(dst) or os.path.getsize(dst) < 10000:
                print(f"      Normalizing {k} to 1080x1920 portrait format...")
                cmd = [
                    "ffmpeg", "-y", "-i", src,
                    "-vf", "scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,fps=30",
                    "-c:v", "libx264", "-preset", "fast", "-crf", "22", "-an",
                    dst
                ]
                subprocess.run(cmd, capture_output=True, check=True)
            resolved[k] = dst
    print(f"      Resolved {len(resolved)} normalized 9:16 clips.")
    return resolved

def render_all_motion_graphics(mg_list: List[Dict[str, Any]], output_dir: str) -> Dict[str, str]:
    print(f"[5/7] ⚛️ Pre-rendering {len(mg_list)} Remotion motion graphics overlays (1080x1920 ProRes 4444)...")
    rendered_map = {}
    for idx, item in enumerate(mg_list, 1):
        mg_id = item["id"]
        comp_id = item["composition_id"]
        props = item["props"]
        dur = item["end"] - item["start"]
        frames = max(1, int(dur * 30))
        out_file = os.path.join(output_dir, f"{mg_id}.mov")

        if os.path.exists(out_file) and os.path.getsize(out_file) > 10000:
            mb = os.path.getsize(out_file) / (1024 * 1024)
            print(f"      [{idx}/{len(mg_list)}] ⚡ Reusing cached MOV: {os.path.basename(out_file)} ({mb:.1f} MB)")
            rendered_map[mg_id] = out_file
            continue

        print(f"      [{idx}/{len(mg_list)}] Rendering '{comp_id}' ({frames} frames, {dur:.1f}s)...")
        t0 = time.time()
        res = render_motion_graphic(
            composition_id=comp_id,
            props=props,
            duration_frames=frames,
            fps=30,
            width=1080,
            height=1920,
            output_path=out_file
        )
        elapsed = time.time() - t0
        if res and os.path.exists(res) and os.path.getsize(res) > 0:
            mb = os.path.getsize(res) / (1024 * 1024)
            print(f"          ✅ Rendered in {elapsed:.1f}s ({mb:.1f} MB) -> {os.path.basename(res)}")
            rendered_map[mg_id] = res
        else:
            print(f"          ⚠️ Failed to render Remotion composition {comp_id}")
    return rendered_map

def composite_master(
    base_video: str,
    output_video: str,
    brolls: List[Dict[str, Any]],
    motion_graphics: List[Dict[str, Any]],
    rendered_mg_map: Dict[str, str],
    sfx_list: List[Dict[str, Any]],
    ass_subs: str,
    bgm_path: str,
    total_duration: float
):
    print("[6/7] 🎬 Compositing complete master (Base + B-Rolls + Motion Graphics + SFX + Subtitles + BGM)...")
    
    inputs = ["-i", base_video]  # Input 0: base canvas with voiceover
    current_idx = 1

    # B-roll inputs
    broll_inputs = []
    for b in brolls:
        inputs.extend(["-i", b["path"]])
        broll_inputs.append((current_idx, b))
        current_idx += 1

    # Motion graphics MOV inputs
    mg_inputs = []
    for mg in motion_graphics:
        mg_file = rendered_mg_map.get(mg["id"])
        if mg_file and os.path.exists(mg_file):
            inputs.extend(["-i", mg_file])
            mg_inputs.append((current_idx, mg))
            current_idx += 1

    # SFX inputs
    sfx_inputs = []
    for s in sfx_list:
        if os.path.exists(s["path"]):
            inputs.extend(["-i", s["path"]])
            sfx_inputs.append((current_idx, s))
            current_idx += 1

    # BGM input
    has_bgm = bgm_path and os.path.exists(bgm_path)
    bgm_idx = None
    if has_bgm:
        inputs.extend(["-stream_loop", "-1", "-i", bgm_path])
        bgm_idx = current_idx
        current_idx += 1

    filter_parts = []
    last_v = "0:v"

    # 1. Overlay B-rolls onto base canvas
    for inp_idx, b in broll_inputs:
        scaled_label = f"broll_scaled_{inp_idx}"
        out_v = f"v_broll_{inp_idx}"
        b_dur = b["end"] - b["start"]
        filter_parts.append(
            f"[{inp_idx}:v]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,"
            f"setpts=PTS-STARTPTS,trim=duration={b_dur:.3f}[{scaled_label}]"
        )
        filter_parts.append(
            f"[{last_v}][{scaled_label}]overlay=0:0:enable='between(t,{b['start']:.2f},{b['end']:.2f})'[{out_v}]"
        )
        last_v = out_v

    # 2. Overlay Motion Graphics MOV files with Alpha Channel
    for inp_idx, mg in mg_inputs:
        out_v = f"v_mg_{inp_idx}"
        filter_parts.append(
            f"[{inp_idx}:v]setpts=PTS-STARTPTS+{mg['start']:.2f}/TB[{inp_idx}_delayed]"
        )
        filter_parts.append(
            f"[{last_v}][{inp_idx}_delayed]overlay=0:0:enable='between(t,{mg['start']:.2f},{mg['end']:.2f})':format=auto[{out_v}]"
        )
        last_v = out_v

    # 3. Burn Subtitles
    escaped_ass = ass_subs.replace("\\", "/").replace(":", "\\:")
    final_v = "v_final"
    filter_parts.append(f"[{last_v}]subtitles='{escaped_ass}'[{final_v}]")

    # 4. Audio Mixing (Voiceover + SFX + ducked BGM)
    audio_mix_inputs = ["[0:a]"]
    
    # Process each SFX: delay and volume
    for inp_idx, s in sfx_inputs:
        sfx_label = f"sfx_{inp_idx}"
        vol = s.get("volume", 0.6)
        delay_ms = int(s["start"] * 1000)
        filter_parts.append(
            f"[{inp_idx}:a]volume={vol:.2f},adelay={delay_ms}|{delay_ms}[{sfx_label}]"
        )
        audio_mix_inputs.append(f"[{sfx_label}]")

    if has_bgm:
        filter_parts.append(
            f"[{bgm_idx}:a]volume=0.14,atrim=0:{total_duration:.2f},asetpts=PTS-STARTPTS[bgm_mix]"
        )
        audio_mix_inputs.append("[bgm_mix]")

    total_audio_streams = len(audio_mix_inputs)
    filter_parts.append(
        f"{''.join(audio_mix_inputs)}amix=inputs={total_audio_streams}:duration=first:dropout_transition=2[a_final]"
    )

    filter_complex_str = ";\n".join(filter_parts)

    cmd = [
        "ffmpeg", "-y",
        *inputs,
        "-filter_complex", filter_complex_str,
        "-map", f"[{final_v}]",
        "-map", "[a_final]",
        "-t", f"{total_duration:.3f}",
        "-c:v", "libx264", "-preset", "medium", "-crf", "19", "-pix_fmt", "yuv420p",
        "-c:a", "aac", "-b:a", "192k",
        output_video
    ]

    print("      Executing FFmpeg master composite...")
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode != 0:
        print(f"❌ FFmpeg composite error:\n{res.stderr[-2000:]}")
        raise RuntimeError(f"FFmpeg composite failed: {res.stderr[-500:]}")
    print(f"      ✅ Master video composited successfully: {output_video}")

def main():
    t_start = time.time()
    audio_mp3 = f"{TEMP_DIR}/speech.mp3"
    audio_wav = f"{TEMP_DIR}/speech.wav"
    raw_video = f"{TEMP_DIR}/base_canvas_9_16.mp4"
    ass_subs = f"{TEMP_DIR}/subtitles.ass"
    mg_dir = f"{TEMP_DIR}/mg_overlays"
    sfx_dir = os.path.join(ROOT_DIR, "apps/worker/data/sfx/clips")
    bgm_path = os.path.join(sfx_dir, "chill-bgm.mp3")

    # Step 1: Speech Generation
    duration = asyncio.run(generate_speech(audio_mp3, audio_wav))
    total_duration = duration + 0.8  # Add 0.8s tail padding for natural impact fade

    # Step 2: B-Roll Assets
    brolls_map = prepare_brolls(f"{TEMP_DIR}/assets")
    bg_video = brolls_map.get("bg_tech_network")

    # Step 3: Base Canvas
    create_base_canvas(total_duration, audio_wav, raw_video, bg_video)

    # Step 4: Define Motion Graphics Overlays & Timeline
    motion_graphics_list = [
        # MG 1: Architecture Pipeline (4-step cognitive loop)
        {
            "id": "mg_1_pipeline",
            "composition_id": "architecture-pipeline",
            "start": 5.2,
            "end": 16.5,
            "props": {
                "title": "AUTONOMOUS COGNITIVE LOOP",
                "subtitle": "4-STAGE SYSTEM ARCHITECTURE & RECURSIVE ENGINE",
                "badge": "⚡ AGENTIC ENGINE",
                "stage1Title": "Perception & Ingest",
                "stage1Desc": "Analyzes goal, context state, and project files.",
                "stage1Badge": "STAGE 01",
                "stage1Metric": "PERCEPTION",
                "stage2Title": "Recursive Reasoning",
                "stage2Desc": "Decomposes missions into executable sub-tasks.",
                "stage2Badge": "STAGE 02",
                "stage2Metric": "PLANNING",
                "stage3Title": "Tool Execution",
                "stage3Desc": "Calls APIs, writes code, and executes bash.",
                "stage3Badge": "STAGE 03",
                "stage3Metric": "LIVE TERMINAL",
                "stage4Title": "Self-Correction Gate",
                "stage4Desc": "Evaluates stack traces and self-heals syntax errors.",
                "stage4Badge": "STAGE 04",
                "stage4Metric": "DETERMINISTIC",
                "personality": "technical"
            }
        },
        # MG 2: Code Reveal / Terminal Execution
        {
            "id": "mg_2_code_exec",
            "composition_id": "code-reveal",
            "start": 16.8,
            "end": 26.8,
            "props": {
                "language": "python",
                "code": (
                    "# 1. Agent decomposes high-level objective\n"
                    "tasks = agent.plan(goal='Deploy API')\n\n"
                    "# 2. Agent invokes live terminal tool\n"
                    "res = agent.call_tool('terminal', cmd='pytest')\n\n"
                    "# 3. Result: 42 tests passed in 0.8s ✅"
                ),
                "personality": "technical"
            }
        },
        # MG 3: Tactile Checklist (Self-Correction & Error Resolution)
        {
            "id": "mg_3_self_correction",
            "composition_id": "tactile-checklist-stamp",
            "start": 27.0,
            "end": 37.0,
            "props": {
                "title": "DETERMINISTIC VERIFICATION",
                "badge": "🛠️ SELF-CORRECTION LOOP",
                "item1Text": "Terminal Test Execution",
                "item1Detail": "Syntax error identified on line 42 during unit test run.",
                "item1Status": "fail",
                "item2Text": "Stack Trace Inspection",
                "item2Detail": "Agent isolates bug, rewrites syntax, and patches file.",
                "item2Status": "pass",
                "item3Text": "Automated Re-Verification",
                "item3Detail": "Full regression suite passes in isolated sandbox.",
                "item3Status": "pass",
                "verdictText": "BUG RESOLVED • 100% PASS RATE",
                "verdictStatus": "pass",
                "synthesis": "VERIFICATION: Closed feedback loops guarantee deterministic outcomes.",
                "personality": "technical"
            }
        },
        # MG 4: Autonomous Swarm Mind Map
        {
            "id": "mg_4_swarm",
            "composition_id": "mind-map-node-web",
            "start": 37.2,
            "end": 47.8,
            "props": {
                "title": "AUTONOMOUS AGENT SWARM",
                "badge": "🤖 MULTI-AGENT SYNERGY",
                "centerTitle": "AGENT SWARM",
                "centerIcon": "⚡",
                "node1Title": "Planner Agent",
                "node1Desc": "Decomposes missions into sub-tasks",
                "node1Icon": "📋",
                "node2Title": "Coder Agent",
                "node2Desc": "Executes tools & modifies codebase",
                "node2Icon": "💻",
                "node3Title": "Reviewer & QA",
                "node3Desc": "Validates builds & patches bugs",
                "node3Icon": "🛡️",
                "personality": "technical"
            }
        }
    ]

    # Pre-render motion graphics overlays (reusing cached MOVs if available)
    rendered_mg_map = render_all_motion_graphics(motion_graphics_list, mg_dir)

    # Step 5: Faster-Whisper Transcription & Dynamic Subtitles
    print("[5/7] 📝 Transcribing with faster-whisper for word-level sync...")
    bracketed_transcript, timestamp_map = transcribe_and_compress(audio_wav)
    print(f"      Extracted {len(timestamp_map)} word-level timestamps.")

    # Edits for subtitle generator: when motion graphics are active, caption docks below card (y=1440)
    # When no motion graphics are active (e.g. B-roll at 0-5.2s, 47.8-54.5s), caption docks in center (y=960)
    mg_edits = [
        {
            "action": "motion_graphics",
            "start": mg["start"],
            "end": mg["end"]
        }
        for mg in motion_graphics_list
    ]

    print("      ⚡ Generating kinetic yellow-highlight ASS subtitles (docked below motion graphics, centered on b-rolls)...")
    generate_ass_subtitles(
        timestamp_map=timestamp_map,
        output_ass_path=ass_subs,
        edits=mg_edits,
        font_size=58,
        primary_color="&H00FFFFFF",
        highlight_color="&H0000FFFF",
        is_faceless=True,
        aspect_ratio="9:16",
        caption_preset="tiktok_yellow",
        motion_graphics_bottom_y=1440,
        enable_bounce=False,
        pop_scale=100
    )

    # Step 6: Define B-Roll Overlays
    brolls_timeline = [
        {
            "name": "Hook Cyber Matrix",
            "path": brolls_map["broll_hook_cyber"],
            "start": 0.0,
            "end": 5.2
        },
        {
            "name": "Climax Future City",
            "path": brolls_map["broll_future_city"],
            "start": 47.8,
            "end": total_duration
        }
    ]

    # Step 7: SFX Sound Design
    sfx_timeline = [
        {"path": os.path.join(sfx_dir, "whoosh-soft.mp3"), "start": 0.0, "volume": 0.5},
        {"path": os.path.join(sfx_dir, "impact-soft.mp3"), "start": 1.5, "volume": 0.5},
        {"path": os.path.join(sfx_dir, "whoosh-soft.mp3"), "start": 5.2, "volume": 0.5},
        {"path": os.path.join(sfx_dir, "scan-hum.mp3"), "start": 6.5, "volume": 0.4},
        {"path": os.path.join(sfx_dir, "keys-typing-soft.mp3"), "start": 17.0, "volume": 0.5},
        {"path": os.path.join(sfx_dir, "ui-click-soft.mp3"), "start": 21.0, "volume": 0.5},
        {"path": os.path.join(sfx_dir, "glitch-zap.mp3"), "start": 27.2, "volume": 0.45},
        {"path": os.path.join(sfx_dir, "stamp-hit.mp3"), "start": 30.5, "volume": 0.6},
        {"path": os.path.join(sfx_dir, "chime-reward.mp3"), "start": 33.0, "volume": 0.5},
        {"path": os.path.join(sfx_dir, "whoosh-soft.mp3"), "start": 37.2, "volume": 0.5},
        {"path": os.path.join(sfx_dir, "sparkle-soft.mp3"), "start": 40.0, "volume": 0.45},
        {"path": os.path.join(sfx_dir, "impact-deep-soft.mp3"), "start": 48.0, "volume": 0.65},
    ]

    # Step 8: Master Assembly
    composite_master(
        base_video=raw_video,
        output_video=OUTPUT_VIDEO,
        brolls=brolls_timeline,
        motion_graphics=motion_graphics_list,
        rendered_mg_map=rendered_mg_map,
        sfx_list=sfx_timeline,
        ass_subs=ass_subs,
        bgm_path=bgm_path,
        total_duration=total_duration
    )

    # Copy to web public
    shutil.copy(OUTPUT_VIDEO, PUBLIC_WEB_VIDEO)
    print(f"[✓] Mirrored video to public web folder: {PUBLIC_WEB_VIDEO}")

    # Extract preview frames for verification
    preview_timestamps = [
        (3.0, "preview_03s_hook_matrix.jpg"),
        (10.0, "preview_10s_architecture_loop.jpg"),
        (22.0, "preview_22s_code_reveal.jpg"),
        (26.0, "preview_26s_code_reveal_docked.jpg"),
        (32.0, "preview_32s_tactile_stamp.jpg"),
        (42.0, "preview_42s_swarm_mindmap.jpg"),
        (50.0, "preview_50s_future_climax.jpg"),
    ]
    print("\n📸 Extracting preview frames...")
    for sec, fname in preview_timestamps:
        out_frame = os.path.join(TEMP_DIR, "previews", fname)
        subprocess.run([
            "ffmpeg", "-y", "-ss", str(sec), "-i", OUTPUT_VIDEO,
            "-vframes", "1", "-q:v", "2", out_frame
        ], capture_output=True)
        if os.path.exists(out_frame):
            print(f"  [✓] Snapshot @ {sec:.1f}s -> {fname}")

    elapsed = time.time() - t_start
    size_mb = os.path.getsize(OUTPUT_VIDEO) / (1024 * 1024)
    print(f"\n🎉 ALL DONE! Video generated in {elapsed:.1f} seconds.")
    print(f"📁 Master Video: {OUTPUT_VIDEO} ({size_mb:.2f} MB)")
    print(f"📁 Web Video:    {PUBLIC_WEB_VIDEO}")

if __name__ == "__main__":
    main()

