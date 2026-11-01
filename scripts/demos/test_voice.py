import asyncio
import subprocess
import edge_tts

SCRIPT_TEXT = """Chatbots just talk. AI agents actually do the work.
Instead of answering a prompt and stopping, an AI agent runs on an autonomous four-step loop.
First, Perception: the agent ingests your goal, analyzes the environment, and reads your files.
Second, Recursive Reasoning: it breaks the big mission down into step-by-step sub-tasks.
Third, Tool Execution: the agent calls APIs, writes code, and runs commands in a live terminal.
And fourth, Self-Correction: when code breaks, it inspects the error, rewrites the syntax, and tests until it passes.
Combine specialized agents into a synchronized swarm—a planner, coder, and reviewer—and you have an autonomous engineering team running twenty-four seven.
Stop doing manual toil. Direct the agents, and let autonomous compute build the future."""

async def generate():
    comm = edge_tts.Communicate(SCRIPT_TEXT, "en-US-ChristopherNeural", rate="+8%")
    await comm.save("/tmp/ai_agents_voice_v3.mp3")

asyncio.run(generate())

subprocess.run([
    "ffmpeg", "-y", "-i", "/tmp/ai_agents_voice_v3.mp3",
    "-ac", "1", "-ar", "16000", "/tmp/ai_agents_voice_v3.wav"
], check=True)

dur_proc = subprocess.run([
    "ffprobe", "-v", "error", "-show_entries", "format=duration",
    "-of", "default=noprint_wrappers=1:nokey=1", "/tmp/ai_agents_voice_v3.wav"
], capture_output=True, text=True)

duration = float(dur_proc.stdout.strip())
print(f"EXACT DURATION: {duration:.2f} seconds")
