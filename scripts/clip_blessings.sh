#!/bin/bash
# Clip individual blessings from sermon video
# Source: last 20 min of Flow Prayer Meeting

SRC="content_bank/trial_blessings/source/sermon_blessings.mp4"
OUT="content_bank/trial_blessings/clips"
mkdir -p "$OUT"

echo "=== CLIPPING BLESSINGS ==="

# Blessing 1: Healing Declaration (9:04 - 9:54)
# "Whatever represents a sickness... Be healed of it now... Let all cancer cells be arrested"
echo "[1/8] Healing Declaration..."
ffmpeg -y -ss 544 -to 594 -i "$SRC" \
  -vf "crop=ih*9/16:ih,scale=1080:1920" \
  -c:v libx264 -preset medium -crf 20 -profile:v main \
  -c:a aac -b:a 128k -ar 44100 -r 30 \
  -movflags +faststart \
  "$OUT/01_healing_declaration.mp4" 2>/dev/null && echo "  ✓ Done" || echo "  ✗ Failed"

# Blessing 2: Receive Life & Deliverance (9:27 - 9:54)
# "Whatever shortens life... premature death... Receive deliverance... cancer cells arrested"
echo "[2/8] Receive Life & Deliverance..."
ffmpeg -y -ss 567 -to 594 -i "$SRC" \
  -vf "crop=ih*9/16:ih,scale=1080:1920" \
  -c:v libx264 -preset medium -crf 20 -profile:v main \
  -c:a aac -b:a 128k -ar 44100 -r 30 \
  -movflags +faststart \
  "$OUT/02_receive_life_deliverance.mp4" 2>/dev/null && echo "  ✓ Done" || echo "  ✗ Failed"

# Blessing 3: Total Healing - Marriage, Finance, Life (9:58 - 10:49)
# "May your marriage be healed... financial life be healed... Receive a good wife... good friend"
echo "[3/8] Total Life Healing..."
ffmpeg -y -ss 598 -to 649 -i "$SRC" \
  -vf "crop=ih*9/16:ih,scale=1080:1920" \
  -c:v libx264 -preset medium -crf 20 -profile:v main \
  -c:a aac -b:a 128k -ar 44100 -r 30 \
  -movflags +faststart \
  "$OUT/03_total_life_healing.mp4" 2>/dev/null && echo "  ✓ Done" || echo "  ✗ Failed"

# Blessing 4: Protection into the New Year (10:52 - 11:47)
# "Whatever will prevent you from passing safely... We block it... Receive divine escape"
echo "[4/8] Divine Protection..."
ffmpeg -y -ss 652 -to 707 -i "$SRC" \
  -vf "crop=ih*9/16:ih,scale=1080:1920" \
  -c:v libx264 -preset medium -crf 20 -profile:v main \
  -c:a aac -b:a 128k -ar 44100 -r 30 \
  -movflags +faststart \
  "$OUT/04_divine_protection.mp4" 2>/dev/null && echo "  ✓ Done" || echo "  ✗ Failed"

# Blessing 5: Impartation & Promise of Life (11:50 - 12:41)
# "You will not be afraid... Receive impartation... You shall live and not die... fulfill your days"
echo "[5/8] Impartation & Life Promise..."
ffmpeg -y -ss 710 -to 761 -i "$SRC" \
  -vf "crop=ih*9/16:ih,scale=1080:1920" \
  -c:v libx264 -preset medium -crf 20 -profile:v main \
  -c:a aac -b:a 128k -ar 44100 -r 30 \
  -movflags +faststart \
  "$OUT/05_impartation_life_promise.mp4" 2>/dev/null && echo "  ✓ Done" || echo "  ✗ Failed"

# Blessing 6: Aaronic Blessing - The Lord Bless You (12:42 - 13:28)
# "The Lord look upon you favorably... His countenance... give you peace... every storm be silent"
echo "[6/8] The Lord Bless You..."
ffmpeg -y -ss 762 -to 808 -i "$SRC" \
  -vf "crop=ih*9/16:ih,scale=1080:1920" \
  -c:v libx264 -preset medium -crf 20 -profile:v main \
  -c:a aac -b:a 128k -ar 44100 -r 30 \
  -movflags +faststart \
  "$OUT/06_the_lord_bless_you.mp4" 2>/dev/null && echo "  ✓ Done" || echo "  ✗ Failed"

# Blessing 7: Prophetic Declaration - Fight On (14:30 - 15:37)
# "I will live and not die... Fulfill your days... It's not your time to die... Fight on... I see a light"
echo "[7/8] Prophetic Declaration - Fight On..."
ffmpeg -y -ss 870 -to 937 -i "$SRC" \
  -vf "crop=ih*9/16:ih,scale=1080:1920" \
  -c:v libx264 -preset medium -crf 20 -profile:v main \
  -c:a aac -b:a 128k -ar 44100 -r 30 \
  -movflags +faststart \
  "$OUT/07_fight_on_prophetic.mp4" 2>/dev/null && echo "  ✓ Done" || echo "  ✗ Failed"

# Blessing 8: He Knows You - Final Blessing (16:10 - 17:00)
# "He knows your name... He knows your room... He has a blessing for you... healing has come"
echo "[8/8] He Knows You..."
ffmpeg -y -ss 970 -to 1020 -i "$SRC" \
  -vf "crop=ih*9/16:ih,scale=1080:1920" \
  -c:v libx264 -preset medium -crf 20 -profile:v main \
  -c:a aac -b:a 128k -ar 44100 -r 30 \
  -movflags +faststart \
  "$OUT/08_he_knows_you.mp4" 2>/dev/null && echo "  ✓ Done" || echo "  ✗ Failed"

echo ""
echo "=== CLIP SUMMARY ==="
for f in "$OUT"/*.mp4; do
  name=$(basename "$f")
  size=$(du -h "$f" | cut -f1)
  duration=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$f" 2>/dev/null)
  duration_int=${duration%.*}
  echo "  $name — ${duration_int}s — $size"
done
echo ""
echo "All clips saved to: $OUT/"
