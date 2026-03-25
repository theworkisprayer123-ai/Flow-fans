#!/usr/bin/env python3
"""Add word-level subtitles to a clip using the transcript data."""

import json
import subprocess
import os

# Load transcript
with open("content_bank/trial_blessings/transcript.json") as f:
    transcript = json.load(f)

# Define clips with their source timestamps (relative to the 20-min download)
clips = [
    {"file": "07_fight_on_prophetic.mp4", "src_start": 870, "src_end": 937, "name": "Fight On Prophetic"},
    {"file": "05_impartation_life_promise.mp4", "src_start": 710, "src_end": 761, "name": "Impartation & Life Promise"},
    {"file": "01_healing_declaration.mp4", "src_start": 544, "src_end": 594, "name": "Healing Declaration"},
]

CLIPS_DIR = "content_bank/trial_blessings/clips"
OUT_DIR = "content_bank/trial_blessings/clips_subtitled"
os.makedirs(OUT_DIR, exist_ok=True)

def get_words_for_range(transcript, start_s, end_s):
    """Extract words with timestamps from transcript for a given time range."""
    words = []
    for seg in transcript["segments"]:
        if seg["end"] < start_s or seg["start"] > end_s:
            continue
        for w in seg.get("words", []):
            if w["start"] >= start_s and w["end"] <= end_s:
                words.append({
                    "word": w["word"],
                    "start": w["start"] - start_s,  # Relative to clip start
                    "end": w["end"] - start_s,
                })
    return words

def generate_ass_subtitles(words, clip_duration):
    """Generate ASS subtitle file with word-by-word highlighting."""

    header = """[Script Info]
Title: You Must Pray Subtitles
ScriptType: v4.00+
WrapStyle: 0
PlayResX: 1080
PlayResY: 1920
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Default,Arial,72,&H00FFFFFF,&H000000FF,&H00000000,&H80000000,-1,0,0,0,100,100,0,0,1,4,2,2,40,40,200,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""

    events = []

    # Group words into phrases (roughly 4-6 words each)
    phrases = []
    current_phrase = []
    for w in words:
        current_phrase.append(w)
        if len(current_phrase) >= 5 or w["word"].endswith(('.', '!', '?', ',')):
            phrases.append(current_phrase)
            current_phrase = []
    if current_phrase:
        phrases.append(current_phrase)

    for phrase in phrases:
        start_time = phrase[0]["start"]
        end_time = phrase[-1]["end"]
        text = " ".join(w["word"] for w in phrase)

        # Format time as H:MM:SS.CC
        def fmt_time(s):
            h = int(s // 3600)
            m = int((s % 3600) // 60)
            sec = int(s % 60)
            cs = int((s % 1) * 100)
            return f"{h}:{m:02d}:{sec:02d}.{cs:02d}"

        # Make key words gold colored
        styled_text = text
        for keyword in ["healed", "healing", "live", "die", "Jesus", "Lord",
                        "bless", "blessed", "receive", "Fight", "Press", "Keep",
                        "prophesy", "light", "peace", "grace", "deliverance",
                        "fulfill", "impartation", "afraid", "escape"]:
            styled_text = styled_text.replace(keyword, f"{{\\c&H0043A8D4&}}{keyword}{{\\c&HFFFFFF&}}")

        event = f"Dialogue: 0,{fmt_time(start_time)},{fmt_time(end_time)},Default,,0,0,0,,{styled_text}"
        events.append(event)

    return header + "\n".join(events) + "\n"

for clip_info in clips:
    print(f"\n--- Processing: {clip_info['name']} ---")

    # Get words for this clip's time range
    words = get_words_for_range(transcript, clip_info["src_start"], clip_info["src_end"])
    print(f"  Found {len(words)} words")

    if not words:
        print("  ⚠ No words found, skipping")
        continue

    # Get clip duration
    result = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "csv=p=0", f"{CLIPS_DIR}/{clip_info['file']}"],
        capture_output=True, text=True
    )
    clip_duration = float(result.stdout.strip())

    # Generate ASS file
    ass_content = generate_ass_subtitles(words, clip_duration)
    ass_path = f"{OUT_DIR}/{clip_info['file'].replace('.mp4', '.ass')}"
    with open(ass_path, "w") as f:
        f.write(ass_content)
    print(f"  Generated subtitle file: {ass_path}")

    # Burn subtitles into video
    input_path = f"{CLIPS_DIR}/{clip_info['file']}"
    output_path = f"{OUT_DIR}/{clip_info['file']}"

    cmd = [
        "ffmpeg", "-y", "-i", input_path,
        "-vf", f"ass={ass_path}",
        "-c:v", "libx264", "-preset", "medium", "-crf", "20",
        "-profile:v", "main",
        "-c:a", "aac", "-b:a", "128k",
        "-movflags", "+faststart",
        output_path
    ]

    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode == 0:
        size = os.path.getsize(output_path) / (1024 * 1024)
        print(f"  ✓ Subtitled clip saved: {output_path} ({size:.1f} MB)")
    else:
        print(f"  ✗ Failed: {result.stderr[:200]}")

print("\n=== DONE ===")
print(f"Subtitled clips saved to: {OUT_DIR}/")
