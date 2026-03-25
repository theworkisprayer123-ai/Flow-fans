#!/usr/bin/env python3
"""
Final processor: Match @flow_thereispowerhere style exactly
- Video fills full 9:16 frame (center crop)
- Subtitles overlaid directly ON the video
- ALL CAPS, white text, key words in RED
- 1.5s fade out (no abrupt endings)
"""

import json
import subprocess
import os

SRC = "content_bank/trial_blessings/source/sermon_blessings.mp4"
TRANSCRIPT_PATH = "content_bank/trial_blessings/transcript.json"
OUT_DIR = "content_bank/trial_blessings/clips_final"
os.makedirs(OUT_DIR, exist_ok=True)

# ASS color format is &HBBGGRR& (BGR, not RGB)
RED = "&H0000DDFF&"      # Bright red
WHITE = "&H00FFFFFF&"

KEYWORDS = [
    "healed", "healing", "heal", "heals", "live", "die", "death",
    "jesus", "lord", "god", "christ",
    "bless", "blessed", "blessing", "blessings", "blesses",
    "receive", "fight", "press", "keep",
    "prophesy", "light", "peace", "grace", "deliverance",
    "fulfill", "impartation", "afraid", "escape",
    "block", "override", "reject", "cancer", "arrested", "reversed",
    "exemption", "divine", "silent", "storm", "crisis",
    "never", "good", "valuable", "help", "mercy", "love",
    "life", "free", "forgiveness", "blood", "wickedness",
    "amen", "pray", "spirit", "countenance", "smile",
]

# === CLIP DEFINITIONS (V2 with merge fix) ===
clips = [
    # MERGED: clip 01+02 → "be healed... receive healing... receive life"
    {"num": "01", "name": "be_healed_receive_life", "start": 544, "end": 567},

    {"num": "02", "name": "receive_deliverance", "start": 571, "end": 582},
    {"num": "03", "name": "cancer_cells_arrested", "start": 587, "end": 595},
    {"num": "04", "name": "your_life_be_healed", "start": 598, "end": 607},
    {"num": "05", "name": "receive_grace_from_god", "start": 618, "end": 632},
    {"num": "06", "name": "receive_good_things", "start": 633, "end": 646},
    {"num": "07", "name": "we_block_it", "start": 652, "end": 669},
    {"num": "08", "name": "divine_escape", "start": 677, "end": 692},
    {"num": "09", "name": "you_will_not_be_afraid", "start": 710, "end": 717},
    {"num": "10", "name": "receive_impartation", "start": 720, "end": 729},
    {"num": "11", "name": "live_and_not_die", "start": 740, "end": 754},
    {"num": "12", "name": "the_lord_look_upon_you", "start": 776, "end": 787},
    {"num": "13", "name": "every_storm_be_silent", "start": 793, "end": 800},
    {"num": "14", "name": "fulfill_your_days", "start": 870, "end": 892},
    {"num": "15", "name": "fight_on", "start": 901, "end": 916},
    {"num": "16", "name": "i_see_a_light", "start": 918, "end": 933},
    {"num": "17", "name": "he_knows_your_name", "start": 970, "end": 984},
    {"num": "18", "name": "healing_has_come", "start": 986, "end": 1013},
]

with open(TRANSCRIPT_PATH) as f:
    transcript = json.load(f)


def get_words_for_range(start_s, end_s):
    words = []
    for seg in transcript["segments"]:
        if seg["end"] < start_s or seg["start"] > end_s:
            continue
        for w in seg.get("words", []):
            if w["start"] >= start_s - 0.3 and w["end"] <= end_s + 0.3:
                words.append({
                    "word": w["word"],
                    "start": w["start"] - start_s,
                    "end": w["end"] - start_s,
                })
    return words


def is_keyword(word):
    clean = word.strip(".,!?;:'\"").lower()
    return clean in KEYWORDS


def fmt_time(s):
    h = int(s // 3600)
    m = int((s % 3600) // 60)
    sec = int(s % 60)
    cs = int((s % 1) * 100)
    return f"{h}:{m:02d}:{sec:02d}.{cs:02d}"


def generate_ass(words, clip_duration):
    """
    Subtitles directly on video:
    - Large bold Impact font
    - Centered in lower third
    - ALL CAPS
    - Key words in RED
    - Black outline for readability
    """
    # MarginV=350 positions text in the lower portion of 1920px height
    header = f"""[Script Info]
Title: Prophetic Flow Daily
ScriptType: v4.00+
WrapStyle: 0
PlayResX: 1080
PlayResY: 1920
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Default,Impact,90,{WHITE},&H000000FF,&H00000000,&H80000000,-1,0,0,0,100,100,2,0,1,5,2,2,80,80,350,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
    events = []

    # Group words into short phrases (3-5 words)
    phrases = []
    current = []
    for w in words:
        current.append(w)
        ends_sentence = w["word"].rstrip().endswith(('.', ',', '!', '?', ':'))
        if (len(current) >= 4 and ends_sentence) or len(current) >= 5:
            phrases.append(current)
            current = []
    if current:
        phrases.append(current)

    for phrase in phrases:
        start_time = phrase[0]["start"]
        end_time = phrase[-1]["end"] + 0.4  # padding so text doesn't vanish too fast

        # Build styled text
        parts = []
        for w in phrase:
            word_text = w["word"].upper()
            if is_keyword(w["word"]):
                parts.append(f"{{\\c{RED}}}{word_text}{{\\c{WHITE}}}")
            else:
                parts.append(word_text)

        styled = " ".join(parts)
        events.append(f"Dialogue: 0,{fmt_time(start_time)},{fmt_time(end_time)},Default,,0,0,0,,{styled}")

    return header + "\n".join(events) + "\n"


def process_clip(clip_info):
    num = clip_info["num"]
    name = clip_info["name"]
    start = clip_info["start"]
    end = clip_info["end"]
    duration = end - start
    fade_start = max(0, duration - 1.5)

    print(f"\n[{num}/{len(clips)}] {name} ({duration}s)")

    words = get_words_for_range(start, end)
    print(f"  Words: {len(words)}")

    ass_content = generate_ass(words, duration)
    ass_path = f"{OUT_DIR}/{num}_{name}.ass"
    with open(ass_path, "w") as f:
        f.write(ass_content)

    output_path = f"{OUT_DIR}/{num}_{name}.mp4"

    # Video filter:
    # 1. Center crop to 9:16 (crop width = height * 9/16)
    # 2. Scale to 1080x1920
    # 3. Burn ASS subtitles
    # 4. Fade out last 1.5s
    vf = (
        f"crop=ih*9/16:ih,"
        f"scale=1080:1920,"
        f"ass={ass_path},"
        f"fade=t=out:st={fade_start}:d=1.5"
    )

    cmd = [
        "ffmpeg", "-y",
        "-ss", str(start), "-to", str(end), "-i", SRC,
        "-vf", vf,
        "-af", f"afade=t=out:st={fade_start}:d=1.5",
        "-c:v", "libx264", "-preset", "medium", "-crf", "20",
        "-profile:v", "main",
        "-c:a", "aac", "-b:a", "128k", "-ar", "44100",
        "-r", "30",
        "-movflags", "+faststart",
        output_path
    ]

    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode == 0:
        size = os.path.getsize(output_path) / (1024 * 1024)
        print(f"  ✓ {output_path} ({size:.1f} MB)")
        return True
    else:
        print(f"  ✗ FAILED")
        err = result.stderr.strip().split('\n')
        for line in err[-3:]:
            print(f"    {line}")
        return False


print("=" * 60)
print("PROPHETIC FLOW DAILY — FINAL CLIP PROCESSOR")
print("Style: @flow_thereispowerhere")
print("=" * 60)

success = 0
for c in clips:
    if process_clip(c):
        success += 1

print(f"\n{'=' * 60}")
print(f"DONE: {success}/{len(clips)} clips")
print(f"Output: {OUT_DIR}/")

# Summary
print(f"\n--- CLIP DURATIONS ---")
for f_name in sorted(os.listdir(OUT_DIR)):
    if f_name.endswith(".mp4"):
        path = f"{OUT_DIR}/{f_name}"
        r = subprocess.run(
            ["ffprobe", "-v", "error", "-show_entries", "format=duration",
             "-of", "csv=p=0", path], capture_output=True, text=True
        )
        dur = float(r.stdout.strip())
        print(f"  {dur:.0f}s  {f_name}")
