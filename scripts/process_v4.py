#!/usr/bin/env python3
"""
V4: Fixed clip boundaries + caption positioning
- Every clip starts at a COMPLETE thought, ends at a natural pause
- Captions at BOTTOM of frame, never covering face
- New captions REPLACE old ones (no stacking)
- Varied lengths: 10-50 seconds
"""

import json
import subprocess
import os

SRC = "content_bank/trial_blessings/source/sermon_blessings.mp4"
TRANSCRIPT_PATH = "content_bank/trial_blessings/transcript.json"
OUT_DIR = "content_bank/trial_blessings/clips_v4"
os.makedirs(OUT_DIR, exist_ok=True)

RED = "&H0000DDFF&"
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
    "amen", "spirit", "countenance", "smile", "faithfulness",
    "triumphantly", "grave", "heaven",
]

# === REDESIGNED CLIPS — Natural start/end points ===
clips = [
    # 1. (KEPT) "Whatever represents a sickness... Be healed... Receive life"
    # Starts: "Whatever represents a sickness" → Ends: "And receive life"
    {"num": "01", "name": "be_healed_receive_life",
     "start": 544, "end": 568},  # 24s

    # 2. "Whatever shortens life... premature death... cancer arrested... In the name of Jesus"
    # Starts: "Whatever shortens life" → Ends: "In the name of Jesus"
    {"num": "02", "name": "whatever_shortens_life",
     "start": 568, "end": 595},  # 27s

    # 3. "May your marriage be healed... financial life... Receive grace from God"
    # Starts: "And may your marriage" → Ends: "Receive grace from God"
    {"num": "03", "name": "marriage_and_life_healed",
     "start": 595, "end": 622},  # 27s

    # 4. (WAS 5+6 — user liked these, combining into one stronger clip)
    # "Receive things more valuable than money... good wife... good friend... In the name of Jesus"
    # Starts: "Receive things that have no value in money" → Ends: "In the name of Jesus"
    {"num": "04", "name": "receive_good_things",
     "start": 622, "end": 650},  # 28s

    # 5. "Between now and the end of the year... we block it... we reject it... In the name of Jesus"
    # Starts: "Between now and the end of the year" → Ends: "In the name of Jesus"
    {"num": "05", "name": "we_block_it",
     "start": 649, "end": 672},  # 23s

    # 6. "Anything that says you cannot enter 2026... divine escape... healed of chronic diseases... In the name of Jesus"
    # Starts: "Anything that will say you cannot enter" → Ends: "In the name of Jesus"
    {"num": "06", "name": "divine_escape_2026",
     "start": 671, "end": 708},  # 37s

    # 7. "From today you will not be afraid... The Lord heals you... receive impartation... In the name of Jesus"
    # Starts: "I say from today" → Ends: "In the name of Jesus"
    {"num": "07", "name": "you_will_not_be_afraid",
     "start": 707, "end": 728},  # 21s

    # 8. "You shall live and not die... fulfill your days... complete your course... In the name of Jesus"
    # Starts: "For you shall live and not die" → Ends: "In the name of Jesus"
    {"num": "08", "name": "live_and_not_die",
     "start": 738, "end": 762},  # 24s

    # 9. "The Lord look upon you favorably... his smile... bless you... every storm be silent... In the name of Jesus"
    # Starts: "The Lord look upon you favorably" → Ends: "In the name of Jesus"
    {"num": "09", "name": "the_lord_bless_you",
     "start": 773, "end": 806},  # 33s

    # 10. "These hands are noticed in heaven... looking to you for help... for sustenance, solace, grace... you bless us"
    # Starts: "Thank you that these hands" → Ends: "And you bless us"
    {"num": "10", "name": "hands_noticed_in_heaven",
     "start": 820, "end": 840},  # 20s

    # 11. "I will live and not die. Fulfill your days... your ministry... your mission. Finish everything."
    # Starts: "I will live and not die" → Ends: "Finish everything"
    {"num": "11", "name": "fulfill_everything",
     "start": 870, "end": 895},  # 25s

    # 12. "Fight on. Serve on. Follow on. It's not your time to die. Press on. Never give up."
    # Starts: "Fight on" → Ends: "Never give up"
    {"num": "12", "name": "fight_on",
     "start": 892, "end": 914},  # 22s

    # 13. "I prophesy and I see a light... let these blessings abide upon you... In Jesus name. Amen."
    # Starts: "For I prophesy" → Ends: "Amen"
    {"num": "13", "name": "i_see_a_light",
     "start": 916, "end": 945},  # 29s

    # 14. "The Lord knows you... He knows your name... He has a blessing for you... healing has come... In the name of Jesus"
    # Starts: "The Lord knows you" → Ends: "In the name of Jesus"
    {"num": "14", "name": "he_knows_your_name",
     "start": 968, "end": 1013},  # 45s
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
    Captions at BOTTOM of frame:
    - Alignment 2 = bottom center
    - MarginV 80 = 80px from bottom edge
    - Each new phrase REPLACES the old (no stacking)
    - Large Impact font, black outline for readability
    """
    header = f"""[Script Info]
Title: Prophetic Flow Daily
ScriptType: v4.00+
WrapStyle: 0
PlayResX: 1080
PlayResY: 1920
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Default,Impact,85,{WHITE},&H000000FF,&H00000000,&H80000000,-1,0,0,0,100,100,2,0,1,5,2,2,80,80,80,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
    events = []

    # Group words into phrases (3-6 words, break on punctuation)
    phrases = []
    current = []
    for w in words:
        current.append(w)
        ends_sentence = w["word"].rstrip().endswith(('.', ',', '!', '?', ':'))
        if (len(current) >= 4 and ends_sentence) or len(current) >= 6:
            phrases.append(current)
            current = []
    if current:
        phrases.append(current)

    for i, phrase in enumerate(phrases):
        start_time = phrase[0]["start"]
        # End time = start of next phrase (so current disappears when next appears)
        if i + 1 < len(phrases):
            end_time = phrases[i + 1][0]["start"]
        else:
            end_time = phrase[-1]["end"] + 0.5

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

    # Print the text for verification
    text = " ".join(w["word"] for w in words)
    print(f"  Text: {text[:100]}...")

    ass_content = generate_ass(words, duration)
    ass_path = f"{OUT_DIR}/{num}_{name}.ass"
    with open(ass_path, "w") as f:
        f.write(ass_content)

    output_path = f"{OUT_DIR}/{num}_{name}.mp4"

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
        print(f"  ✓ {size:.1f} MB")
        return True
    else:
        print(f"  ✗ FAILED")
        err = result.stderr.strip().split('\n')
        for line in err[-3:]:
            print(f"    {line}")
        return False


print("=" * 60)
print("PROPHETIC FLOW DAILY — V4")
print("Natural boundaries + bottom captions + varied lengths")
print("=" * 60)

success = 0
for c in clips:
    if process_clip(c):
        success += 1

print(f"\n{'=' * 60}")
print(f"DONE: {success}/{len(clips)} clips")
print(f"Output: {OUT_DIR}/")

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
