#!/bin/bash
# V2: Short blessing clips (10-20 sec), 2-3 lines each
# Ends with a natural pause, not abrupt cuts
# Each clip = ONE powerful moment, not a whole section

SRC="content_bank/trial_blessings/source/sermon_blessings.mp4"
OUT="content_bank/trial_blessings/clips_v2"
rm -rf "$OUT"
mkdir -p "$OUT"

echo "=== CLIPPING BLESSINGS V2 (Short & Punchy) ==="

# Fade out: -af "afade=t=out:st=X:d=1.5" adds 1.5s audio fade at end
# Video fade: fade=t=out:st=X:d=1.5
# This prevents abrupt endings

clip() {
  local num="$1" name="$2" start="$3" end="$4"
  local duration=$(echo "$end - $start" | bc)
  local fade_start=$(echo "$duration - 1.5" | bc)

  echo "[$num] $name (${duration}s)..."
  ffmpeg -y -ss "$start" -to "$end" -i "$SRC" \
    -vf "crop=ih*9/16:ih,scale=1080:1920,fade=t=out:st=${fade_start}:d=1.5" \
    -af "afade=t=out:st=${fade_start}:d=1.5" \
    -c:v libx264 -preset medium -crf 20 -profile:v main \
    -c:a aac -b:a 128k -ar 44100 -r 30 \
    -movflags +faststart \
    "$OUT/${num}_${name}.mp4" 2>/dev/null && echo "  ✓" || echo "  ✗"
}

# --- BLESSING CLIPS (2-3 lines each, natural ending points) ---

# "Whatever represents a sickness, a disease, a calamity...
#  Whatever represents an evil disease. Be healed of it now."
clip "01" "be_healed_of_it_now" 544 558

# "Receive healing. And receive life."
clip "02" "receive_healing_receive_life" 561 570

# "Whatever shortens life that has entered into you,
#  to cause a premature death... Receive deliverance."
clip "03" "receive_deliverance" 571 582

# "Let all cancer cells be arrested in the name of Jesus.
#  Let all negative diagnosis be reversed."
clip "04" "cancer_cells_arrested" 587 595

# "May your marriage be healed. And your life be healed.
#  Let your financial life be healed."
clip "05" "your_life_be_healed" 598 607

# "Receive help from God. Receive grace from God.
#  Receive things more valuable than money."
clip "06" "receive_grace_from_god" 618 632

# "Receive a good wife. Receive a good relationship.
#  Receive a good friend. Receive good things."
clip "07" "receive_good_things" 633 646

# "Whatever will prevent you from passing safely into the new year,
#  we block it. We override it. We reject it."
clip "08" "we_block_it" 652 669

# "Anything that will say you cannot enter into 2026...
#  Receive a divine escape. Divine exemption from wickedness."
clip "09" "divine_escape" 677 692

# "From today you will not be afraid again.
#  The Lord heals you. The Lord blesses you."
clip "10" "you_will_not_be_afraid" 710 717

# "Receive an impartation. His love and his mercy into your life."
clip "11" "receive_impartation" 720 729

# "You shall live and not die. You shall serve the Lord.
#  You shall fulfill your days. You shall complete your course."
clip "12" "live_and_not_die" 740 754

# "The Lord look upon you favorably.
#  Let his countenance and his smile be lifted over your face."
clip "13" "the_lord_look_upon_you" 776 787

# "Let every crisis and storm of your life be silent.
#  In the name of Jesus."
clip "14" "every_storm_be_silent" 793 800

# "I will live and not die. I will fulfill my days.
#  Fulfill your course. Fulfill your ministry."
clip "15" "fulfill_your_days" 870 892

# "It's not your time to die. Fight on. Press on. Keep on.
#  Never be tired. Never give up."
clip "16" "fight_on" 901 916

# "I prophesy and I see a light. A light at the end.
#  Your light arrives in the face of death."
clip "17" "i_see_a_light" 918 933

# "He knows your name. He knows your room.
#  He knows what you are experiencing."
clip "18" "he_knows_your_name" 970 984

# "He has a word for you. He has a blessing for you.
#  For healing has come. Help has come."
clip "19" "healing_has_come" 986 1013

echo ""
echo "=== V2 CLIP SUMMARY ==="
for f in "$OUT"/*.mp4; do
  name=$(basename "$f" .mp4)
  duration=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$f" 2>/dev/null)
  duration_int=${duration%.*}
  echo "  ${duration_int}s  $name"
done
echo ""
echo "Total clips: $(ls "$OUT"/*.mp4 | wc -l | tr -d ' ')"
echo "Saved to: $OUT/"
