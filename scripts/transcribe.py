#!/usr/bin/env python3
"""Transcribe sermon video using faster-whisper with word-level timestamps."""

import json
import sys
from faster_whisper import WhisperModel

VIDEO_PATH = "content_bank/trial_blessings/source/sermon_blessings.mp4"
OUTPUT_PATH = "content_bank/trial_blessings/transcript.json"

print("Loading Whisper model (medium)... This may take a moment on first run.")
model = WhisperModel("medium", device="cpu", compute_type="int8")

print(f"Transcribing: {VIDEO_PATH}")
segments, info = model.transcribe(
    VIDEO_PATH,
    beam_size=5,
    word_timestamps=True,
    language="en"
)

print(f"Detected language: {info.language} (probability: {info.language_probability:.2f})")

all_segments = []
for segment in segments:
    words = []
    if segment.words:
        for word in segment.words:
            words.append({
                "word": word.word.strip(),
                "start": round(word.start, 3),
                "end": round(word.end, 3),
                "probability": round(word.probability, 3)
            })

    seg_data = {
        "id": segment.id,
        "start": round(segment.start, 3),
        "end": round(segment.end, 3),
        "text": segment.text.strip(),
        "words": words
    }
    all_segments.append(seg_data)
    # Print progress
    minutes = int(segment.end // 60)
    seconds = int(segment.end % 60)
    print(f"  [{minutes:02d}:{seconds:02d}] {segment.text.strip()[:80]}")

output = {
    "language": info.language,
    "language_probability": round(info.language_probability, 3),
    "duration": round(info.duration, 3),
    "segments": all_segments
}

with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
    json.dump(output, f, indent=2, ensure_ascii=False)

print(f"\nDone! {len(all_segments)} segments transcribed.")
print(f"Transcript saved to: {OUTPUT_PATH}")
