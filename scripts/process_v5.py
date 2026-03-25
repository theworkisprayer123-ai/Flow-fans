#!/usr/bin/env python3
"""
V5: Karaoke-style word-by-word captions
- Each word appears exactly when spoken (word-level Whisper timestamps)
- ALL WHITE text, no color highlights
- Words build up phrase by phrase, then reset for next phrase
- Bottom of frame, never covers face
"""

import json
import subprocess
import os

SRC = "content_bank/trial_blessings/source/sermon_blessings.mp4"
TRANSCRIPT_PATH = "content_bank/trial_blessings/transcript.json"
OUT_DIR = "content_bank/trial_blessings/clips_v5"
os.makedirs(OUT_DIR, exist_ok=True)

WHITE = "&H00FFFFFF&"
DIM = "&H00888888&"  # Dimmed gray for upcoming words

clips = [
    {"num": "01", "name": "be_healed_receive_life", "start": 544, "end": 568},
    {"num": "02", "name": "whatever_shortens_life", "start": 568, "end": 595},
    {"num": "03", "name": "marriage_and_life_healed", "start": 595, "end": 622},
    {"num": "04", "name": "receive_good_things", "start": 622, "end": 649},
    {"num": "05", "name": "we_block_it", "start": 649, "end": 671},
    {"num": "06", "name": "divine_escape_2026", "start": 671, "end": 706},
    {"num": "07", "name": "you_will_not_be_afraid", "start": 708, "end": 728},
    {"num": "08", "name": "live_and_not_die", "start": 739, "end": 760},
    {"num": "09", "name": "the_lord_bless_you", "start": 773, "end": 806},
    {"num": "10", "name": "hands_noticed_in_heaven", "start": 825, "end": 840},
    {"num": "11", "name": "fulfill_everything", "start": 879, "end": 895},
    {"num": "12", "name": "fight_on", "start": 892, "end": 914},
    {"num": "13", "name": "i_see_a_light", "start": 916, "end": 945},
    {"num": "14", "name": "he_knows_your_name", "start": 968, "end": 992},
    {"num": "15", "name": "healing_has_come", "start": 996, "end": 1013},
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


def fmt_time(s):
    s = max(0, s)
    h = int(s // 3600)
    m = int((s % 3600) // 60)
    sec = int(s % 60)
    cs = int((s % 1) * 100)
    return f"{h}:{m:02d}:{sec:02d}.{cs:02d}"


def generate_ass_karaoke(words, clip_duration):
    """
    Word-by-word karaoke: each word appears exactly when spoken.
    Words build up within a phrase, then the phrase clears for the next one.

    Method: For each phrase, show the full phrase but use \\kf tags
    so each word fills in from dim to white as it's spoken.
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
Style: Karaoke,Impact,85,{WHITE},{DIM},&H00000000,&H80000000,-1,0,0,0,100,100,2,0,1,5,2,2,80,80,80,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
    events = []

    # Group words into phrases (4-6 words, break on punctuation)
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
        phrase_start = phrase[0]["start"]
        # Phrase ends when next phrase starts, or after last word
        if i + 1 < len(phrases):
            phrase_end = phrases[i + 1][0]["start"]
        else:
            phrase_end = phrase[-1]["end"] + 0.8

        # Build karaoke text with \kf tags
        # \kf<duration in centiseconds> makes the word fill from SecondaryColour to PrimaryColour
        karaoke_parts = []
        for j, w in enumerate(phrase):
            word_text = w["word"].upper()
            # Duration of this word in centiseconds
            word_dur = w["end"] - w["start"]
            cs_dur = int(word_dur * 100)

            # Gap before this word (silence between words)
            if j == 0:
                gap = w["start"] - phrase_start
            else:
                gap = w["start"] - phrase[j-1]["end"]

            if gap > 0.05:
                gap_cs = int(gap * 100)
                karaoke_parts.append(f"{{\\kf{gap_cs}}}")

            karaoke_parts.append(f"{{\\kf{cs_dur}}}{word_text}")

        styled = " ".join(karaoke_parts)
        # Clean up extra spaces around tags
        styled = styled.replace("} {", "}{")

        events.append(
            f"Dialogue: 0,{fmt_time(phrase_start)},{fmt_time(phrase_end)},Karaoke,,0,0,0,,{styled}"
        )

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

    ass_content = generate_ass_karaoke(words, duration)
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
print("PROPHETIC FLOW DAILY — V5")
print("Karaoke word-by-word sync, all white, no highlights")
print("=" * 60)

success = 0
for c in clips:
    if process_clip(c):
        success += 1

print(f"\n{'=' * 60}")
print(f"DONE: {success}/{len(clips)} clips")
print(f"Output: {OUT_DIR}/")
