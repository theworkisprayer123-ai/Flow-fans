#!/usr/bin/env python3
"""
V3: Match @flow_thereispowerhere layout
- 9:16 black frame (1080x1920)
- Original 16:9 video centered in middle (no crop)
- Top: title bar with message info
- Bottom: large bold subtitles with red keyword highlighting
"""

import json
import subprocess
import os
import re

# === CONFIG ===
SRC = "content_bank/trial_blessings/source/sermon_blessings.mp4"
TRANSCRIPT_PATH = "content_bank/trial_blessings/transcript.json"
OUT_DIR = "content_bank/trial_blessings/clips_v3"
os.makedirs(OUT_DIR, exist_ok=True)

# Branding
TITLE_LINE1 = "RECEIVE YOUR BLESSING"
TITLE_LINE2 = "FLOW PRAYER MEETING • BISHOP DAG HEWARD-MILLS"

# Red highlight color in ASS format: &H0000FF& (BGR format, blue=00, green=00, red=FF)
RED_HIGHLIGHT = "&H004040FF&"  # Warm red
WHITE = "&H00FFFFFF&"

# Keywords to highlight in red
KEYWORDS = [
    "healed", "healing", "heal", "live", "die", "Jesus", "Lord",
    "bless", "blessed", "blessing", "blessings", "receive", "Receive",
    "fight", "Fight", "press", "Press", "keep", "Keep",
    "prophesy", "light", "peace", "grace", "deliverance",
    "fulfill", "Fulfill", "impartation", "afraid", "escape",
    "block", "override", "reject", "cancer", "arrested", "reversed",
    "exemption", "divine", "silent", "storm", "crisis",
    "never", "Never", "good", "valuable", "help", "mercy"
]

# === CLIP DEFINITIONS ===
clips = [
    {"num": "01", "name": "be_healed_of_it_now", "start": 544, "end": 558},
    {"num": "02", "name": "receive_healing_receive_life", "start": 561, "end": 570},
    {"num": "03", "name": "receive_deliverance", "start": 571, "end": 582},
    {"num": "04", "name": "cancer_cells_arrested", "start": 587, "end": 595},
    {"num": "05", "name": "your_life_be_healed", "start": 598, "end": 607},
    {"num": "06", "name": "receive_grace_from_god", "start": 618, "end": 632},
    {"num": "07", "name": "receive_good_things", "start": 633, "end": 646},
    {"num": "08", "name": "we_block_it", "start": 652, "end": 669},
    {"num": "09", "name": "divine_escape", "start": 677, "end": 692},
    {"num": "10", "name": "you_will_not_be_afraid", "start": 710, "end": 717},
    {"num": "11", "name": "receive_impartation", "start": 720, "end": 729},
    {"num": "12", "name": "live_and_not_die", "start": 740, "end": 754},
    {"num": "13", "name": "the_lord_look_upon_you", "start": 776, "end": 787},
    {"num": "14", "name": "every_storm_be_silent", "start": 793, "end": 800},
    {"num": "15", "name": "fulfill_your_days", "start": 870, "end": 892},
    {"num": "16", "name": "fight_on", "start": 901, "end": 916},
    {"num": "17", "name": "i_see_a_light", "start": 918, "end": 933},
    {"num": "18", "name": "he_knows_your_name", "start": 970, "end": 984},
    {"num": "19", "name": "healing_has_come", "start": 986, "end": 1013},
]

# Load transcript
with open(TRANSCRIPT_PATH) as f:
    transcript = json.load(f)


def get_words_for_range(start_s, end_s):
    words = []
    for seg in transcript["segments"]:
        if seg["end"] < start_s or seg["start"] > end_s:
            continue
        for w in seg.get("words", []):
            if w["start"] >= start_s - 0.5 and w["end"] <= end_s + 0.5:
                words.append({
                    "word": w["word"],
                    "start": w["start"] - start_s,
                    "end": w["end"] - start_s,
                })
    return words


def highlight_word(word):
    """Check if word should be highlighted in red."""
    clean = word.strip(".,!?;:'\"")
    for kw in KEYWORDS:
        if clean.lower() == kw.lower():
            return True
    return False


def generate_ass(words, clip_duration):
    """Generate ASS subtitles — large bold text at bottom, red highlights."""

    header = f"""[Script Info]
Title: Prophetic Flow Daily
ScriptType: v4.00+
WrapStyle: 0
PlayResX: 1080
PlayResY: 1920
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Default,Impact,80,{WHITE},&H000000FF,&H00000000,&H00000000,-1,0,0,0,100,100,2,0,1,4,0,2,60,60,120,1
Style: Title,Arial,38,{WHITE},&H000000FF,&H00000000,&H00000000,-1,0,0,0,100,100,1,0,1,0,0,8,40,40,40,1
Style: Title2,Arial,28,&H00AAAAAA,&H000000FF,&H00000000,&H00000000,0,0,0,0,100,100,1,0,1,0,0,8,40,40,90,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""

    events = []

    # Title bar - stays for entire clip
    def fmt(s):
        h = int(s // 3600)
        m = int((s % 3600) // 60)
        sec = int(s % 60)
        cs = int((s % 1) * 100)
        return f"{h}:{m:02d}:{sec:02d}.{cs:02d}"

    events.append(f"Dialogue: 0,{fmt(0)},{fmt(clip_duration)},Title,,0,0,0,,{TITLE_LINE1}")
    events.append(f"Dialogue: 0,{fmt(0)},{fmt(clip_duration)},Title2,,0,0,0,,{TITLE_LINE2}")

    # Group words into short phrases (3-5 words)
    phrases = []
    current = []
    for w in words:
        current.append(w)
        # Break on punctuation or every 4-5 words
        if (len(current) >= 4 and w["word"].rstrip().endswith(('.', ',', '!', '?', ':'))) or len(current) >= 5:
            phrases.append(current)
            current = []
    if current:
        phrases.append(current)

    for phrase in phrases:
        start_time = phrase[0]["start"]
        end_time = phrase[-1]["end"] + 0.3  # Small padding

        # Build text with red highlights on keywords
        text_parts = []
        for w in phrase:
            word = w["word"]
            if highlight_word(word):
                # Red highlight + slightly larger
                text_parts.append(f"{{\\c{RED_HIGHLIGHT}\\b1}}{word.upper()}{{\\c{WHITE}\\b1}}")
            else:
                text_parts.append(word.upper())

        styled_text = " ".join(text_parts)
        events.append(f"Dialogue: 0,{fmt(start_time)},{fmt(end_time)},Default,,0,0,0,,{styled_text}")

    return header + "\n".join(events) + "\n"


def process_clip(clip_info):
    num = clip_info["num"]
    name = clip_info["name"]
    start = clip_info["start"]
    end = clip_info["end"]
    duration = end - start
    fade_start = max(0, duration - 1.5)

    print(f"\n[{num}/19] {name} ({duration}s)")

    # Get words
    words = get_words_for_range(start, end)
    print(f"  Words found: {len(words)}")

    # Generate ASS subtitle file
    ass_content = generate_ass(words, duration)
    ass_path = f"{OUT_DIR}/{num}_{name}.ass"
    with open(ass_path, "w") as f:
        f.write(ass_content)

    output_path = f"{OUT_DIR}/{num}_{name}.mp4"

    # FFmpeg filter:
    # 1. Scale source video to fit width (1080px) maintaining aspect ratio
    # 2. Create black 1080x1920 background
    # 3. Overlay scaled video centered vertically (slightly above center)
    # 4. Burn ASS subtitles
    # 5. Fade out at end

    filter_complex = (
        # Scale source to 1080 wide, maintaining 16:9 = 1080x608
        f"[0:v]scale=1080:608[scaled];"
        # Create black background
        f"color=black:s=1080x1920:d={duration}[bg];"
        # Overlay video centered but shifted up (y=300 puts it in upper-middle area)
        f"[bg][scaled]overlay=0:340[composed];"
        # Burn subtitles
        f"[composed]ass={ass_path}[subtitled];"
        # Fade out
        f"[subtitled]fade=t=out:st={fade_start}:d=1.5[vout]"
    )

    cmd = [
        "ffmpeg", "-y",
        "-ss", str(start), "-to", str(end), "-i", SRC,
        "-filter_complex", filter_complex,
        "-map", "[vout]", "-map", "0:a",
        "-af", f"afade=t=out:st={fade_start}:d=1.5",
        "-c:v", "libx264", "-preset", "medium", "-crf", "20",
        "-profile:v", "main",
        "-c:a", "aac", "-b:a", "128k", "-ar", "44100",
        "-r", "30",
        "-t", str(duration),
        "-movflags", "+faststart",
        output_path
    ]

    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode == 0:
        size = os.path.getsize(output_path) / (1024 * 1024)
        print(f"  ✓ Saved: {output_path} ({size:.1f} MB)")
        return True
    else:
        print(f"  ✗ FAILED")
        # Print last few lines of stderr for debugging
        err_lines = result.stderr.strip().split('\n')
        for line in err_lines[-3:]:
            print(f"    {line}")
        return False


# === MAIN ===
print("=" * 60)
print("PROPHETIC FLOW DAILY — V3 CLIP PROCESSOR")
print("Layout: @flow_thereispowerhere style")
print("=" * 60)

success = 0
for clip_info in clips:
    if process_clip(clip_info):
        success += 1

print(f"\n{'=' * 60}")
print(f"DONE: {success}/{len(clips)} clips processed")
print(f"Output: {OUT_DIR}/")
print(f"{'=' * 60}")
